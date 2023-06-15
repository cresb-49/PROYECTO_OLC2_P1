import pyTypeParser as parser
from pyTypeParser import Scope
from pyTypeParser import TipoEnum
# from pyTypeParser import Sentencias
from pyTypeParser import Resultado
from Instrucciones.entorno import Entorno
from Modulos.grafico_dot import GraficoDot
from Symbol.generador import Generador

import ply.yacc as yacc


class Principal:
    def leer(self, codigo):
        # Clases y metodos para la generacion de codigo en 3 direcciones
        gen_aux = Generador()
        gen_aux.cleanAll()  # Limpia todos los archivos anteriores
        generador = gen_aux.getInstance()

        # Agregamos el ultimo salto de linea para evitar conflictos con los comentarios :D
        codigo = codigo + '\n'

        print('#### CODIGO A PROCESAR\n', codigo)
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

        if len(result.errores) == 0:
            print('#### EJECUCION DEL CODIGO')
            entorno.ejecutar(None)
        else:
            print('#### NO SE PUEDE EJECUTAR EL CODIGO HAY ERRORES')

        print('#### CONSOLA DE SALIDA')
        for n in result.consola:
            print(n)

        print('#### ERRORES EJECUCION DE CODIGO')
        for n in result.errores:
            print(n)

        tabla_de_simbolos = []
        code_dot = ""
        codigo_3_direcciones = ""

        if len(result.errores) == 0:
            print('#### TABLA DE SIMBOLOS')
            # FORMATO PARA INGRESAR LA INFORMACION AL DICCIONARIO
            # {'nombre': value , 'clase': value , 'tipo': value , 'ambito': value ,'fila':value , 'columna': value}
            for key in result.entornos_variables:
                if result.entornos_variables[key].tipo != 'Global':
                    result.entornos_variables[key].tipo = 'Local'
                diccionario_vars = result.entornos_variables[key].variables.get_diccionario(
                )
                diccionario_funciones = result.entornos_variables[key].funciones.get_diccionario(
                )
                diccionario_estructuras = result.entornos_variables[key].estructuras.get_diccionario(
                )
                for key2 in diccionario_vars:
                    variable = diccionario_vars[key2]
                    tabla_de_simbolos.append({'nombre': variable.id, 'clase': 'Variable', 'tipo': variable.tipo.value,
                                              'ambito': result.entornos_variables[key].tipo, 'linea': variable.linea, 'columna': variable.columna})
                for key2 in diccionario_funciones:
                    variable = diccionario_funciones[key2]
                    tabla_de_simbolos.append({'nombre': variable.id, 'clase': 'Funcion', 'tipo': variable.tipo.value,
                                              'ambito': result.entornos_variables[key].tipo, 'linea': variable.linea, 'columna': variable.columna})
                for key2 in diccionario_estructuras:
                    variable = diccionario_estructuras[key2]
                    tabla_de_simbolos.append({'nombre': variable.id, 'clase': 'Estructura', 'tipo': TipoEnum.STRUCT.value,
                                              'ambito': result.entornos_variables[key].tipo, 'linea': variable.linea, 'columna': variable.columna})
            for simbolos in tabla_de_simbolos:
                print(simbolos)
            # GENERACION DEL CODIGO DOT PARA REALZIAR EL GRAFICO DEL AST
            gv = GraficoDot()
            entorno.graficar(gv, None)
            code_dot = gv.get_dot()
            self.escribir_salida_dot(code_dot)
            codigo_3_direcciones = generador.get_code()
        else:
            result.consola = []

        respuesta = {"result": result, "dot": code_dot,"simbolos": tabla_de_simbolos, "c3d": codigo_3_direcciones}

        return respuesta

    def escribir_salida_dot(self, code):
        # Abrir el archivo en modo escritura
        archivo = open("salida_dot.txt", "w")
        # Escribir en el archivo
        archivo.write(code)
        # Cerrar el archivo
        archivo.close()
