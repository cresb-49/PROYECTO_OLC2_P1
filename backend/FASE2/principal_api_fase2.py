import pyTypeParser as parser
from pyTypeParser import Scope
from pyTypeParser import TipoEnum
# from pyTypeParser import Sentencias
from pyTypeParser import Resultado
from pyTypeParser import resultado
from Instrucciones.entorno import Entorno
from Modulos.grafico_dot import GraficoDot
from Symbol.generador import Generador

import ply.yacc as yacc


class PrincipalFase2:
    def leer(self, codigo):
        # Clases y metodos para la generacion de codigo en 3 direcciones
        gen_aux = Generador()
        gen_aux.clean_all()  # Limpia todos los archivos anteriores
        generador = gen_aux.get_instance()

        # Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
        codigo = codigo + '\n'

        # print('#### CODIGO A PROCESAR\n', codigo)
        print('#### PARSER FASE 2 EJECUTADO')
        result: Resultado = parser.parse(codigo)
        if result != None:
            print('#### PARSER FASE 2 FINALIZADO')
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

            if len(result.errores) == 0:
                print('#### EJECUCION DEL CODIGO FASE 2')
                entorno.ejecutar(None)
            else:
                print('#### NO SE PUEDE EJECUTAR EL CODIGO HAY ERRORES')

            print('#### CONSOLA DE SALIDA FASE 2')
            for n in result.consola:
                print(n)

            print('#### ERRORES EJECUCION DE CODIGO FASE 2')
            for n in result.errores:
                print(n)

            codigo_3_direcciones = ""

            if len(result.errores) == 0:
                # GENERACION DEL CODIGO 3 DIRECCIONES EN GO
                ambito_global.size = 0
                entorno.generar_c3d(None)
                codigo_3_direcciones = generador.get_code()
                # print('#### CODIGO 3 DIRECCIONES\n', codigo_3_direcciones)
            else:
                result.consola = []
            respuesta = {"result": result, "c3d": codigo_3_direcciones}
            return respuesta
        else:
            print(resultado.errores)
            resultado.add_error(
                'Sintactico', 'Existe un error al final del archivo', 0, 0)
            respuesta = {"result": resultado, "c3d": ''}
            return respuesta
