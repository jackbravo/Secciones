#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# can change this later for optparse
# (argparse only available on python 2.7 which is not installed on ubuntu server 10.04)
import sys 
import csv
import re

if len(sys.argv) != 3:
    error = "transform.py <inputFile> <outputFile>.\n"
    error+= "\n"
    error+= "Las columnas obligatorias en este archivo son:\n"
    error+= " - category\n"
    error+= " - servicios\n"
    sys.exit(error)

# http://docs.python.org/library/csv.html#csv.DictReader
infile = open(sys.argv[1])
outfile = open(sys.argv[2], 'wt')
reader = csv.DictReader(infile)
writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

for row in reader:
    row['tipo de comida'] = row['category'].replace('Restaurantes-Cocina ', '')
    row['tipo de comida'] = row['tipo de comida'].replace('Restaurantes-', '')
    row['tipo de comida'] = row['tipo de comida'].replace('Restaurantes en General', '')
    row['tipo de comida'] = row['tipo de comida'].replace('Especialidades del Mar', 'Pescados y Mariscos')
    row['tipo de comida'] = row['tipo de comida'].replace('Mariscos', 'Pescados y Mariscos')
    row['tipo de comida'] = row['tipo de comida'].replace('Comida Naturista', 'Naturista / Vegetariana')
    row['tipo de comida'] = row['tipo de comida'].replace('Vegetariana', 'Naturista / Vegetariana')
    if re.match(row['tipo de comida'], "Comida R"):
        row['tipo de comida'] = 'Fast Food'
    if re.match(row['tipo de comida'], "Japonesa"):
        row['tipo de comida'] = 'Japonesa/Sushi'

    if re.search("hamburguesa", row['servicios'], re.IGNORECASE):
        row['tipo de comida'] += ', Hamburguesas'
    if re.search("hot dog", row['servicios'], re.IGNORECASE):
        row['tipo de comida'] += ', Hotdogs'
    if re.search("cafe", row['servicios'], re.IGNORECASE):
        row['tipo de comida'] += ', Café y Té'
    if re.search("carne", row['servicios'], re.IGNORECASE) or re.search("cortes", row['servicios'], re.IGNORECASE):
        row['tipo de comida'] += ', Carnes'

#-----------------------

    row['caracteristicas'] = ''
    if re.search("diversion", row['servicios'], re.IGNORECASE):
        row['caracteristicas'] += ', Área para niños'
    if re.search("club", row['servicios'], re.IGNORECASE):
        row['caracteristicas'] += ', Área para niños'
    if re.search("banquetes", row['servicios'], re.IGNORECASE):
        row['caracteristicas'] += ', Banquetes'
    if re.search("\Wbar\W", row['servicios'], re.IGNORECASE) or re.search("\Wbar\W", row['name'], re.IGNORECASE) or row['tipo de comida'] == 'Cantinas y Bares':
        row['caracteristicas'] += ', Bar'
    if re.search("vino", row['servicios'], re.IGNORECASE) or re.search("cerveza", row['servicios'], re.IGNORECASE):
        row['caracteristicas'] += ', Vinos y Cervezas'

    print row['tipo de comida'] + "\t" + row['caracteristicas']

