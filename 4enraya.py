#Se verá que hay funciones iguales que hacen lo mismo y que se llaman
#igual salvo porque algunas tienen un 1 al final del nombre. Esto es así porque
#la estructura de los tableros que usa el minimmax y montecarlo son
#diferentes y se modifican ligeramente las funciones para que funcionen
# bien para los métodos. Las que tiene  un 1 al final son las modificadas
#para que funcione bien montecarlo. Se verá que hay cosas comentadas. Estas
#cosas se dejan para que se vea como se han generado los tableros aleatorios
#o como se han llevado a cabo las simulaciones.
import random
import time
from math import sqrt
from multiprocessing import Process,Queue
from numpy import log
from copy import deepcopy





tablero_inicial = {(0,0):0,(0,1):0,(0,2):0,(0,3):0,(0,4):0,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):0,(1,4):0,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):0,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_2 = {(0,0):0,(0,1):0,(0,2):2,(0,3):1,(0,4):0,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):1,(1,4):0,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):2,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_3 = {(0,0):0,(0,1):1,(0,2):1,(0,3):2,(0,4):0,(0,5):2,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):1,(1,4):0,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):2,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_4 = {(0,0):0,(0,1):0,(0,2):1,(0,3):2,(0,4):1,(0,5):2,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):0,(1,4):0,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):0,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_5 = {(0,0):0,(0,1):0,(0,2):0,(0,3):1,(0,4):2,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):2,(1,4):0,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):1,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_6 = {(0,0):0,(0,1):0,(0,2):0,(0,3):2,(0,4):1,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):0,(1,3):1,(1,4):1,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):2,(2,4):2,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):1,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):2,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_7 = {(0,0):0,(0,1):2,(0,2):0,(0,3):0,(0,4):1,(0,5):0,(0,6):0,
(1,0):0,(1,1):1,(1,2):0,(1,3):0,(1,4):2,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):0,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_8 = {(0,0):0,(0,1):0,(0,2):1,(0,3):1,(0,4):2,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):1,(1,3):2,(1,4):1,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):1,(2,3):0,(2,4):2,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):2,(3,3):0,(3,4):2,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_9 = {(0,0):1,(0,1):0,(0,2):1,(0,3):0,(0,4):2,(0,5):0,(0,6):2,
(1,0):0,(1,1):0,(1,2):1,(1,3):0,(1,4):1,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):2,(2,3):0,(2,4):0,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):2,(3,3):0,(3,4):0,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):0,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):0,(5,5):0,(5,6):0}

tablero_10 = {(0,0):1,(0,1):0,(0,2):2,(0,3):2,(0,4):1,(0,5):0,(0,6):0,
(1,0):0,(1,1):0,(1,2):1,(1,3):0,(1,4):1,(1,5):0,(1,6):0,
(2,0):0,(2,1):0,(2,2):0,(2,3):0,(2,4):2,(2,5):0,(2,6):0,
(3,0):0,(3,1):0,(3,2):0,(3,3):0,(3,4):2,(3,5):0,(3,6):0,
(4,0):0,(4,1):0,(4,2):0,(4,3):0,(4,4):2,(4,5):0,(4,6):0,
(5,0):0,(5,1):0,(5,2):0,(5,3):0,(5,4):1,(5,5):0,(5,6):0}

tablero_aleatorio1 = {(0,0): 0,(0,1): 1,(0,2): 2,(0,3): 0,(0,4): 1,(0,5): 1,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 2,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio2 ={(0,0): 1,(0,1): 1,(0,2): 0,(0,3): 2,(0,4): 1,(0,5): 0,(0,6): 0,(1,0): 2,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 2,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio3 = {(0,0): 1,(0,1): 1,(0,2): 0,(0,3): 2,(0,4): 0,(0,5): 1,(0,6): 2,(1,0): 2,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio4 =  {(0,0): 0,(0,1): 1,(0,2): 1,(0,3): 0,(0,4): 0,(0,5): 2,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio5 = {(0,0): 1,(0,1): 0,(0,2): 1,(0,3): 2,(0,4): 2,(0,5): 0,(0,6): 1,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 2,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio6 = {(0,0): 1,(0,1): 1,(0,2): 2,(0,3): 1,(0,4): 0,(0,5): 2,(0,6): 0,(1,0): 2,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio7 = {(0,0): 1,(0,1): 0,(0,2): 0,(0,3): 0,(0,4): 0,(0,5): 2,(0,6): 1,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 2,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio8 = {(0,0): 0,(0,1): 0,(0,2): 2,(0,3): 0,(0,4): 1,(0,5): 0,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio9 = {(0,0): 2,(0,1): 0,(0,2): 0,(0,3): 1,(0,4): 2,(0,5): 1,(0,6): 2,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 1,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio10 = {(0,0): 1,(0,1): 0,(0,2): 1,(0,3): 0,(0,4): 0,(0,5): 0,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 2,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio11 = {(0,0): 2,(0,1): 0,(0,2): 1,(0,3): 0,(0,4): 0,(0,5): 2,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 1,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio12 = {(0,0): 0,(0,1): 0,(0,2): 2,(0,3): 0,(0,4): 2,(0,5): 1,(0,6): 1,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio13 = {(0,0): 2,(0,1): 0,(0,2): 0,(0,3): 0,(0,4): 0,(0,5): 1,(0,6): 1,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 2,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 1,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio14 = {(0,0): 1,(0,1): 1,(0,2): 0,(0,3): 0,(0,4): 2,(0,5): 0,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio15 = {(0,0): 0,(0,1): 1,(0,2): 1,(0,3): 0,(0,4): 2,(0,5): 0,(0,6): 2,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio16 = {(0,0): 1,(0,1): 2,(0,2): 0,(0,3): 0,(0,4): 0,(0,5): 0,(0,6): 2,(1,0): 0,(1,1): 1,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 1,(2,0): 0,(2,1): 2,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio17 = {(0,0): 0,(0,1): 0,(0,2): 2,(0,3): 0,(0,4): 0,(0,5): 1,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio18 = {(0,0): 0,(0,1): 1,(0,2): 0,(0,3): 2,(0,4): 0,(0,5): 2,(0,6): 0,(1,0): 0,(1,1): 2,(1,2): 0,(1,3): 1,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 1,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio19 = {(0,0): 0,(0,1): 1,(0,2): 0,(0,3): 1,(0,4): 2,(0,5): 0,(0,6): 2,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}

tablero_aleatorio20 = {(0,0): 0,(0,1): 0,(0,2): 0,(0,3): 1,(0,4): 0,(0,5): 2,(0,6): 0,(1,0): 0,(1,1): 0,(1,2): 0,(1,3): 0,(1,4): 0,(1,5): 0,(1,6): 0,(2,0): 0,(2,1): 0,(2,2): 0,(2,3): 0,(2,4): 0,(2,5): 0,(2,6): 0,(3,0): 0,(3,1): 0,(3,2): 0,(3,3): 0,(3,4): 0,(3,5): 0,(3,6): 0,(4,0): 0,(4,1): 0,(4,2): 0,(4,3): 0,(4,4): 0,(4,5): 0,(4,6): 0,(5,0): 0,(5,1): 0,(5,2): 0,(5,3): 0,(5,4): 0,(5,5): 0,(5,6): 0}




tableros_mios = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10]
tableros = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10,tablero_aleatorio1,tablero_aleatorio2,tablero_aleatorio3,tablero_aleatorio4,tablero_aleatorio5,tablero_aleatorio6,tablero_aleatorio7,tablero_aleatorio8,tablero_aleatorio9,tablero_aleatorio10,tablero_aleatorio11,tablero_aleatorio12,tablero_aleatorio13,tablero_aleatorio14,tablero_aleatorio15,tablero_aleatorio16,tablero_aleatorio17,tablero_aleatorio18,tablero_aleatorio19,tablero_aleatorio20]

def casillas_contiguas(casilla):
    lista_casillas = []
    for i in range(-1,2):
        for j in range(-1,2):
            if 0<=casilla[0]+i<=5 and 0<=casilla[1]+j<=6 and (i!=0 or j!=0):
                lista_casillas.append((casilla[0]+i,casilla[1]+j))
    return lista_casillas

def numero_fichas(tablero):
    suma_fichas = 0
    for i in tablero:
        if tablero[i] != 0:
            suma_fichas = suma_fichas + 1
    return suma_fichas


conjuntos_de4 = []
for i in list(tablero_inicial.keys()):
    if i[0]+3 <= 5:
        conjuntos_de4.append([i,(i[0]+1,i[1]),(i[0]+2,i[1]),(i[0]+3,i[1])])
    if i[1]+3 <= 6:
        conjuntos_de4.append([i,(i[0],i[1]+1),(i[0],i[1]+2),(i[0],i[1]+3)])
    if i[0]+3 <= 5 and i[1]+3 <= 6:
        conjuntos_de4.append([i,(i[0]+1,i[1]+1),(i[0]+2,i[1]+2),(i[0]+3,i[1]+3)])
    if i[0]+3 <= 5 and i[1]-3 >= 0:
        conjuntos_de4.append([i,(i[0]+1,i[1]-1),(i[0]+2,i[1]-2),(i[0]+3,i[1]-3)])

def heuristica(tablero):
    l = []
    n_ceros = 0
    n_unos = 0
    n_doses = 0
    total = 0
    for i in conjuntos_de4:
        for j in i:
            l.append(tablero[j])
        for k in l:
            if k == 0:
                n_ceros = n_ceros + 1
            elif k == 1:
                n_unos = n_unos + 1
            else:
                n_doses = n_doses + 1
        if n_unos == 4:
            total = float('inf')
        elif n_unos == 3 and n_ceros == 1:
            total = total +9
        elif n_unos == 2 and n_ceros == 2:
            total = total +3
        elif n_doses == 4:
            total = float('-inf')
        elif n_doses == 3 and n_ceros == 1:
            total = total -9
        elif n_doses == 2 and n_ceros == 2:
            total = total -3
        l = []
        n_ceros = 0
        n_unos = 0
        n_doses = 0
    return total

def esta_lleno(tablero):
    for i in list(tablero.values()):
        if i == 0:
            return False
    return True

def terminal(tablero):
    if heuristica(tablero) == float('inf') or heuristica(tablero) == float('-inf'):
        return True
    elif esta_lleno(tablero):
        return True
    else:
        return False



def hijos(tablero,jugador):
   hijos_tablero = []
   for i in range(7):
       j = 0
       tablero_aux = tablero.copy()
       while j<=5 and tablero[(j,i)] != 0:
           j = j+1
       if j != 6:
          if jugador:
              tablero_aux[(j,i)] = 1
          else:
              tablero_aux[(j,i)] = 2
          hijos_tablero.append(tablero_aux)
   return hijos_tablero



def tablero_aleatorio(tablero,numero_movimientos,turno):
    if numero_movimientos == 0:
        return tablero
    l = hijos(tablero, turno)
    tab_aleatorio = random.choice(l)
    resultado = tablero_aleatorio(tab_aleatorio,numero_movimientos-1,not turno)  
    return resultado   

def cuatro_en_raya(tablero):
    for i in conjuntos_de4:
        if tablero[i[0]] == 1 and tablero[i[1]] == 1 and tablero[i[2]] == 1 and tablero[i[3]] == 1:
            return i,1
        elif tablero[i[0]] == 2 and tablero[i[1]] == 2 and tablero[i[2]] == 2 and tablero[i[3]] == 2:
            return i,2
    return [],0

movimientos = [2,3,4,5,6]
'''
tableros = []
tableros = tableros + tableros_mios

while len(tableros) < 30:
    num_movimientos = random.choice(movimientos)
    tablero = tablero_aleatorio(tablero_inicial,num_movimientos,True)
    if tablero not in tableros:
        tableros.append(tablero)
'''



def minimax_alfa_beta(tablero, profundidad, alfa, beta, jugador):
    if profundidad == 0 or terminal(tablero):
        return heuristica(tablero), None
    l = []
    if jugador:
        mejor_valor = float('-inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
            valor, _ = minimax_alfa_beta(hijo, profundidad - 1, alfa, beta, False)
            if valor >= mejor_valor:
                if valor == mejor_valor:
                    l.append(hijo)
                else:
                    l = [hijo]
                mejor_valor = valor
                mejor_movimiento = hijo
            if valor > beta:
                break
            alfa = max(alfa, valor)
        mejor_movimiento = random.choice(l)
        return mejor_valor, mejor_movimiento

    else:
        mejor_valor = float('inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
            valor, _ = minimax_alfa_beta(hijo, profundidad - 1, alfa, beta, True)
            if valor <= mejor_valor:
                if valor == mejor_valor:
                    l.append(hijo)
                else:
                    l = [hijo]
                mejor_valor = valor
                mejor_movimiento = hijo
            if valor < alfa:
                break
            beta = min(beta, valor)
        mejor_movimiento = random.choice(l)
        return mejor_valor, mejor_movimiento

def crear_tablero(estado, padre=None):
    return {"estado": estado,"hijos": [],"estadisticas": {"visitas": 0, "ganancias": 0},"visitado": False,"padre": padre}




tableros_mios = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10]
tableros = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10,tablero_aleatorio1,tablero_aleatorio2,tablero_aleatorio3,tablero_aleatorio4,tablero_aleatorio5,tablero_aleatorio6,tablero_aleatorio7,tablero_aleatorio8,tablero_aleatorio9,tablero_aleatorio10,tablero_aleatorio11,tablero_aleatorio12,tablero_aleatorio13,tablero_aleatorio14,tablero_aleatorio15,tablero_aleatorio16,tablero_aleatorio17,tablero_aleatorio18,tablero_aleatorio19,tablero_aleatorio20]


def numero_fichas1(tablero):
    suma_fichas = 0
    for i in tablero["estado"]:
        if tablero["estado"][i] != 0:
            suma_fichas = suma_fichas + 1
    return suma_fichas

def n_fichas_jugadores1(tablero):
    fichas1 =0 
    fichas2 = 0
    for i in tablero["estado"]:
        if tablero["estado"][i] == 1:
            fichas1 = fichas1 +1
        elif tablero["estado"][i] == 2:
            fichas2 = fichas2 +1
    return fichas1,fichas2



def heuristica1(tablero):
    total = 0
    for conjunto in conjuntos_de4:
        n_ceros = 0
        n_unos = 0
        n_doses = 0
        
        for indice in conjunto:
            valor = tablero["estado"][indice]
            if valor == 0:
                n_ceros = n_ceros + 1
            elif valor == 1:
                n_unos = n_unos + 1
            elif valor == 2:
                n_doses = n_doses + 1
        
        if n_unos == 4:
            return float('inf')
        elif n_doses == 4:
            return float('-inf')
        elif n_unos == 3 and n_ceros == 1:
            total = total + 9
        elif n_doses == 3 and n_ceros == 1:
            total = total - 9
        elif n_unos == 2 and n_ceros == 2:
            total = total + 3
        elif n_doses == 2 and n_ceros == 2:
            total = total - 3
    return total


def esta_lleno1(tablero):
    for i in list(tablero["estado"].values()):
        if i == 0:
            return False
    return True

def terminal1(tablero):
    if heuristica1(tablero) == float('inf') or heuristica1(tablero) == float('-inf'):
        return True
    elif esta_lleno1(tablero):
        return True
    else:
        return False



def hijos1(tablero,jugador):
   hijos_tablero = []
   for i in range(7):
       j = 0
       tablero_aux = tablero["estado"].copy()
       while j<=5 and tablero_aux[(j,i)] != 0:
           j = j+1
       if j != 6:
          if jugador:
              tablero_aux[(j,i)] = 1
          else:
              tablero_aux[(j,i)] = 2
          hijo = crear_tablero(tablero_aux,tablero)
          hijos_tablero.append(hijo)
   tablero["hijos"] = hijos_tablero
   return hijos_tablero

  

movimientos = [2,3,4,5,6,8,10,12,14,16,18,20,22,24]

tableros_aleatorios = []
'''
while len(tableros_aleatorios) < 70:
    num_movimientos = random.randint(1, 41)
    tablero = tablero_aleatorio(tablero_inicial,num_movimientos,True)
    tablero_aleatorio1 = crear_tablero(tablero)
    if tablero_aleatorio1 not in tableros_aleatorios:
        tableros.append(tablero_aleatorio1)
'''



def jugar_partida(profundidad1,profundidad2,tablero):
    i = 0
    j = 0
    while not terminal(tablero):
        if i == j:
            tablero = minimax_alfa_beta(tablero,profundidad1,float('-inf'),float('inf'),True)[1]
            i = i+1
        elif not terminal(tablero):
            tablero = minimax_alfa_beta(tablero,profundidad2,float('-inf'),float('inf'),False)[1]
            j = j+1
    conj,jug = cuatro_en_raya(tablero)
    return tablero,conj,jug

        

def cuatro_en_raya1(tablero):
    for i in conjuntos_de4:
        if tablero["estado"][i[0]] == 1 and tablero["estado"][i[1]] == 1 and tablero["estado"][i[2]] == 1 and tablero["estado"][i[3]] == 1:
            return i,1
        elif tablero["estado"][i[0]] == 2 and tablero["estado"][i[1]] == 2 and tablero["estado"][i[2]] == 2 and tablero["estado"][i[3]] == 2:
            return i,2
    return [],0
            

    

def jugar_procesos(tablero,cola_profundidades,cola_resultado):
     profundidades = 0
     while profundidades != None:
         profundidades = cola_profundidades.get()
         cola_profundidades.put(None)
         if profundidades != None:
             a = jugar_partida(profundidades[0],profundidades[1],tablero)
             cola_resultado.put(a)


distintas_profundidades = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),(1,7),(1,8), 
                          (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),(2,7),(2,8), 
                          (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),(3,7),(3,8), 
                          (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),(4,7),(4,8), 
                          (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),(5,7),(5,8), 
                          (6, 1), (6, 2), (6, 3),  (6, 4), (6, 5), (6, 6), (6, 7),(6,8),
                          (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),(7,7),(7,8),
                          (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6),(8,7),(8,8)]

def main(tablero):
    inicio = time.time()
    nr_buscadores = 4
    cola_resultado = Queue()
    profundidades = Queue()
    l = []
    for i in distintas_profundidades:
        profundidades.put(i)
    procesos = [Process(target=jugar_procesos, args=(tablero,profundidades,cola_resultado)) for i in range(nr_buscadores)]
    for proceso in procesos:
        proceso.start()
    contador_fin = 0
    i = 0
    while True:
        if contador_fin == nr_buscadores:
            break
        if i == 64:
            break
        if not cola_resultado.empty():
            a = cola_resultado.get()
            i = i+1
            l.append(a)
    for proceso in procesos:
        cola_resultado.put(None)
        proceso.join()
    fin = time.time()
    duracion = fin-inicio
    with open("resultado.txt", "w") as archivo:
        for item in l:
            archivo.write(f"{item}\n")
    print(l)
    print(f"Duración: {duracion} segundos")


'''
if __name__ == "__main__":
    main(tablero_aleatorio10)
'''

'''
j= 11
if __name__ == "__main__":
    for i in tableros[20:]:
        main(i)
        j = j + 1
        print('tablero_', j)
'''
    
def eliminar(lista):
    for i in lista:
        i["hijos"] = []           

def montecarlo(tablero,iteraciones,jugador):
    tableros_creados = []
    tablero_aux = deepcopy(tablero)
    tablero_aux["visitado"] = True
    hijos1(tablero_aux,jugador)
    for i in tablero_aux["hijos"]:
        tableros_creados.append(i)
    for iteracion in range(iteraciones):
        hoja = expandir(tablero_aux,jugador,tableros_creados)
        resultado = simulacion(hoja[0],hoja[1],tableros_creados)
        retroprogramacion(hoja[0],resultado[0],jugador)
        '''
        print(iteracion)
        '''
    hijo_elegido = hijo_escogido(tablero_aux,jugador)
    eliminar(tableros_creados)
    return hijo_elegido



def expandir(tablero,jugador,tableros_creados):
    i = 0
    while not esta_lleno1(tablero):
        if todos_hijos_visitados(tablero,jugador,tableros_creados):  
            tablero = mejor_uct(tablero)
            i += 1
               
        else:
            tablero = no_visitados(tablero,jugador) or tablero
            break
    if i%2 ==1:
        jugador = not jugador
    return tablero,jugador
        

def simulacion(tablero,jugador,tableros_creados):
    i = 0
    while not terminal1(tablero):
        if i%2 == 0:
            tablero = simulacion_aleatoria(tablero, not jugador,tableros_creados) 
            i +=1
        else:
            tablero = simulacion_aleatoria(tablero,jugador,tableros_creados)
            i+=1
    return cuatro_en_raya1(tablero)[1],n_fichas_jugadores1(tablero),tablero["estado"]

def retroprogramacion(tablero,resultado,jugador):
    while tablero is not None:
        actualizar_ganancias(tablero,resultado,jugador)
        tablero = tablero["padre"]
        
def actualizar_ganancias(tablero, resultado,jugador):
    tablero["estadisticas"]["visitas"] += 1
    if resultado == 0:
        resultado = 0.5
    else:
        if jugador:
            if resultado == 2:
                resultado = 0
        else:
            if resultado == 1:
                resultado = 0
            else:
                resultado = 1
    tablero["estadisticas"]["ganancias"] += resultado

def hijo_escogido(tablero,jugador):
    max_visitas = float('-inf')
    hijo_escogido = None
    
    for hijo in tablero["hijos"]:
        if hijo["estadisticas"]["visitas"] >= max_visitas:
            max_visitas = hijo["estadisticas"]["visitas"]
            hijo_escogido = hijo
    return hijo_escogido

def todos_hijos_visitados(tablero,jugador,tableros_creados):
    if tablero["hijos"] == []:
        hijos1(tablero, jugador) 
        for i in tablero["hijos"]:
            tableros_creados.append(i)
    if terminal1(tablero):
        return False
    else:
        for hijo in tablero["hijos"]:
            if hijo["visitado"] == False:
                return False
    return True


def no_visitados(tablero,jugador):
    no_visitados = []
    for hijo in tablero["hijos"]:
        if hijo["visitado"] == False:
            no_visitados.append(hijo)
    if no_visitados ==[]:
        escogido = tablero
    else:
        escogido = random.choice(no_visitados)
        escogido["visitado"] = True
    return escogido


    
def mejor_uct(tablero):
    max_uct = float('-inf')
    hijo_escogido = None
    c = sqrt(2)
    visitas_tablero = tablero["estadisticas"]["visitas"]
    for hijo in tablero["hijos"]:
        w = hijo["estadisticas"]["ganancias"]
        n = hijo["estadisticas"]["visitas"]
        uct = (w/n)+(c*sqrt(log(visitas_tablero)/n))
        if (uct>=max_uct):
                max_uct = uct
                hijo_escogido = hijo
    return hijo_escogido
    

def simulacion_aleatoria(tablero,jugador,tableros_creados):
    hijos1(tablero,jugador)
    for i in tablero["hijos"]:
        tableros_creados.append(i)
    hijo = random.choice(tablero["hijos"])
    return hijo

def cantidad(tablero_estado,numero):
    cantidad = 0
    for i in tablero_estado:
        if tablero_estado[i] == numero:
            cantidad += 1
    return cantidad




def jugar_montecarlo_montecarlo(tablero,iteraciones1,iteraciones2):
    tablero2 = crear_tablero(tablero)
    tablero1 = crear_tablero(tablero)
    while not(terminal1(tablero2)) and not(terminal1(tablero1)):
        tablero1 = montecarlo(tablero2, iteraciones1, True)
        ultimo = tablero1
        if not(terminal1(tablero1)):
            tablero2 = montecarlo(tablero1, iteraciones2, False)
            ultimo = tablero2
    conj,jug = cuatro_en_raya1(ultimo)
    return iteraciones1, iteraciones2,conj,jug


def jugar_minmax_montecarlo(tablero,profundidad,iteraciones):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        a,tablero1 = minimax_alfa_beta(tablero2,profundidad,float('-inf'),float('inf'),True)
        ultimo = tablero1
        if not(terminal(tablero1)):
            tablero1 = crear_tablero(tablero1)
            tablero2 = montecarlo(tablero1, iteraciones, False)
            tablero2 = tablero2["estado"]
            ultimo = tablero2
            tablero1 = tablero1["estado"]
    conj,jug = cuatro_en_raya(ultimo)
    return profundidad, iteraciones,conj,jug

def jugar_montecarlo_minmax(tablero,profundidad,iteraciones):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        tablero2 = crear_tablero(tablero2)
        tablero1 = montecarlo(tablero2, iteraciones, True)
        tablero1 = tablero1["estado"]
        ultimo = tablero1
        if not(terminal(tablero1)):
            a,tablero2 = minimax_alfa_beta(tablero1,profundidad,float('-inf'),float('inf'),False)
            ultimo = tablero2
        else:
            tablero2 = tablero2["estado"]
    conj,jug = cuatro_en_raya(ultimo)
    return profundidad, iteraciones,conj,jug

def tiempo_medio_poda(tableros,profundidad):
    tableros_aux = deepcopy(tableros)
    tiempo = 0
    for i in tableros_aux:
        a=numero_fichas(i)
        if a%2 == 0:
            jugador = True
        else:
            jugador = False
        inicio = time.time()
        minimax_alfa_beta(i, profundidad,float('-inf') , float('inf'), jugador)
        fin = time.time()
        duracion = fin -inicio
        tiempo += duracion
    return tiempo/30

def tiempo_medio_montecarlo(tableros,iteraciones):
    tableros_aux = deepcopy(tableros)
    tiempo = 0
    for i in tableros_aux:
        i = crear_tablero(i)
        a=numero_fichas1(i)
        if a%2 == 0:
            jugador = True
        else:
            jugador = False
        inicio = time.time()
        montecarlo(i, iteraciones, jugador)
        fin = time.time()
        duracion = fin -inicio
        tiempo += duracion
    return tiempo/30



'''
tiempo_medio_poda(tableros,2)
0.0026381969451904296
tiempo_medio_montecarlo(tableros,1)
0.002635812759399414

tiempo_medio_poda(tableros,3)
0.015746506055196126
tiempo_medio_montecarlo(tableros,7)
0.015708374977111816

tiempo_medio_poda(tableros,4)
0.07273549238840739
tiempo_medio_montecarlo(tableros,31)
0.07378881772359212

tiempo_medio_poda(tableros,5)
0.3732462803522746
tiempo_medio_montecarlo(tableros,140)
0.3717538356781006

tiempo_medio_poda(tableros,6)
1.691063141822815
tiempo_medio_montecarlo(tableros,685)
1.687225071589152

tiempo_medio_poda(tableros,7)
6.834467395146688
tiempo_medio_montecarlo(tableros,2700)
6.879983973503113

tiempo_medio_poda(tableros,8)
50.67181860605876
tiempo_medio_montecarlo(tableros,31250)
50.717760769526166

'''

iteraciones_montecarlo = [(31250,1),(31250,7),(31250,31),(31250,140),(31250,685),(31250,2700),(31250,31250)]
iteraciones_poda_montecarlo = [(3,7),(3,31),(3,140),(3,685),(3,2700),(3,31250),(4,7),(4,31),(4,140),(4,685),(4,2700),(4,31250),(5,7),(5,31),(5,140),(5,685),(5,2700),(5,31250),(6,7),(6,31),(6,140),(6,685),(6,2700),(6,31250),(7,7),(7,31),(7,140),(7,685),(7,2700),(7,31250),(8,7),(8,31),(8,140),(8,685),(8,2700),(8,31250)]


'''
for j in tableros:
    for i in iteraciones_poda_montecarlo:
        inicio = time.time()
        resultado = jugar_minmax_montecarlo(j, i[0], i[1])
        fin = time.time()
        duracion = fin-inicio
        print(resultado,duracion)
'''
