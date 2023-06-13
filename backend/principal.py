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
# Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
input = input + '\n'
print('#### PARSER EJECUTADO')
result: Resultado = parser.parse(input)
print('#### PARSER FINALIZADO')

# print('#### INTRUCIONES RECUPERADAS')
# print(result.sentencias)

ambito_global: Scope = None
# Buscar si puedo hacer un deep copy sin eliminar lo que ya tengo
ambitos_copia: Scope = copy.deepcopy(ambito_global)

# print('#### ENTORNOS GENERADOS')
for n in result.tabla_simbolos:
    if isinstance(n, Scope):
        # print('Scope ->', n, ", Anterior ->", n.anterior)
        if n.tipo == 'Global':
            # ambito_global = copy.deepcopy(n)
            ambito_global = n
        # for x in n.variables.get_diccionario():
            # print('  ', n.variables.get_diccionario()[x])
        # for x in n.funciones.get_diccionario():
            # print('  ', n.funciones.get_diccionario()[x])

print('#### AMBITO GLOBAL')
ambito_global.reboot_variables()
print(ambito_global)
for x in ambito_global.variables.get_diccionario():
    print('  ', ambito_global.variables.get_diccionario()[x])
for x in ambito_global.funciones.get_diccionario():
    print('  ', ambito_global.funciones.get_diccionario()[x])
entorno = Entorno(result, 0, 0, ambito_global, result.sentencias)

result.set_scope_global(ambito_global)
print('#### ERRORES LEXER PARSER')
for n in result.errores:
    print(n)

print('#### EJECUCION DEL CODIGO')
entorno.ejecutar(None)

print('#### CONSOLA DE SALIDA')
for n in result.consola:
    print(n)

print('#### ERRORES EJECUCION DE CODIGO')
for n in result.errores:
    print(n)


# print('#### CODIGO AST')
# gv = GraficoDot()
# entorno.graficar(gv,None)
# print(gv.get_dot())

print('#### TABLA DE SIMBOLOS')
#print(result.entornos_variables)

tabla_de_simbolos = []

#FORMATO PARA INGRESAR LA INFORMACION AL DICCIONARIO
#{'nombre': value , 'clase': value , 'tipo': value , 'ambito': value ,'fila':value , 'columna': value}
for key in result.entornos_variables:
    if result.entornos_variables[key].tipo != 'Global':
        result.entornos_variables[key].tipo = 'Local'
    diccionario_vars = result.entornos_variables[key].variables.get_diccionario()
    diccionario_funciones = result.entornos_variables[key].funciones.get_diccionario()
    diccionario_estructuras = result.entornos_variables[key].estructuras.get_diccionario()
    for key2 in diccionario_vars:
        variable = diccionario_vars[key2] 
        tabla_de_simbolos.append({'nombre': variable.id , 'clase': 'Variable' , 'tipo': variable.tipo.value , 'ambito': result.entornos_variables[key].tipo ,'linea':variable.linea , 'columna': variable.columna})
    for key2 in diccionario_funciones:
        variable = diccionario_funciones[key2] 
        tabla_de_simbolos.append({'nombre': variable.id , 'clase': 'Funcion' , 'tipo': variable.tipo.value , 'ambito': result.entornos_variables[key].tipo ,'linea':variable.linea , 'columna': variable.columna})
    for key2 in diccionario_estructuras:
        variable = diccionario_estructuras[key2] 
        tabla_de_simbolos.append({'nombre': variable.id , 'clase': 'Estructura' , 'tipo': variable.tipo.value , 'ambito': result.entornos_variables[key].tipo ,'linea':variable.linea , 'columna': variable.columna})
    
    
for simbolos in tabla_de_simbolos:
    print(simbolos)
