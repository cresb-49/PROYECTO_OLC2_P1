import pyTypeParser as parser
from pyTypeParser import Scope
# from pyTypeParser import Sentencias
from pyTypeParser import Resultado
from Instrucciones.entorno import Entorno


# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()
print('#### PARSER EJECUTADO')
result: Resultado = parser.parse(input)
print('#### PARSER FINALIZADO')

print('#### INTRUCIONES RECUPERADAS')
print(result.sentencias)

entorno = Entorno(0, 0, result.tabla_simbolos[0], result.sentencias)

print('#### ENTORNOS GENERADOS')
for n in result.tabla_simbolos:
    if isinstance(n, Scope):
        print('Scope ->', n, ", Anterior ->", n.anterior)
        for x in n.variables.get_diccionario():
            print('  ', n.variables.get_diccionario()[x])
        for x in n.funciones.get_diccionario():
            print('  ', n.funciones.get_diccionario()[x])

print(entorno)
print('#### EJECUCION DEL CODIGO')
entorno.ejecutar(None)
