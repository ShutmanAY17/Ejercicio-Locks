import threading
import logging
import time

class CuentaBancaria:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def depositar(self, cantidad):
        with self.lock:
            self.balance += cantidad

    def retirar(self, cantidad):
        with self.lock:
            if cantidad <= self.balance:
                self.balance -= cantidad
            else:
                print("No hay suficiente saldo.")


def worker(lock: threading.Lock, cuenta: CuentaBancaria):
    hizo_movimiento = False
    num_tries = 0
    while not hizo_movimiento:
        time.sleep(0.5)
        logging.debug('Intentando abrir')
        num_tries += 1
        have_it = lock.acquire(0)
        try:
            if have_it:
                logging.debug('Intento %d: Abierto, puedo entrar', num_tries)
                realizar_transacciones(cuenta)
            else:
                logging.debug('Intento %d: Cerrado, sigue intentando', num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Realizado después de %d intentos', num_tries)

def realizar_transacciones(cuenta):
    for _ in range(100):
        cuenta.depositar(10)
        cuenta.retirar(5)

def lock_holder(lock: threading.Lock):
    logging.debug('Iniciando')
    while True:
        lock.acquire()
        try:
            logging.debug('Ocupado')
            time.sleep(0.5)
        finally:
            logging.debug('Disponible')
            lock.release()
        time.sleep(0.5)

def main():
    cuenta = CuentaBancaria()
    hilos = []

    logging.basicConfig(
        level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
    )

    holder = threading.Thread(target=lock_holder, args=(cuenta.lock) name='LockHolder', daemon=True, )
    holder.start()

    for _ in range(5):
        hilo = threading.Thread(target=worker, args=(cuenta.lock, cuenta), name='Worker')
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"Saldo final: {cuenta.balance}")

if __name__ == '__main__':
    main()
