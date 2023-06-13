import pyTypeParser as parser
from pyTypeParser import Scope
# from pyTypeParser import Sentencias
from pyTypeParser import Resultado
from Instrucciones.entorno import Entorno


def leer(codigo):
    # Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
    codigo = codigo + '\n'
    print('#### PARSER EJECUTADO')
    result: Resultado = parser.parse(codigo)
    print('#### PARSER FINALIZADO')
    ambito_global: Scope = None
    for n in result.tabla_simbolos:
        if isinstance(n, Scope):
            if n.tipo == 'Global':
                ambito_global = n

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
    return result
