"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from model import analyzer
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
countriesfile = 'countries.csv'
concectionsfile = 'connections.csv'
landingfile = 'landing_points.csv'

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador.")
    print("2- Cargar información del catálogo.")
    print("3- Componentes conectados.")
    print("4- Encontrar landing points.")
    print("5- El mejor camino entre dos países.")

analyzer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando...")
        analyzer = controller.init()
        controller.loadData(analyzer, countriesfile,landingfile,concectionsfile)
        controller.conexion_total(analyzer)

    elif int(inputs[0]) == 2:
        informacion =  controller.consulta_datos(analyzer)

        print('\n El total de landing points es: ' ,informacion[0])
        print('El total de conexiones entre landing points es: ', informacion[1])
        print('El total de países cargados es de: ', informacion[2])
        print('El primer landing point es: ', informacion[4], ", su código es: ", informacion[3],", su latitud es ", informacion[5], "y su longitud es: ", informacion[6])
    
    elif int(inputs[0]) == 3:
        lp1= input("Digite el id del landing point 1.")
        lp2= input("Digite el id del landing point 2.")

        rta= controller.requerimiento1(analyzer,lp1,lp2)
        print('El número total de clúseteres es de: ', rta[0])
        if rta[1]:
            print('Los landing points están en el mismo cluster.')
        
        else: 
            print('Los landing points no están en el mismo cluster.')

    elif int(inputs[0]) == 5:

        rta = controller.requerimiento2(analyzer)
        print("Los landing point son: ", rta[1])
        print("El número total de conexiones es de: ", rta[0])

    elif int(inputs[0]) == 5:
        p1= input("Digite el primer país.")
        p2= input("Digite el segundo país.")

        rta = controller.requerimiento3(analyzer,p1,p2)

        print('La distancia total entre las capitales de ambos países es: ', rta)

    else:
        sys.exit(0)
sys.exit(0)
