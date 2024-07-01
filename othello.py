#Esta es la implementación correspondiente al othello. Las cosas que se
#han dejado comentadas son herramientas que se han usado para obetener
#los resultados de los enfrentamientos. Las funciones que tienen un 1 al
#final y tienen el mismo nombre que otras que son iguales exceptuando que
#las que tienen un 1 estan hechas para manejar la estructura de los tableros
#que se modifica para poder usarlos en montecarlo.

import time
import random
from math import sqrt

from multiprocessing import Queue

from numpy import log
from copy import deepcopy


tablero_inicial = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):0,('d',3):0,('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'B',('e',4):'N',('f',4):0,('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

lista_letras = ['a','b','c','d','e','f','g','h']
#Comprueba si una casilla es vacia y si en alguna de sus casillas adyacentes hay
#una ficha del color contrario al color del jugador al que le toca poner una ficha.
def casillas_alrededor_color_contrario(tablero,casilla,color):
    if tablero[casilla] != 0:
        return False,[]
    if color == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    if casilla[0] == 'a':
        lc = [0,1]
    elif casilla[0] == 'h':
        lc = [-1,0]
    else:
        lc = [-1,0,1]
    if casilla[1] == 1:
        lf = [0,1]
    elif casilla[1] == 8:
        lf = [-1,0]
    else:
        lf = [-1,0,1]
    casillas_posibles = []
    for i in lc:
        for j in lf:
            if i != 0 or j != 0:
                casilla_aux = (chr(ord(casilla[0])+i),casilla[1]+j)
                if tablero[casilla_aux] == contrario:
                    casillas_posibles.append(casilla_aux)   
    if casillas_posibles != []:
        return True,casillas_posibles
    return False,[]

def casilla_en_tablero(casilla):
    return 'a'<=casilla[0] and casilla[0]<='h' and 1<=casilla[1] and casilla[1]<=8

    

#Dada una casilla y una casilla adyacente que se sabe que es del color contrario
#devuelve un booleano indicando si se produce giro de fichas al colocar una ficha
#del color indicado en la casilla  en caso de ser cierto que fichas habria que 
#girar.
def giro(tablero,casilla,casilla_posible,color_casilla):
    direc = (ord(casilla_posible[0])-ord(casilla[0]),casilla_posible[1]-casilla[1])
    if color_casilla == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    l = []
    casilla_aux = casilla_posible
    while tablero[casilla_aux] == contrario and casilla_en_tablero((chr(ord(casilla_aux[0])+direc[0]),casilla_aux[1]+direc[1])):
        l.append(casilla_aux)
        casilla_aux = (chr(ord(casilla_aux[0])+direc[0]),casilla_aux[1]+direc[1])
    if tablero[casilla_aux] == color_casilla and l != []:
        return True,l
    else:
        return False,[]

def giros(tablero,casilla,casillas_posibles,color_casilla):
    l = []
    for i in casillas_posibles:
        valor_aux = giro(tablero,casilla,i,color_casilla)
        if valor_aux[0] == True:
            l.append(valor_aux[1])
    if l != []:
        return True,l
    else:
        return False,l

#Dada una casilla y un color devuelve un booleano indicando si es moviento valido
#colocar una ficha de dicho color en la casilla.
def movimiento_valido(tablero,casilla,color):
    casillas_posibles = casillas_alrededor_color_contrario(tablero,casilla,color)
    return (casillas_posibles[0] and giros(tablero,casilla,casillas_posibles[1],color)[0])
 
  
#Devuelve una lista con todos los posibles tableros que se pueden obtener con las
#jugadas del jugador al que le toca el turno.
def hijos(tablero,turno):
    hijos = []
    for i in lista_letras:
        for j in range(1,9):
            casilla_aux = i,j
            hay_casillas_posibles = casillas_alrededor_color_contrario(tablero,casilla_aux,turno)
            if hay_casillas_posibles[0]:
                jugada = giros(tablero,casilla_aux,hay_casillas_posibles[1],turno)
                if jugada[0]:
                    tablero_aux = tablero.copy()
                    tablero_aux[casilla_aux] = turno
                    for k in jugada[1]:
                        for h in k:
                            tablero_aux[h] = turno
                    hijos.append(tablero_aux)
    return hijos

def esta_lleno(tablero):
    for i in lista_letras:
        for j in range(1,9):
            if tablero[(i,j)] == 0:
                return False
    return True

def terminal(tablero):
    if esta_lleno(tablero):
        return True
    for i in lista_letras:
        for j in range(1,9):
            if movimiento_valido(tablero,(i,j),'N') or movimiento_valido(tablero,(i,j),'B'):
                return False          
    return True 

def esquina(casilla):
    if casilla == ('a',1) or casilla == ('a',8) or casilla == ('h',1) or casilla == ('h',8):
        return True
    return False

def heuristica(tablero):
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if esquina((i,j)):
                if tablero[(i,j)] == 'N':
                    n_negras += 10
                elif tablero[(i,j)] == 'B':
                    n_blancas += 10
            else:
                if tablero[(i,j)] == 'N':
                    n_negras += 1
                elif tablero[(i,j)] == 'B':
                    n_blancas += 1
    return n_negras - n_blancas


def adyacentes_esquina(casilla):
    if casilla == ('a',2) or casilla == ('a',7) or casilla == ('b',1) or casilla == ('b',2) or casilla == ('b',7) or casilla == ('b',8) or casilla == ('g',1) or  casilla == ('g',2) or casilla == ('g',7) or casilla == ('g',8) or casilla == ('h',2) or casilla == ('h',7):
        return True
    return False
            
#Se consideran un hijo no traqnuilo cuando del tablero padre al hijo se produce
#que el jugador solo pueda realizar una jugada o si se ocupa una esquina o una 
#casilla adyacente a una esquina.
def no_tranquilo(tablero1,tablero2,turno):
    if turno == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    mov_validos = 0
    for i in lista_letras:
        for j in range(1,9):
            casilla_aux = (i,j)
            if movimiento_valido(tablero2,casilla_aux,contrario):
                mov_validos += 1
            if esquina(casilla_aux) or adyacentes_esquina(casilla_aux):
                if tablero1[casilla_aux] == 0 and tablero2[casilla_aux] != 0:
                    return True
    return mov_validos == 1

def minimax_alfa_beta(tablero, profundidad, alfa, beta, jugador):
    if profundidad == 0 or terminal(tablero):
        return heuristica(tablero), None

    if jugador == 'N':
        mejor_valor = float('-inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
                valor, _ = minimax_alfa_beta(hijo, profundidad - 1, alfa, beta, 'B')
                if valor >= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor > beta:
                    break
                alfa = max(alfa, valor)
        if mejor_movimiento == None:
            mejor_movimiento = tablero
        return mejor_valor, mejor_movimiento

    else:
        mejor_valor = float('inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
                valor, _ = minimax_alfa_beta(hijo, profundidad - 1, alfa, beta, 'N')
                if valor <= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor < alfa:
                    break
                beta = min(beta, valor)
        if mejor_movimiento == None:
            mejor_movimiento = tablero
        return mejor_valor, mejor_movimiento

def quiescence_search(tablero, profundidad, alfa, beta, jugador):
    if profundidad == 0 or terminal(tablero):
        return heuristica(tablero), None

    if jugador == 'N':
        mejor_valor = float('-inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
            if no_tranquilo(tablero,hijo,jugador):
                valor, _ = minimax_alfa_beta(hijo, profundidad, alfa, beta, 'B')
                if valor >= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor > beta:
                    break
                alfa = max(alfa, valor)
            else:
                valor, _ = quiescence_search(hijo, profundidad - 1, alfa, beta, 'B')
                if valor >= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor > beta:
                    break
                alfa = max(alfa, valor)
        if mejor_movimiento == None:
            mejor_movimiento = tablero
        return mejor_valor, mejor_movimiento

    else:
        mejor_valor = float('inf')
        mejor_movimiento = None
        for hijo in hijos(tablero, jugador):
            if no_tranquilo(tablero,hijo,jugador):
                valor, _ = minimax_alfa_beta(hijo, profundidad, alfa, beta, 'N')
                if valor <= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor < alfa:
                    break
                beta = min(beta, valor)
            else:
                valor, _ = quiescence_search(hijo, profundidad - 1, alfa, beta, 'N')
                if valor <= mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = hijo
                if valor < alfa:
                    break
                beta = min(beta, valor)
        if mejor_movimiento == None:
            mejor_movimiento = tablero
        return mejor_valor, mejor_movimiento
                        
def jugar(tablero,profundidad1,profundidad2):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        a,tablero1 = minimax_alfa_beta(tablero2,profundidad1,float('-inf'),float('inf'),'N')
        ultimo = tablero1
        if not(terminal(tablero1)):
            b,tablero2 = minimax_alfa_beta(tablero1,profundidad2,float('-inf'),float('inf'),'B')
            ultimo = tablero2
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo[(i,j)] == 'N':
                n_negras += 1
            elif ultimo[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return profundidad1, profundidad2,n_negras,n_blancas,ganador


def jugar_negro(tablero,profundidad1,profundidad2):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        a,tablero1 = quiescence_search(tablero2,profundidad1,float('-inf'),float('inf'),'N')
        ultimo = tablero1
        if not(terminal(tablero1)):
            b,tablero2 = minimax_alfa_beta(tablero1,profundidad2,float('-inf'),float('inf'),'B')
            ultimo = tablero2
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo[(i,j)] == 'N':
                n_negras += 1
            elif ultimo[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return profundidad1, profundidad2,n_negras,n_blancas,ganador

def jugar_blanco(tablero,profundidad1,profundidad2):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        a,tablero1 = minimax_alfa_beta(tablero2,profundidad1,float('-inf'),float('inf'),'N')
        ultimo = tablero1
        if not(terminal(tablero1)):
            b,tablero2 = quiescence_search(tablero1,profundidad2,float('-inf'),float('inf'),'B')
            ultimo = tablero2
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo[(i,j)] == 'N':
                n_negras += 1
            elif ultimo[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return profundidad1, profundidad2,n_negras,n_blancas,ganador

def tablero_aleatorio(tablero,numero_movimientos,turno):
    if turno == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    if numero_movimientos == 0:
        return tablero
    if terminal(tablero):
        return tablero
    else:    
        l = hijos(tablero, turno)
        if l ==[]:
            resultado = tablero_aleatorio(tablero,numero_movimientos,contrario)
        else:
            tab_aleatorio = random.choice(l)
            resultado = tablero_aleatorio(tab_aleatorio,numero_movimientos-1,contrario)  
    return resultado

movimientos = [2,4,6,8,10]
'''
tableros_aleatorios = []
while len(tableros_aleatorios) < 20:
    num_movimientos = random.choice(movimientos)
    tablero = tablero_aleatorio(tablero_inicial,num_movimientos,'N')
    if tablero not in tableros_aleatorios:
        tableros_aleatorios.append(tablero)
'''

tablero_2 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 'B', ('d', 5): 'B', ('e', 5): 'B', ('f', 5): 'N', ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 0, ('f', 6): 'N', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 'N', ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_3 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):0,('d',3):0,('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):'N',('d',4):'N',('e',4):'N',('f',4):0,('g',4):0,('h',4):0,
('a',5):0,('b',5):'B',('c',5):'B',('d',5):'B',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):'N',('d',6):0,('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_4  ={('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):'B',('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):'N',('c',3):'B',('d',3):'N',('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'B',('e',4):'N',('f',4):0,('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_5 ={('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):0,('d',3):'N',('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'N',('e',4):'B',('f',4):'B',('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'B',('e',5):'N',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):'B',('d',6):0,('e',6):'N',('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_6 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):0,('d',3):0,('e',3):'B',('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):'N',('d',4):'N',('e',4):'B',('f',4):0,('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):'B',('f',6):'N',('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_7 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):0,('d',3):0,('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'B',('e',4):'B',('f',4):'B',('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'B',('e',5):'N',('f',5):'N',('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):'N',('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):'N',('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_8 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):'B',('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):'N',('c',3):'N',('d',3):'B',('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'B',('e',4):'N',('f',4):0,('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_9 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):'B',('d',3):0,('e',3):'B',('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):'N',('d',4):'B',('e',4):'N',('f',4):'N',('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'B',('f',5):0,('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):0,('f',6):0,('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_10 = {('a',1):0,('b',1):0,('c',1):0,('d',1):0,('e',1):0,('f',1):0,('g',1):0,('h',1):0,
('a',2):0,('b',2):0,('c',2):0,('d',2):0,('e',2):0,('f',2):0,('g',2):0,('h',2):0,
('a',3):0,('b',3):0,('c',3):'N',('d',3):0,('e',3):0,('f',3):0,('g',3):0,('h',3):0,
('a',4):0,('b',4):0,('c',4):0,('d',4):'N',('e',4):'B',('f',4):'B',('g',4):0,('h',4):0,
('a',5):0,('b',5):0,('c',5):0,('d',5):'N',('e',5):'N',('f',5):'B',('g',5):0,('h',5):0,
('a',6):0,('b',6):0,('c',6):0,('d',6):0,('e',6):0,('f',6):'B',('g',6):0,('h',6):0,
('a',7):0,('b',7):0,('c',7):0,('d',7):0,('e',7):0,('f',7):0,('g',7):0,('h',7):0,
('a',8):0,('b',8):0,('c',8):0,('d',8):0,('e',8):0,('f',8):0,('g',8):0,('h',8):0}

tablero_aleatorio1 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 'N', ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 'N', ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'B', ('e', 5): 'B', ('f', 5): 'B', ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio2 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 'N', ('c', 3): 'N', ('d', 3): 'N', ('e', 3): 'B', ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'B', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 0, ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio3 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 'B', ('f', 6): 'B', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 'B', ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio4 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'N', ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'N', ('e', 4): 'B', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 'B', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 'B', ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio5 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 'N', ('d', 4): 'B', ('e', 4): 'B', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 'N', ('c', 5): 0, ('d', 5): 'B', ('e', 5): 'B', ('f', 5): 'N', ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 'B', ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 'B', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 'B', ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio6 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'B', ('d', 3): 'N', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 'B', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 'N', ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio7 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 'B', ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 0, ('f', 3): 'B', ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 'N', ('c', 4): 'N', ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio8 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'N', ('d', 3): 'B', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'B', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio9 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 'B', ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 'B', ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 'N', ('d', 6): 'N', ('e', 6): 'N', ('f', 6): 'B', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}

tablero_aleatorio10 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'B', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'N', ('f', 5): 'N', ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 0, ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio11 ={('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 'B', ('c', 2): 'N', ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'B', ('d', 3): 'N', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 'N', ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'B', ('f', 6): 'B', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio12 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 'N', ('f', 2): 'B', ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 'B', ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 'B', ('d', 5): 'B', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 0, ('f', 6): 'N', ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio13 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'N', ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 'N', ('d', 6): 'N', ('e', 6): 'B', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 'B', ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio14 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 'B', ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'B', ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'N', ('e', 4): 'B', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio15 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 'N', ('c', 3): 'N', ('d', 3): 0, ('e', 3): 'B', ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 'B', ('c', 4): 'B', ('d', 4): 'B', ('e', 4): 'B', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 'N', ('f', 6): 'N', ('g', 6): 'N', ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio16 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 'N', ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'B', ('e', 4): 'B', ('f', 4): 'N', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'B', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 'B', ('d', 6): 0, ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}



tablero_aleatorio17 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 'B', ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 'B', ('d', 4): 'B', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 'B', ('d', 5): 'N', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio18 = {('a', 1): 0, ('b', 1): 'N', ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 'B', ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 'N', ('d', 2): 0, ('e', 2): 0, ('f', 2): 'B', ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 'N', ('e', 3): 'B', ('f', 3): 'B', ('g', 3): 'B', ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 0, ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 0, ('e', 6): 0, ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio19 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 'B', ('b', 4): 0, ('c', 4): 'N', ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 0, ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 'B', ('b', 5): 'B', ('c', 5): 'N', ('d', 5): 'N', ('e', 5): 'N', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 'B', ('b', 6): 0, ('c', 6): 'B', ('d', 6): 'N', ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 'B', ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}


tablero_aleatorio20 = {('a', 1): 0, ('b', 1): 0, ('c', 1): 0, ('d', 1): 0, ('e', 1): 0, ('f', 1): 0, ('g', 1): 0, ('h', 1): 0,
    ('a', 2): 0, ('b', 2): 0, ('c', 2): 0, ('d', 2): 0, ('e', 2): 0, ('f', 2): 0, ('g', 2): 0, ('h', 2): 0,
    ('a', 3): 0, ('b', 3): 0, ('c', 3): 0, ('d', 3): 0, ('e', 3): 0, ('f', 3): 0, ('g', 3): 0, ('h', 3): 0,
    ('a', 4): 0, ('b', 4): 0, ('c', 4): 'N', ('d', 4): 'N', ('e', 4): 'N', ('f', 4): 'B', ('g', 4): 0, ('h', 4): 0,
    ('a', 5): 0, ('b', 5): 0, ('c', 5): 0, ('d', 5): 'N', ('e', 5): 'B', ('f', 5): 0, ('g', 5): 0, ('h', 5): 0,
    ('a', 6): 0, ('b', 6): 0, ('c', 6): 0, ('d', 6): 'B', ('e', 6): 'N', ('f', 6): 0, ('g', 6): 0, ('h', 6): 0,
    ('a', 7): 0, ('b', 7): 0, ('c', 7): 0, ('d', 7): 0, ('e', 7): 0, ('f', 7): 0, ('g', 7): 0, ('h', 7): 0,
    ('a', 8): 0, ('b', 8): 0, ('c', 8): 0, ('d', 8): 0, ('e', 8): 0, ('f', 8): 0, ('g', 8): 0, ('h', 8): 0}



tableros = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10,tablero_aleatorio1,tablero_aleatorio2,tablero_aleatorio3,tablero_aleatorio4,tablero_aleatorio5,tablero_aleatorio6,tablero_aleatorio7,tablero_aleatorio8,tablero_aleatorio9,tablero_aleatorio10,tablero_aleatorio11,tablero_aleatorio12,tablero_aleatorio13,tablero_aleatorio14,tablero_aleatorio15,tablero_aleatorio16,tablero_aleatorio17,tablero_aleatorio18,tablero_aleatorio19,tablero_aleatorio20]
tableros_mios = [tablero_inicial,tablero_2,tablero_3,tablero_4,tablero_5,tablero_6,tablero_7,tablero_8,tablero_9,tablero_10]

def jugar_procesos(tablero,cola_profundidades,cola_resultado):
    profundidades = 0
    while profundidades != None:
        profundidades = cola_profundidades.get()
        cola_profundidades.put(None)
        if profundidades != None:
            a = jugar(tablero,profundidades[0],profundidades[1])
            cola_resultado.put(a)
    cola_resultado.put(None)
    
def jugar_procesos_quiescence_search_negro(tablero,cola_profundidades,cola_resultado):
    profundidades = 0
    while profundidades != None:
        profundidades = cola_profundidades.get()
        cola_profundidades.put(None)
        if profundidades != None:
            a = jugar_negro(tablero,profundidades[0],profundidades[1])
            cola_resultado.put(a)
    cola_resultado.put(None)

def jugar_procesos_quiescence_search_blanco(tablero,cola_profundidades,cola_resultado):
    profundidades = 0
    while profundidades != None:
        profundidades = cola_profundidades.get()
        cola_profundidades.put(None)
        if profundidades != None:
            a = jugar_blanco(tablero,profundidades[0],profundidades[1])
            cola_resultado.put(a)
    cola_resultado.put(None)


distintas_profundidades = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,2),(2,3),(2,4),(2,5),(3,1),(3,2),(3,3),(3,4),(3,5),(4,1),(4,2),(4,3),(4,4),(4,5),(5,1),(5,2),(5,3),(5,4),(5,5)]
profundidad_6 = [(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(6,5),(6,4),(6,3),(6,2),(6,1)]
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
        if i == 25:
            break
        if not cola_resultado.empty():
            a = cola_resultado.get()
            if a == None:
                contador_fin += 1
            else:
                print(a)
                i = i+1
                l.append(a)
    for proceso in procesos:
        cola_resultado.put(None)
        proceso.join()
    fin = time.time()
    duracion = fin-inicio
    print(f"Duración: {duracion} segundos")


'''
if __name__ == "__main__":
    main(tablero_inicial)
'''

'''
j= 0
if __name__ == "__main__":
    for i in tableros:
        main(i)
        j = j + 1
        print('tablero_', j)

'''
  

'''
profundidad_6 = [(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(6,5),(6,4),(6,3),(6,2),(6,1)]
profundidad_7 = [(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(7,6),(7,5),(7,4),(7,3),(7,2),(7,1)]
for i in tableros:  
    for j in profundidad_7:
        inicio = time.time()
        resultado = jugar(i,j[0],j[1])
        fin = time.time()
        duracion = fin-inicio
        print(resultado,duracion)
'''






def ganador(tablero):
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if tablero[(i,j)] == 'N':
                n_negras += 1
            elif tablero[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return ganador
def crear_tablero(estado, padre=None):
    return {"estado": estado,"hijos": [],"estadisticas": {"visitas": 0, "ganancias": 0},"visitado": False,"padre": padre}



#Comprueba si una casilla es vacia y si en alguna de sus casillas adyacentes hay
#una ficha del color contrario al color del jugador al que le toca poner una ficha.
def casillas_alrededor_color_contrario1(tablero,casilla,color):
    if tablero["estado"][casilla] != 0:
        return False,[]
    if color == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    if casilla[0] == 'a':
        lc = [0,1]
    elif casilla[0] == 'h':
        lc = [-1,0]
    else:
        lc = [-1,0,1]
    if casilla[1] == 1:
        lf = [0,1]
    elif casilla[1] == 8:
        lf = [-1,0]
    else:
        lf = [-1,0,1]
    casillas_posibles = []
    for i in lc:
        for j in lf:
            if i != 0 or j != 0:
                casilla_aux = (chr(ord(casilla[0])+i),casilla[1]+j)
                if tablero["estado"][casilla_aux] == contrario:
                    casillas_posibles.append(casilla_aux)   
    if casillas_posibles != []:
        return True,casillas_posibles
    return False,[]



    

#Dada una casilla y una casilla adyacente que se sabe que es del color contrario
#devuelve un booleano indicando si se produce giro de fichas al colocar una ficha
#del color indicado en la casilla  en caso de ser cierto que fichas habria que 
#girar.
def giro1(tablero,casilla,casilla_posible,color_casilla):
    direc = (ord(casilla_posible[0])-ord(casilla[0]),casilla_posible[1]-casilla[1])
    if color_casilla == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    l = []
    casilla_aux = casilla_posible
    while tablero["estado"][casilla_aux] == contrario and casilla_en_tablero((chr(ord(casilla_aux[0])+direc[0]),casilla_aux[1]+direc[1])):
        l.append(casilla_aux)
        casilla_aux = (chr(ord(casilla_aux[0])+direc[0]),casilla_aux[1]+direc[1])
    if tablero["estado"][casilla_aux] == color_casilla and l != []:
        return True,l
    else:
        return False,[]

def giros1(tablero,casilla,casillas_posibles,color_casilla):
    l = []
    for i in casillas_posibles:
        valor_aux = giro1(tablero,casilla,i,color_casilla)
        if valor_aux[0] == True:
            l.append(valor_aux[1])
    if l != []:
        return True,l
    else:
        return False,l

#Dada una casilla y un color devuelve un booleano indicando si es moviento valido
#colocar una ficha de dicho color en la casilla.
def movimiento_valido1(tablero,casilla,color):
    casillas_posibles = casillas_alrededor_color_contrario1(tablero,casilla,color)
    return (casillas_posibles[0] and giros1(tablero,casilla,casillas_posibles[1],color)[0])
 
  
#Devuelve una lista con todos los posibles tableros que se pueden obtener con las
#jugadas del jugador al que le toca el turno.
def hijos1(tablero,turno):
    todos_hijos = []
    for i in lista_letras:
        for j in range(1,9):
            casilla_aux = i,j
            hay_casillas_posibles = casillas_alrededor_color_contrario1(tablero,casilla_aux,turno)
            if hay_casillas_posibles[0]:
                jugada = giros1(tablero,casilla_aux,hay_casillas_posibles[1],turno)
                if jugada[0]:
                    tablero_aux = tablero["estado"].copy()
                    tablero_aux[casilla_aux] = turno
                    for k in jugada[1]:
                        for h in k:
                            tablero_aux[h] = turno
                    hijo = crear_tablero(tablero_aux,tablero)
                    todos_hijos.append(hijo)
    tablero["hijos"] = todos_hijos
    return todos_hijos

def esta_lleno1(tablero):
    for i in lista_letras:
        for j in range(1,9):
            if tablero["estado"][(i,j)] == 0:
                return False
    return True

def terminal1(tablero):
    if esta_lleno1(tablero):
        return True
    for i in lista_letras:
        for j in range(1,9):
            if movimiento_valido1(tablero,(i,j),'N') or movimiento_valido1(tablero,(i,j),'B'):
                return False          
    return True 

def no_hay_mov1(tablero,jugador):
    for i in lista_letras:
        for j in range(1,9):
            if movimiento_valido1(tablero,(i,j),jugador):
                return False          
    return True



def heuristica1(tablero):
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if esquina((i,j)):
                if tablero["estado"][(i,j)] == 'N':
                    n_negras += 10
                elif tablero["estado"][(i,j)] == 'B':
                    n_blancas += 10
            else:
                if tablero["estado"][(i,j)] == 'N':
                    n_negras += 1
                elif tablero["estado"][(i,j)] == 'B':
                    n_blancas += 1
    return n_negras - n_blancas


            
#Se consideran un hijo no traqnuilo cuando del tablero padre al hijo se produce
#que el jugador solo pueda realizar una jugada o si se ocupa una esquina o una 
#casilla adyacente a una esquina.
def no_tranquilo1(tablero1,tablero2,turno):
    if turno == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    mov_validos = 0
    for i in lista_letras:
        for j in range(1,9):
            casilla_aux = (i,j)
            if movimiento_valido1(tablero2,casilla_aux,contrario):
                mov_validos += 1
            if esquina(casilla_aux) or adyacentes_esquina(casilla_aux):
                if tablero1["estado"][casilla_aux] == 0 and tablero2["estado"][casilla_aux] != 0:
                    return True
    return mov_validos == 1


                        

def ganador1(tablero):
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if tablero["estado"][(i,j)] == 'N':
                n_negras += 1
            elif tablero["estado"][(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return ganador,n_negras,n_blancas


def eliminar(lista):
    for i in lista:
        i["hijos"] = []

def montecarlo(tablero,iteraciones,jugador):
    tableros_creados = []
    if no_hay_mov1(tablero, jugador):
        return tablero
    tablero_aux = tablero.copy()
    tablero_aux["visitado"] = True
    hijos1(tablero_aux,jugador)
    for i in tablero_aux["hijos"]:
        tableros_creados.append(i)
    for iteracion in range(iteraciones):
        hoja = expandir(tablero_aux,jugador,tableros_creados)
        resultado = simulacion(hoja[0],hoja[1],tableros_creados)
        retroprogramacion(hoja[0],resultado[0][0],jugador)
    hijo_elegido = escoger_hijo(tablero_aux,jugador)
    eliminar(tableros_creados)
    return hijo_elegido

def expandir(tablero,jugador,tableros_creados):
    i = 0
    if  jugador == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    while not esta_lleno1(tablero):
        if todos_hijos_visitados(tablero,jugador,tableros_creados):
           if i%2 == 0:    
                tablero = mejor_uct(tablero,jugador)
                i += 1
           else:
               tablero = mejor_uct(tablero,contrario)
               i += 1
               
        else:
            tablero = no_visitados(tablero,jugador) or tablero
            break
    if i%2 ==1:
        jugador = contrario
    return tablero,jugador
        

def simulacion(tablero,jugador,tableros_creados):
    i = 0
    if  jugador == 'N':
        contrario = 'B'
    else:
        contrario = 'N'
    while not terminal1(tablero):
        if i%2 == 0:
            tablero = simulacion_aleatoria(tablero, contrario,tableros_creados) 
            i +=1
        else:
            tablero = simulacion_aleatoria(tablero,jugador,tableros_creados)
            i+=1
    return ganador1(tablero),tablero["estado"]

def retroprogramacion(tablero,resultado,jugador):
    while tablero is not None:
        actualizar_ganancias(tablero,resultado,jugador)
        tablero = tablero["padre"]
        
def actualizar_ganancias(tablero, resultado,jugador):
    tablero["estadisticas"]["visitas"] += 1
    if resultado[0] == 'E':
        resultado = 0.5
    else:
        if jugador == 'N':
            if resultado == 'N':
                resultado = 1
            else:
                resultado = 0
        else:
            if resultado == 'B':
                resultado = 1
            else:
                resultado = 0
    tablero["estadisticas"]["ganancias"] += resultado

def escoger_hijo(tablero,jugador):
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
    no_visitados = tablero
    for hijo in tablero["hijos"]:
        if hijo["visitado"] == False:
            no_visitados = hijo
            hijo["visitado"] = True
            break

    return no_visitados
    
def mejor_uct(tablero,jugador):
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
    if tablero["hijos"] == []:
        return tablero
    else:
        hijo = random.choice(tablero["hijos"])
        return hijo


def jugar_montecarlo_montecarlo(tablero,iteraciones1,iteraciones2):
    tablero2 = crear_tablero(tablero)
    tablero1 = crear_tablero(tablero)
    while not(terminal1(tablero2)) and not(terminal1(tablero1)):
        tablero1 = montecarlo(tablero2, iteraciones1, 'N')
        ultimo = tablero1
        if not(terminal1(tablero1)):
            tablero2 = montecarlo(tablero1, iteraciones2, 'B')
            ultimo = tablero2
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo["estado"][(i,j)] == 'N':
                n_negras += 1
            elif ultimo["estado"][(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return iteraciones1, iteraciones2,n_negras,n_blancas,ganador


def jugar_minmax_montecarlo(tablero,profundidad,iteraciones):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        a,tablero1 = minimax_alfa_beta(tablero2,profundidad,float('-inf'),float('inf'),'N')
        ultimo = tablero1
        if not(terminal(tablero1)):
            tablero1 = crear_tablero(tablero1)
            tablero2 = montecarlo(tablero1, iteraciones, 'B')
            tablero2 = tablero2["estado"]
            ultimo = tablero2
            tablero1 = tablero1["estado"]
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo[(i,j)] == 'N':
                n_negras += 1
            elif ultimo[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return profundidad, iteraciones,n_negras,n_blancas,ganador

def jugar_montecarlo_minmax(tablero,profundidad,iteraciones):
    tablero2 = tablero
    tablero1 = tablero
    while not(terminal(tablero2)) and not(terminal(tablero1)):
        tablero2 = crear_tablero(tablero2)
        tablero1 = montecarlo(tablero2, iteraciones, 'N')
        tablero1 = tablero1["estado"]
        ultimo = tablero1
        if not(terminal(tablero1)):
            a,tablero2 = minimax_alfa_beta(tablero1,profundidad,float('-inf'),float('inf'),'B')
            ultimo = tablero2
        else:
            tablero2 = tablero2["estado"]
    n_negras = 0
    n_blancas = 0
    for i in lista_letras:
        for j in range(1,9):
            if ultimo[(i,j)] == 'N':
                n_negras += 1
            elif ultimo[(i,j)] == 'B':
                n_blancas += 1
    if n_negras > n_blancas:
        ganador = 'N'
    elif n_negras < n_blancas:
        ganador = 'B'
    else:
        ganador = 'E'
    return profundidad, iteraciones,n_negras,n_blancas,ganador

def tiempo_medio_poda(tableros,profundidad):
    tableros_aux = deepcopy(tableros)
    tiempo = 0
    for i in tableros_aux:
        inicio = time.time()
        minimax_alfa_beta(i, profundidad,float('-inf') , float('inf'), 'N')
        fin = time.time()
        duracion = fin -inicio
        tiempo += duracion
    return tiempo/30

def tiempo_medio_montecarlo(tableros,iteraciones):
    tableros_aux = deepcopy(tableros)
    tiempo = 0
    for i in tableros_aux:
        i = crear_tablero(i)
        inicio = time.time()
        montecarlo(i, iteraciones, 'N')
        fin = time.time()
        duracion = fin -inicio
        tiempo += duracion
    return tiempo/30

'''
tiempo_medio_poda(tableros,3)
0.008488019307454428
tiempo_medio_montecarlo(tableros,1)
0.008447750409444173

tiempo_medio_poda(tableros,4)
0.052770773569742836
tiempo_medio_montecarlo(tableros,5)
0.05326383908589681

tiempo_medio_poda(tableros,5)
0.290666389465332
tiempo_medio_montecarlo(tableros,27)
0.29188016255696614


tiempo_medio_poda(tableros,6)
2.2045265197753907
tiempo_medio_montecarlo(tableros,145)
2.218624639511108

tiempo_medio_poda(tableros,7)
11.188161484400432
tiempo_medio_montecarlo(tableros,765)
11.604261207580567

tiempo_medio_montecarlo(tableros,3000)
41.15516487757365
'''

iteraciones_montecarlo = [(1,1),(1,5),(1,27),(1,145),(1,765),(1,3000),(5,1),(5,5),(5,27),(5,145),(5,765),(5,3000),(27,1),(27,5),(27,27),(27,145),(27,765),(27,3000),(145,1),(145,5),(145,27),(145,145),(145,765),(145,3000),(765,1),(765,5),(765,27),(765,145),(765,765),(765,3000),(3000,1),(3000,5),(3000,27),(3000,145),(3000,765),(3000,3000)]
iteraciones_poda_montecarlo = [(3,1),(3,5),(3,27),(3,145),(3,765),(3,3000),(4,1),(4,5),(4,27),(4,145),(4,765),(4,3000),(5,1),(5,5),(5,27),(5,145),(5,765),(5,3000),(6,1),(6,5),(6,27),(6,145),(6,765),(6,3000),(7,1),(7,5),(7,27),(7,145),(7,765),(7,3000)]


'''
for j in iteraciones_poda_montecarlo:
    inicio = time.time()
    resultado = jugar_montecarlo_minmax(tablero_aleatorio1, j[0], j[1])
    fin = time.time()
    duracion = fin-inicio
    print(resultado,duracion)
'''

    