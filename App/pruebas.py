import config as cf
from DISClib.ADT.graph import gr, vertices
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from math import radians, cos, sin, asin, sqrt
assert cf
import model
from model import analyzer
import csv


def separador_comas(cadena:str):

    n_cadena = cadena.split(",")

    return n_cadena

cadena = 'Bogotá, Colombia'

lista = separador_comas(cadena)


def conseguir_npais(lista):
    nombre = ''
    tam = len(lista)
    if tam < 2:
        nombre = lista

    elif tam <= 2 :
        nombre= lista[tam-1]
    
    return nombre

def conseguir_nciudad(lista):

    nombre = ''
    tam = len(lista)
    if tam < 2:
        nombre = lista
    elif tam == 2 :
        nombre=  lista[tam-2]
    elif tam < 3:
        nombre = lista[tam-3]
    return nombre
    
print(conseguir_npais(lista))
print(conseguir_nciudad(lista))