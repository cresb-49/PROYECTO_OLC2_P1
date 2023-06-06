import pyTypeParser as parser
from pyTypeParser import Scope

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()

result = parser.parse(input)
for n in result:
    if isinstance(n,Scope):
        print('Actual',n,'Anterior',n.anterior)
        for x in n.variables.get_diccionario():
            print(x)