import pyTypeParser as parser
from pyTypeParser import Scope
from pyTypeParser import Sentencias

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()
print('#### PARSER EJECUTADO')
result:Sentencias = parser.parse(input)
print('#### PARSER FINALIZADO')
print('#### DEBUJ RESULT')
for n in result.intrucciones:
    print (n)
    #if isinstance(n,Scope):
    #    print('Actual',n,'Anterior',n.anterior)
    #    for x in n.variables.get_diccionario():
    #        print(x)