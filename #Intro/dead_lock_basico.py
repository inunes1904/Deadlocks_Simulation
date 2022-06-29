
from threading import Thread, Lock
import time

def robot_vermelho(lock1, lock2):
    """
    Nesta função simulamos o acesso por parte do robot vermelho
    correspondente a Thread Azul no qual acede a duas fechaduras
    e depois liberta-as
    """
    while True:
        print("Robot Vermelho: A receber fechadura1..")
        lock1.acquire()
        print("Robot Vermelho: A receber fechadura2..")
        lock2.acquire()
        lock1.release()
        lock2.release()
        print("Robot Vermelho: Fechaduras estão livres..")
        time.sleep(0.5)

def robot_azul(lock1, lock2):
    """
    Nesta função simulamos o acesso por parte do robot azul
    correspondente a Thread Vermelho no qual acede a duas fechaduras
    e depois liberta-as no entanto neste caso a ordem esta diferente
    para forçar o Deadlock
    """
    while True:
        print("Robot Azul: A receber fechadura1..")
        lock1.acquire()
        print("Robot Azul: A receber fechadura2..")
        lock2.acquire()
        lock1.release()
        lock2.release()
        print("Robot Azul: Fechaduras estão livres..")
        time.sleep(0.5)

# Instanciamos dois Mutual Exclusion Objects e em cada um tem um objecto do tipo fechadura
mutex1 = Lock()
mutex2 = Lock()

# Criacao das duas Threads enviando como argumento enviando 
# enviando dois mutex como argumentos
vermelho = Thread(target=robot_vermelho, args=(mutex1, mutex2))
azul = Thread(target=robot_azul, args=(mutex1, mutex2))

# Iniciamos as Threads
vermelho.start()
azul.start()