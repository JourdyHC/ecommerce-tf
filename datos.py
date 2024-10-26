import csv
import random

#Lista que representa las opiciones en la escala de Likert

esc = [1,2,3,4,5]

#Pesos ficticios para cada item del instrumento
p01 = [5,10,20,40,25]
p02 = [15,20,30,25,10]
p03 = [10,15,25,35,15]
p04 = [12,18,25,30,15]
p05 = [20,25,25,20,10]
p06 = [18,22,30,20,10]
p07 = [15,20,28,25,12]
p08 = [10,15,20,30,25]
p09 = [15,20,20,25,20]
p10 = [8,12,18,35,27]
p11 = [5,10,20,40,25]
p12 = [10,15,22,28,25]
p13 = [10,12,18,32,28]
p14 = [12,15,20,30,23]

#Generación de datos aleatorios
items = [
    random.choices(esc, weights=p01, k=500),
    random.choices(esc, weights=p02, k=500),
    random.choices(esc, weights=p03, k=500),
    random.choices(esc, weights=p04, k=500),
    random.choices(esc, weights=p05, k=500),
    random.choices(esc, weights=p06, k=500),
    random.choices(esc, weights=p07, k=500),
    random.choices(esc, weights=p08, k=500),
    random.choices(esc, weights=p09, k=500),
    random.choices(esc, weights=p10, k=500),
    random.choices(esc, weights=p11, k=500),
    random.choices(esc, weights=p12, k=500),
    random.choices(esc, weights=p13, k=500),
    random.choices(esc, weights=p14, k=500),
]

data = []
for x in range(500):
    row =[]
    for y in items:
        row.append(y[x]) 
    data.append(row)

# Crear el archivo CSV y escribir valores aleatorios
with open('data.csv', mode='w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)

    # Escribir filas en el archivo CSV
    escritor_csv.writerows(data)

print("Archivo CSV creado exitosamente con columnas.")


