import pyTypeParser as parser

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()

result = parser.parse(input)
print(result)