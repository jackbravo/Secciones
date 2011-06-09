#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# can change this later for optparse
# (argparse only available on python 2.7 which is not installed on ubuntu server 10.04)
import sys 
import csv
import re

def main():
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
    fieldnames = reader.fieldnames
    fieldnames.append('tipo de comida')
    fieldnames.append('caracteristicas')
    fieldnames.append('para')
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    headers = dict( (n,n) for n in fieldnames )
    writer.writerow(headers)

    for row in reader:
        row['tipo de comida'] = getTipoComida(row)
        row['caracteristicas'] = getCaracteristicas(row)
        row['para'] = getPara(row)
        writer.writerow(row)

    infile.close()
    outfile.close()


def getTipoComida(row):
    tipoComida = []
    cleanCategory = row['category']
    cleanCategory = cleanCategory.replace('Restaurantes-Cocina ', '')
    cleanCategory = cleanCategory.replace('Restaurantes-', '')
    cleanCategory = cleanCategory.replace('Restaurantes en General', '')
    cleanCategory = cleanCategory.replace('Mariscos', 'Pescados y Mariscos')
    cleanCategory = cleanCategory.replace('Especialidades del Mar', 'Pescados y Mariscos')
    cleanCategory = cleanCategory.replace('Comida Naturista', 'Naturista / Vegetariana')
    cleanCategory = cleanCategory.replace('Vegetariana', 'Naturista / Vegetariana')
    if re.match("Comida R", cleanCategory):
        cleanCategory = 'Fast Food'
    if re.match("Japonesa", cleanCategory):
        cleanCategory = 'Japonesa/Sushi'
    if re.match("Pizza", cleanCategory):
        cleanCategory = 'Pizza'

    cleanCategory = cleanCategory.strip()

    if cleanCategory:
        tipoComida.append(cleanCategory)

    if re.search("hamburguesa", row['servicios'], re.IGNORECASE):
        tipoComida.append('Hamburguesas')
    if re.search("hot dog", row['servicios'], re.IGNORECASE):
        tipoComida.append('Hotdogs')
    if re.search("cafe", row['servicios'], re.IGNORECASE):
        tipoComida.append('Café y Té')
    if re.search("carne", row['servicios'], re.IGNORECASE) or re.search("cortes", row['servicios'], re.IGNORECASE):
        tipoComida.append('Carnes')
    if re.search("tacos?\W", row['servicios'], re.IGNORECASE) or re.search("tacos?\W", row['marcas'], re.IGNORECASE) or re.search("tacos?\W", row['informacion'], re.IGNORECASE) or re.search("tacos?\W", row['name'], re.IGNORECASE):
        tipoComida.append('Tacos')
    return ", ".join(tipoComida)

def getCaracteristicas(row):
    caracteristicas = []
    if re.search("diversion", row['servicios'], re.IGNORECASE):
        caracteristicas.append('Área para niños')
    if re.search("club", row['servicios'], re.IGNORECASE):
        caracteristicas.append('Área para niños')
    if re.search("fumar", row['servicios'], re.IGNORECASE):
        caracteristicas.append('Sección de Fumar')
    if re.search("banquetes", row['servicios'], re.IGNORECASE) or re.search("banquetes", row['marcas'], re.IGNORECASE):
        caracteristicas.append('Banquetes')
    if re.search("\Wbar\W", row['servicios'], re.IGNORECASE) or re.search("\Wbar\W", row['name'], re.IGNORECASE) or row['tipo de comida'] == 'Cantinas y Bares':
        caracteristicas.append('Bar')
    if re.search("vino", row['servicios'], re.IGNORECASE) or re.search("cerveza", row['servicios'], re.IGNORECASE):
        caracteristicas.append('Vinos y Cervezas')
    if re.search("vivo", row['servicios'], re.IGNORECASE) or re.search("vivo", row['marcas'], re.IGNORECASE) or re.search("vivo", row['informacion'], re.IGNORECASE):
        caracteristicas.append('Entretenimiento en vivo')
    if re.search("estacionamiento", row['servicios'], re.IGNORECASE) or re.search("estacionamiento", row['marcas'], re.IGNORECASE) or re.search("estacionamiento", row['informacion'], re.IGNORECASE):
        caracteristicas.append('Estacionamiento')
    if re.search("internet", row['servicios'], re.IGNORECASE) or re.search("internet", row['marcas'], re.IGNORECASE) or re.search("internet", row['informacion'], re.IGNORECASE):
        caracteristicas.append('Internet')
    if re.search("musica", row['servicios'], re.IGNORECASE) or re.search("musica", row['marcas'], re.IGNORECASE) or re.search("musica", row['informacion'], re.IGNORECASE):
        caracteristicas.append('Música')
    if re.search("salones", row['servicios'], re.IGNORECASE) or re.search("salones", row['marcas'], re.IGNORECASE) or re.search("salones", row['category'], re.IGNORECASE):
        caracteristicas.append('Salónes Privados')
    if re.search("master", row['formas_de_pago'], re.IGNORECASE) or re.search("visa", row['formas_de_pago'], re.IGNORECASE) or re.search("american", row['formas_de_pago'], re.IGNORECASE):
        caracteristicas.append('Tarjétas de crédito')
    if re.search("terraza", row['servicios'], re.IGNORECASE) or re.search("jardin", row['servicios'], re.IGNORECASE):
        caracteristicas.append('Terraza o Jardín')
    if re.search("valet parking", row['servicios'], re.IGNORECASE) or re.search("valet parking", row['marcas'], re.IGNORECASE) or re.search("valet parking", row['informacion'], re.IGNORECASE):
        caracteristicas.append('Valet Parking')
    return ", ".join(caracteristicas)

def getPara(row):
    para = []
    if re.search("desayuno", row['servicios'], re.IGNORECASE) or re.search("desayuno", row['marcas'], re.IGNORECASE) or re.search("desayuno", row['informacion'], re.IGNORECASE):
        para.append('Desayunar')
    if re.search("cena", row['servicios'], re.IGNORECASE) or re.search("cena", row['marcas'], re.IGNORECASE) or re.search("cena", row['informacion'], re.IGNORECASE):
        para.append('Cenar')
    return ", ".join(para)

if __name__ == '__main__':
    main()

