import csv
import random

#Lista que representa las opiciones en la escala de Likert

esc = [1,2,3,4]

#Pesos ficticios para cada item del instrumento
p01 = [5,10,50,35]
p02 = [4,8,55,33]
p03 = [6,12,48,34]
p04 = [3,9,60,28]
p05 = [7,11,49,33]
p06 = [5,13,54,27]
p07 = [6,13,54,27]
p08 = [8,16,45,31]
p09 = [4,10,53,33]
p10 = [7,15,46,32]
p11 = [5,12,50,33]
p12 = [6,14,51,29]
p13 = [4,13,52,31]
p14 = [3,10,54,33]

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
with open('data2.csv', mode='w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)

    # Escribir filas en el archivo CSV
    escritor_csv.writerows(data)

print("Archivo CSV creado exitosamente con columnas.")


