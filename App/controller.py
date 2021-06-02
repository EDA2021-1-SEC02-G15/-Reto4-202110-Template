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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    analyzer = model.analyzer()
    return analyzer

# Funciones para la carga de datos

def loadCountries(analyzer, countriesfile):

    countriesfile = cf.data_dir + countriesfile
    input_file = csv.DictReader(open(countriesfile, encoding= "utf-8"), delimiter = ",")

    for country in countriesfile:
        model.addCountry(analyzer, country)


def load_landing(analyzer, landingfile):

    landingfile = cf.data_dir + landingfile
    input_file = csv.DictReader(open(landingfile, encoding= "utf-8"), delimiter = ",")

    for lp in landingfile:
        model.addLanding(analyzer, lp)

def loadCountries(analyzer,concectionsfile):

    concectionsfile = cf.data_dir + concectionsfile
    input_file = csv.DictReader(open(concectionsfile, encoding= "utf-8"), delimiter = ",")

    for conect in concectionsfile:
        model.addCountry(analyzer, conect)
 






# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo








