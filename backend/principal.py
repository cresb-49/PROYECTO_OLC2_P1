import pyTypeParser as parser
from pyTypeParser import Scope
from pyTypeParser import Sentencias
from pyTypeParser import Resultado

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()
print('#### PARSER EJECUTADO')
result:Resultado = parser.parse(input)
print('#### PARSER FINALIZADO')

print('#### INTRUCIONES RECUPERADAS')
for n in result.sentencias.intrucciones:
    print (n)
    
print('#### ENTORNOS GENERADOS')
for n in result.tabla_simbolos:
    if isinstance(n,Scope):
        print('Actual',n,'Anterior',n.anterior)
        for x in n.variables.get_diccionario():
            print(x)