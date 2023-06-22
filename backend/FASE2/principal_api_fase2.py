# import pyTypeParser as parser
import FASE2.pyTypeParser2 as parser
from FASE2.pyTypeParser2 import Scope
from FASE2.pyTypeParser2 import TipoEnum
# from pyTypeParser import Sentencias
from FASE2.pyTypeParser2 import Resultado
from FASE2.pyTypeParser2 import resultado
from FASE2.Instrucciones.entorno import Entorno
from FASE2.Modulos.grafico_dot import GraficoDot
from FASE2.Symbol.generador import Generador


class PrincipalFase2:
    def leer(self, codigo):
        resultado = Resultado([], [])

        # Clases y metodos para la generacion de codigo en 3 direcciones
        gen_aux = Generador()
        gen_aux.clean_all()  # Limpia todos los archivos anteriores
        generador = gen_aux.get_instance()

        # Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
        codigo = codigo + '\n'

        # print('#### CODIGO A PROCESAR\n', codigo)
        print('#### PARSER FASE 2 EJECUTADO')
        parser.parse(codigo)
        lista_errores = parser.get_errores_parser_lexer()
        parser.clear_errores()
        print('Debuj errores ->', lista_errores)
        if len(lista_errores) == 0:
            result: Resultado = parser.get_resultado()
            print('Resultado',result)
            print('#### PARSER FASE 2 FINALIZADO')
            if result.tabla_simbolos != None:
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

            codigo_3_direcciones = ""

            if len(result.errores) == 0:
                # GENERACION DEL CODIGO 3 DIRECCIONES EN GO
                ambito_global.size = 0
                new_scope = Scope(None)
                new_scope.tipo = 'Global'
                entorno.generar_c3d(new_scope)
                codigo_3_direcciones = generador.get_code()
                # print('#### CODIGO 3 DIRECCIONES\n', codigo_3_direcciones)
            else:
                result.consola = []
            respuesta = {"result": result, "c3d": codigo_3_direcciones}
            return respuesta
        else:
            for error in lista_errores:
                resultado.errores.append(error)
            resultado.add_error('Sintactico', 'Existe un error al final del archivo', 0, 0)
            respuesta = {"result": resultado, "c3d": ''}
            return respuesta
