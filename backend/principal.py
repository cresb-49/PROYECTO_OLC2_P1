import pyTypeParser as parser
from pyTypeParser import Scope
# from pyTypeParser import Sentencias
from pyTypeParser import Resultado
from Instrucciones.entorno import Entorno
from Modulos.grafico_dot import GraficoDot

import copy

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()
input = input + '\n' #Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
print('#### PARSER EJECUTADO')
result: Resultado = parser.parse(input)
print('#### PARSER FINALIZADO')

#print('#### INTRUCIONES RECUPERADAS')
#print(result.sentencias)


ambito_global: Scope = copy.deepcopy(result.tabla_simbolos[0])

ambito_global.reboot_variables()

entorno = Entorno(result,0, 0, ambito_global, result.sentencias)

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
print('#### ERRORES')

for n in result.errores:
    print(n.descripcion)

#entorno.ejecutar(None)
#print('#### CODIGO AST')
#gv = GraficoDot()
#entorno.graficar(gv,None)
#print(gv.get_dot())

