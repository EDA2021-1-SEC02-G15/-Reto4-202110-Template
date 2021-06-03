"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos

def analyzer():
    try:
        analyzer = {'landing_points': None, 
                    'connections': None, 
                    'countries': None,
                    'graph': None}
        
        analyzer['landing_points'] = mp.newMap(numelements=14000, 
                                                maptype='PROBING', 
                                                comparefunction= compareLandingIds)

        analyzer['connections'] = mp.newMap(numelements=14000, 
                                                maptype='PROBING', 
                                                comparefunction= compareroutes)
        
        analyzer['countries'] = mp.newMap(numelements=14000, 
                                                maptype='PROBING', 
                                                comparefunction= compareroutes)

        analyzer['graph'] = gr.newGraph(datastructure= "ADJ_LIST", 
                                        directed= True, size= 14000, 
                                        comparefunction= compareLandingIds)                       
        
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo


def addCountry(analyzer, country):

    entry = mp.get(analyzer['countries'], country['CapitalName'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, country['CapitalLatitude'])
        lt.addLast(lstroutes, country['CapitalLongitude'])
        lt.addLast(lstroutes, country['CountryName'])
        lt.addLast(lstroutes, country['Population'])
        lt.addLast(lstroutes, country['Internet users'])
        mp.put(analyzer['countries'], country['CapitalName'], lstroutes)
    else:
        lstroutes = entry['value']
        info = lt.newList()
        lt.addLast(info,country['CapitalLatitude'])
        lt.addLast(info,country['CapitalLongitude'])
        lt.addLast(info,country['CountryName'])
        lt.addLast(info,country['Population'])
        lt.addLast(info,country['Internet users'])
        i=0

        while i < lt.size(lstroutes):
            if not lt.isPresent(lstroutes, info[i]):
                lt.addLast(lstroutes, info[i])
            i+=0
            
    return analyzer

def addLanding(analyzer, lp):

    entry = mp.get(analyzer['landing_points'], lp['landing_point_id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, lp['latitude'])
        lt.addLast(lstroutes, lp['longitude'])
        lt.addLast(lstroutes, lp['name'])
        mp.put(analyzer['landing_points'], lp['landing_point_id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = lt.newList()
        lt.addLast(info,lp['latitude'])
        lt.addLast(info,lp['longitude'])
        lt.addLast(info,lp['name'])
        i=0

        while i < lt.size(lstroutes):
            if not lt.isPresent(lstroutes, info[i]):
                lt.addLast(lstroutes, info[i])
            i+=0
            
    return analyzer

def addConnection(analyzer, conect):

    entry = mp.get(analyzer['connections'], conect['Origin'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, conect['destination'])
        mp.put(analyzer['countries'], conect['origin'], lstroutes)
    else:
        lstroutes = entry['value']
        info = lt.newList()
        lt.addLast(info,conect['destination'])

        i=0

        while i < lt.size(lstroutes):
            if not lt.isPresent(lstroutes, info[i]):
                lt.addLast(lstroutes, info[i])
            i+=0
            
    return analyzer

def concetar_capitales(analyzer):
    
    m_c = analyzer['countries']
    m_lp= analyzer['landing_points']
    tam1 = mp.size(m_c)
    tam2 = mp.size(m_lp)
    key_c = mp.keySet(m_c)
    val_c = mp.valueSet(m_c)
    key_lp = mp.keySet(m_lp)
    val_lp = mp.valueSet(m_lp)
    i=0
    j=0

    while i < tam1:
        nombre = key_c[i]
        n_c = val_c[i][2]
        lat1 = val_c[i][0]
        long1 = val_c[i][1]
        while j < tam2:
            nombre2 = key_lp[j]
            n_c = val_lp[j][2]
            n_c2= separador_comas(n_c)[1]
            lat2 = val_lp[j][0]
            long2= val_lp[j][1]

            if n_c == n_c2:
                peso = distancia_harversine(lat1,long1,lat2,long2)
                vertices = gr.vertices(analyzer['graph'])

                if nombre not in vertices:
                    gr.insertVertex(analyzer['graph'], nombre)

                    if nombre2 not in vertices:
                        gr.insertVertex(analyzer['graph'],nombre2)
                        gr.addEdge(analyzer['graph'],nombre, nombre2, peso)
                    else:
                        gr.addEdge(analyzer['graph'],nombre, nombre2, peso)
                else:
                    if nombre2 not in vertices:
                        gr.insertVertex(analyzer['graph'],nombre2)
                        gr.addEdge(analyzer['graph'],nombre, nombre2, peso)
                    else:
                        gr.addEdge(analyzer['graph'],nombre, nombre2, peso)
            j+=1
        i+=1
                    
    return analyzer

def conectar_ciudades(analyzer):

    ciudades= gr.vertices(analyzer['graph'])
    i=0
    tam = lt.size(ciudades)

    while i<tam:
        city = gr.adjacents(analyzer['graph'],ciudades[i])
        tam2 = lt.size()
        j=0

        while j<tam:
            if j < tam-1:
                gr.addEdge(analyzer['graph'],city[j],city[j+1],0.1)

            else: gr.addEdge(analyzer['graph'], city[j],city[0],0.1)

            j+=1
        
        i+=1

    return analyzer

def conexion_total(analyzer):

    concetar_capitales(analyzer)

    tabla = analyzer['connections']
    tabla2 = analyzer['landing_points']
    grafo = analyzer['graph']
    vertices = gr.vertices(grafo)
    name = mp.keySet(tabla)
    destino = mp.valueSet(tabla)
    tam = mp.size(tabla)
    i=0

    while i < tam:

        if lt.isPresent(vertices, name[i]):
            destino_f = destino[i]
            origen_p = mp.get(tabla2, name[i])
            lat1 = origen_p[1][0]
            long1 = origen_p[1][1]
            adyacentes = gr.adjacents(grafo,name[i])

            if lt.isPresent(vertices, destino_f):
                dest_p = mp.get(tabla2, destino_f)
                lat2 = dest_p[1][0]
                long2 = dest_p[1][1]
                peso = distancia_harversine(lat1,long1,lat2,long2)

                if not lt.isPresent(adyacentes, destino_f):
                    gr.addEdge(grafo,name[i], destino_f, peso)
                
            else: 
                gr.insertVertex(grafo, destino_f)
                dest_p = mp.get(tabla2, destino_f)
                lat2 = dest_p[1][0]
                long2 = dest_p[1][1]
                peso = distancia_harversine(lat1,long1,lat2,long2)
                gr.addEdge(grafo,name[i], destino_f, peso)
        else:
            gr.addEdge(grafo, name[i])
            destino_f = destino[i]
            origen_p = mp.get(tabla2, name[i])
            lat1 = origen_p[1][0]
            long1 = origen_p[1][1]
            adyacentes = gr.adjacents(grafo,name[i])

            if lt.isPresent(vertices, destino_f):
                dest_p = mp.get(tabla2, destino_f)
                lat2 = dest_p[1][0]
                long2 = dest_p[1][1]
                peso = distancia_harversine(lat1,long1,lat2,long2)
                gr.addEdge(grafo,name[i], destino_f, peso)
                
            else: 
                gr.insertVertex(grafo, destino_f)
                dest_p = mp.get(tabla2, destino_f)
                lat2 = dest_p[1][0]
                long2 = dest_p[1][1]
                peso = distancia_harversine(lat1,long1,lat2,long2)
                gr.addEdge(grafo,name[i], destino_f, peso)
            
        vertices = gr.vertices(grafo)
        tam = mp.size(tabla)
        i+=1

    conectar_ciudades(analyzer)
    return analyzer


# Funciones para creacion de datos

# Funciones de consulta
def carga_datos(analyzer):

    num_landing_points= gr.numVertices(analyzer['graph'])
    num_conections = gr.numEdges(analyzer['graph'])
    total_paises = lt.size(mp.keySet(analyzer['countries']))
    vertice_p = gr.vertices(analyzer['graph'])
    prim_vert = lt.firstElement(vertice_p)
    tabla = analyzer['landing_points']
    print(vertice_p)
    detalles = mp.get(tabla, prim_vert)
    code = detalles[0]
    name = separador_comas(detalles[1][3])[0]
    lat = detalles[1][0]
    long = detalles[1][1]

    return num_landing_points, num_conections, total_paises, code,name, lat,long

def requerimiento1(analyzer,lp1, lp2):

    n_cluster = gr.adjacentEdges(analyzer['graph'],lp1)
    n_cluster2 = gr.adjacentEdges(analyzer['graph'],lp2)
    adyacentes = gr.adjacents(analyzer['graph'],lp1)
    tam1 = lt.size(n_cluster)
    tam2 = lt.size(n_cluster2)
    total = tam1 + tam2
    relacion = False
    if lt.isPresent(adyacentes, lp2):
        relacion = True
    
    return total, relacion



#Funciones Helper

def distancia_harversine(latitud1, longitud1, latitud2, longitud2):

    lon1, lat1, lon2, lat2 = map(radians, [longitud1, latitud1, longitud2, latitud2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c*r

def separador_comas(cadena:str):

    n_cadena = cadena.split(",")

    return n_cadena

# Funciones utilizadas para comparar elementos dentro de una lista
def compareLandingIds(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


# Funciones de ordenamiento
