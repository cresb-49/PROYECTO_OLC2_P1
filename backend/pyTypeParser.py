from Nativas.split import Split
from Nativas.to_fixed import ToFixed
from Nativas.to_exponential import ToExponential
import ply.yacc as yacc  # Import de yacc para generar el analizador sintactico
from pyTypeLex import lexer  # Import del lexer realizado por el usuario
# Import de los tokens del lexer, es necesario por tenerlo en archivos separados
from pyTypeLex import tokens
from ply.lex import LexToken

# Seccion para importar las abstracciones y ED para verificar la infomacion
from ED.Pila import Pila
from pyTypeLex import find_column
from pyTypeLex import resultado
from Models.resultado import Resultado
from Instrucciones.sentencias import Scope
from Symbol.tipoEnum import TipoEnum
# Clases referentes a las expreciones
from Expresiones.acceder import Abstract
from Expresiones.acceder import Acceder
from Expresiones.aritmetica import Aritmetica
from Expresiones.logico import Logico
from Expresiones.primitivo import Primitivo
from Expresiones.relacional import Relacional
from Expresiones.arreglo import Arreglo
from Expresiones.acceder_array import AccederArray
from Expresiones.val_funcion import ValFuncion

from Nativas.concat import Concat
from Nativas.to_string import ToString
from Nativas.to_lower import ToLowerCase
from Nativas.to_upper import ToUpperCase
from Nativas.concat import Concat
# Clases referentes a las intrucciones
from Instrucciones.asignacion import Asignacion
from Instrucciones.asignar_array import AsignacionArray
from Instrucciones.callFuncion import CallFuncion
from Instrucciones.declaracion import Declaracion

from Instrucciones.instr_error import IntruccionError

# from Instrucciones.continuar import Continuar
# from Instrucciones.detener import Detener
# from Instrucciones.retornar import Retornar

from Instrucciones.sentencias import Sentencias

from Instrucciones.sentencias import Continuar
from Instrucciones.sentencias import Detener
from Instrucciones.sentencias import Retornar

from Instrucciones.funcion import Funcion
from Instrucciones.imprimir import Imprimir
from Instrucciones.mientras import Mientras
from Instrucciones.para import Para
from Instrucciones.si import Si
from Instrucciones.si_contrario import SiContrario
from Instrucciones.contrario import Contrario

# Inicio de la gramatica

memoria = Pila()
contador = 0
registro = []

# Memoria para entornos con nombres
memoria_entornos_intrucciones_interrupcion = Pila()
ESPACIO_GLOBAL = 'GLOBAL'
ESPACIO_FUNCION = 'FUNCION'
ESPACIO_CICLO = 'CICLO'
ESPACIO_SENTENCIA = 'SENTENCIA'
INS_RETURN = 'RETURN'
INS_BREAK = 'BREAK'
INS_CONTINUE = 'CONTINUE'


def set_memoria_funcion():
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_FUNCION)


def validar_interrupciones():
    # print('Parser en linea 78 -> ', 'Validacion de Interrupciones')
    # print(memoria_entornos_intrucciones_interrupcion.items)
    # Divicion de toda la memoria hasta arreglos pequenos
    general = []
    tmp = []
    for elemento in memoria_entornos_intrucciones_interrupcion.items:
        if elemento == ESPACIO_GLOBAL:
            tmp.append(elemento)
            p = Pila()
            p.items = list(reversed(invertir_solo_abstractos(tmp)))
            general.append(p)
            tmp = []
        else:
            tmp.append(elemento)

    for pila_sentencias in general:
        if isinstance(pila_sentencias, Pila):
            while pila_sentencias.obtener_tamanio() != 0:
                top = pila_sentencias.obtener_tope()
                if isinstance(top, Retornar):
                    if not pila_sentencias.existe_elemento_abajo_arriba(ESPACIO_FUNCION):
                        resultado.add_error(
                            'Semantico', 'No puede agregar un "return" si no esta contenido en una funcion', top.linea, top.columna)
                        print(
                            'Semantico', 'No puede agregar un "return" si no esta contenido en una funcion', top.linea, top.columna)
                        pila_sentencias.desapilar()
                    else:
                        pila_sentencias.desapilar()
                        # Debemos de verificar si hay otro return en la pila despues de una sentencia
                        verificacion_codigo_basura_return(
                            pila_sentencias, top, 'return')
                elif isinstance(top, Continuar):
                    if not pila_sentencias.existe_elemento_arriba_abajo(ESPACIO_CICLO):
                        resultado.add_error(
                            'Semantico', 'No puede agregar un "continue" si no esta contenido en un ciclo for o while', top.linea, top.columna)
                        print(
                            'Semantico', 'No puede agregar un "continue" si no esta contenido en un ciclo for o while', top.linea, top.columna)
                        pila_sentencias.desapilar()
                    else:
                        pila_sentencias.desapilar()
                        # Debemos de verificar si hay otro return en la pila despues de una sentencia
                        verificacion_codigo_basura_return(
                            pila_sentencias, top, 'continue')
                elif isinstance(top, Detener):
                    if not pila_sentencias.existe_elemento_arriba_abajo(ESPACIO_CICLO):

                        resultado.add_error(
                            'Semantico', 'No puede agregar un "break" si no esta contenido en un ciclo for o while', top.linea, top.columna)
                        print(
                            'Semantico', 'No puede agregar un "break" si no esta contenido en un ciclo for o while', top.linea, top.columna)
                        pila_sentencias.desapilar()
                    else:
                        pila_sentencias.desapilar()
                        # Debemos de verificar si hay otro return en la pila despues de una sentencia
                        verificacion_codigo_basura_return(
                            pila_sentencias, top, 'break')
                else:
                    pila_sentencias.desapilar()


def verificacion_codigo_basura_return(pila: Pila, inst: Abstract, nombre):
    if pila.existe_elemento_arriba_abajo(ESPACIO_SENTENCIA):
        instrucciones = pila.obtener_elementos_arriba_abajo_hasta(
            ESPACIO_SENTENCIA)
        for ins in instrucciones:
            # print('ccc', ins)
            if isinstance(ins, Abstract):
                resultado.add_error(
                    'Semantico', f'El "{nombre}" nunca se ejecutara', inst.linea, inst.columna)
                resultado.add_error(
                    'Semantico', f'Las instrucciones contenidas en el bloque que empieza en la linea: {ins.linea+1} no se ejecutaran debido a hay una instruccion de interrupcion que le precede', inst.linea, inst.columna)
                break
    else:
        instrucciones = pila.obtener_elementos_arriba_abajo_hasta(
            ESPACIO_CICLO)
        if instrucciones != None:
            for ins in instrucciones:
                # print('ccc', ins)
                if isinstance(ins, Abstract):
                    resultado.add_error(
                        'Semantico', f'El "{nombre}" nunca se ejecutara', inst.linea, inst.columna)
                    resultado.add_error(
                        'Semantico', f'Las instrucciones contenidas en el bloque que empieza en la linea: {ins.linea+1} no se ejecutaran debido a hay una instruccion de interrupcion que le precede', inst.linea, inst.columna)
                    break
        else:
            instrucciones = pila.obtener_elementos_arriba_abajo_hasta(
                ESPACIO_GLOBAL)
            for ins in instrucciones:
                # print('ccc', ins)
                if isinstance(ins, Abstract):
                    resultado.add_error(
                        'Semantico', f'El "{nombre}" nunca se ejecutara', inst.linea, inst.columna)
                    resultado.add_error(
                        'Semantico', f'Las instrucciones contenidas en el bloque que empieza en la linea: {ins.linea+1} no se ejecutaran debido a hay una instruccion de interrupcion que le precede', inst.linea, inst.columna)
                    break


def invertir_solo_abstractos(items) -> list:
    result = []
    tmp = []
    for item in items:
        if isinstance(item, Abstract):
            tmp.append(item)
        else:
            if len(tmp) == 0:
                result.append(item)
            else:
                result.extend(list(reversed(tmp)))
                tmp = []
                result.append(item)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@')
    # for item in result:
    #     print(item)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@')
    return result


def decla_var_fun(instruccion):
    if isinstance(instruccion, Declaracion):
        scope: Scope = memoria.obtener_tope()
        tipo_secundario = instruccion.tipo_secundario
        try:
            scope.declarar_variable(instruccion.id, None, instruccion.tipo,
                                    tipo_secundario, instruccion.linea, instruccion.columna)
        except ValueError as error:
            resultado.add_error('Semantico', str(
                error), instruccion.linea, instruccion.columna)
            print(str(error))
    if isinstance(instruccion, Funcion):
        scope: Scope = memoria.obtener_tope()
        try:
            scope.declarar_funcion(instruccion.id, instruccion)
        except ValueError as error:
            resultado.add_error('Semantico', str(
                error), instruccion.linea, instruccion.columna)
            print(str(error))


def p_init(p):
    """init : limit_intrucciones"""
    memoria.desapilar()
    resultado.sentencias = p[1]
    resultado.tabla_simbolos = registro
    p[0] = resultado
    validar_interrupciones()

# Intrucciones limitadas solo al ambito global


def p_limit_intrucciones(p):
    """limit_intrucciones : limit_intrucciones limit_intruccion"""
    # Limites de verificacion
    print('Regreso a Entorno Global')
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_GLOBAL)
    sent: Sentencias = p[1]
    sent.instr_derecha = p[2]
    sentencias: Sentencias = Sentencias(resultado, 0, 0, sent, None)
    decla_var_fun(p[2])
    p[0] = sentencias


def p_limit_intrucciones_2(p):
    """limit_intrucciones : limit_intruccion"""
    sentencias = Sentencias(resultado, 0, 0, p[1], None)
    # sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    # Aqui es donde se inicializa el scope global, este es el scope 0
    print('Generacion Entorno Global')
    entorno = Scope(memoria.obtener_tope())
    entorno.tipo = 'Global'
    memoria.apilar(entorno)
    registro.append(entorno)
    decla_var_fun(p[1])
    # Limites de verificacion
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_GLOBAL)


# ESTA PRODUCCION ES PARA INTRUCCIONES SOLO PARA EL AMBITO GLOBAL
def p_limit_intruccion(p):
    """limit_intruccion : instruccion
                        | funcion"""
    p[0] = p[1]

# Intrucciones que pueden estar dentro de sentencias de control, no podemos
# declarar funciones dentro de las sentencias de control


def p_instrucciones(p):
    """instrucciones : instrucciones instruccion"""
    sent: Sentencias = p[1]
    sent.instr_derecha = p[2]
    # sentencias.intrucciones.append(p[2])
    sentencias: Sentencias = Sentencias(resultado, 0, 0, sent, None)
    decla_var_fun(p[2])
    p[0] = sentencias


def p_instrucciones_2(p):
    """instrucciones : instruccion"""
    sentencias = Sentencias(resultado, 0, 0, p[1], None)
    # sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    # Aqui es donde se inicializa un scope local, crear una pila para numerar los scopes
    print('Generacion Entorno Local')
    entorno = Scope(memoria.obtener_tope())
    entorno.tipo = 'Local'
    memoria.apilar(entorno)
    registro.append(entorno)
    decla_var_fun(p[1])


def p_instruccion(p):
    """instruccion : print
                   | struct
                   | llamar_funcion
                   | declaracion
                   | asignar_array
                   | asignacion
                   | interrupcion_funcion
                   | interrupcion_ciclo"""
    p[0] = p[1]

def p_asignar_array(p):
    """asignar_array : sub_array LBRA exprecion RBRA IGUAL exprecion SEMICOLON"""
    p[0] = AsignacionArray(resultado, p.lineno(5), find_column(input, p.slice[5]),p[1],p[3],p[6])
    
def p_sub_array(p):
    """sub_array : sub_array LBRA exprecion RBRA
                 | ID """
    if len(p) == 2:
        p[0] = Acceder(resultado,p.lineno(1),find_column(input,p.slice[1]),p[1])
    else:
        p[0] = AccederArray(resultado,p.lineno(2),find_column(input,p.slice[2]),p[1],p[3])


def p_instruccion_2(p):
    """instruccion : ciclo_for
                   | ciclo_while"""
    p[0] = p[1]


def p_instruccion_3(p):
    """instruccion : error"""  # produccion de error
    p[0] = IntruccionError(resultado, p.lineno(
        1), find_column(input, p.slice[1]))


def p_instruccion_4(p):
    """instruccion : condicional_if"""
    p[0] = p[1]


def p_interrupcion_ciclo(p):
    """interrupcion_ciclo : continuar"""
    memoria_entornos_intrucciones_interrupcion.apilar(p[1])
    p[0] = p[1]


def p_interrupcion_ciclo_2(p):
    """interrupcion_ciclo : romper"""
    memoria_entornos_intrucciones_interrupcion.apilar(p[1])
    p[0] = p[1]


def p_interrupcion_funcion(p):
    """interrupcion_funcion : retorno"""
    memoria_entornos_intrucciones_interrupcion.apilar(p[1])
    p[0] = p[1]

# Intrucion console.log


def p_print(p):
    """print : CONSOLE DOT ID LPAR exprecion RPAR SEMICOLON"""
    p[0] = Imprimir(resultado, p.lineno(
        1), find_column(input, p.slice[1]), p[5])

# Instruccion continue


def p_continuar(p):
    """continuar : CONTINUE SEMICOLON"""
    p[0] = Continuar(resultado, p.lineno(1), find_column(input, p.slice[1]))

# Instruccion break


def p_romper(p):
    """romper : BREAK SEMICOLON"""
    p[0] = Detener(resultado, p.lineno(1), find_column(input, p.slice[1]))


# Instruccion return


def p_retorno(p):
    """retorno : RETURN SEMICOLON
               | RETURN exprecion SEMICOLON"""
    if len(p) == 3:
        p[0] = Retornar(resultado, p.lineno(
            1), find_column(input, p.slice[1]), None)
    else:
        p[0] = Retornar(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[2])
# Producciones de la intruccion for


def p_ciclo_for(p):
    """ciclo_for : FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY RKEY
                 | FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY instrucciones RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY instrucciones RKEY"""
    # Apilamos la instruccion ciclo para verificacion
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_CICLO)
    # Debemos de verificar primiero que tipo de derivacion es
    if p[5] == 'of':
        # For de tipo iterable
        # Verificacion que produccion tenga instrucciones
        if len(p) == 11:
            # Es un for con instrucciones debemos de apilar el scope implicio del mismo y colocar la referencia al que ya esta
            declarar: Declaracion = Declaracion(resultado, p.lineno(
                3), find_column(input, p.slice[3]), p[4], TipoEnum.ANY, None, None)
            manejo_for_pila(declarar, True)
            p[0] = Para(resultado, p.lineno(1), find_column(
                input, p.slice[1]), 2, declarar, None, p[6], p[9])
        else:
            # Es un for sin intrucciones generamos un scope simple declaramos variable del for y hacemos un pop nuevamente
            declarar: Declaracion = Declaracion(resultado, p.lineno(
                3), find_column(input, p.slice[3]), p[4], TipoEnum.ANY, None, None)
            manejo_for_pila(declarar, False)
            p[0] = Para(resultado, p.lineno(1), find_column(
                input, p.slice[1]), 2, declarar, None, p[6], None)
    else:
        # For de tipo index
        # Verificamos que la produccion tenga instrucciones
        if len(p) == 12:
            # Es un for con instrucciones debemos de apilar el scope implicio del mismo y colocar la referencia al que ya esta
            manejo_for_pila(p[3], True)
            p[0] = Para(resultado, p.lineno(1), find_column(
                input, p.slice[1]), 1, p[3], p[5], p[7], p[10])
        else:
            # Es un for sin intrucciones generamos un scope simple declaramos variable del for y hacemos un pop nuevamente
            manejo_for_pila(p[3], False)
            p[0] = Para(resultado, p.lineno(1), find_column(
                input, p.slice[1]), 1, p[3], p[5], p[7], None)


def manejo_for_pila(declarar, desapilar: bool):
    if desapilar:
        scope: Scope = memoria.desapilar()
        anterior = scope.anterior
        scope_interior_for: Scope = Scope(anterior)
        scope_interior_for.tipo = 'Local'
        registro.pop()
        registro.append(scope_interior_for)
        registro.append(scope)
        scope.anterior = scope_interior_for
        memoria.apilar(scope_interior_for)
        decla_var_fun(declarar)
        memoria.desapilar()
    else:
        scope_anterior = memoria.obtener_tope()
        scope_interior_for: Scope = Scope(scope_anterior)
        scope_interior_for.tipo = 'Local'
        registro.append(scope_interior_for)
        memoria.apilar(scope_interior_for)
        decla_var_fun(declarar)
        memoria.desapilar()


def p_declaracion_for(p):
    """declaracion_for : LET ID COLON tipo IGUAL exprecion
                       | LET ID IGUAL exprecion
    """
    if (p[3] == ':'):
        p[0] = Declaracion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[4]['tipo'], p[4]['tipo_secundario'], p[6])
    else:
        p[0] = Declaracion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], TipoEnum.ANY, None, p[4])


def p_declaracion_for_2(p):
    """declaracion_for : ID IGUAL exprecion"""
    p[0] = Asignacion(resultado, p.lineno(
        1), find_column(input, p.slice[1]), p[1], p[3])


def p_sumador(p):
    """sumador : ID SUM"""
    acc: Acceder = Acceder(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[1])
    pri: Primitivo = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NUMBER, 1)
    arit: Aritmetica = Aritmetica(resultado, p.lineno(1), find_column(
        input, p.slice[1]), acc, pri, '+')
    asig: Asignacion = Asignacion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[1], arit)
    p[0] = asig


def p_sumador_2(p):
    """sumador : ID RES"""
    acc: Acceder = Acceder(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[1])
    pri: Primitivo = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NUMBER, 1)
    arit: Aritmetica = Aritmetica(resultado, p.lineno(1), find_column(
        input, p.slice[1]), acc, pri, '-')
    asig: Asignacion = Asignacion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[1], arit)
    p[0] = asig

# Producciones de la intruccion if


def p_condicional_if(p):
    """condicional_if : si_continuacion_if continuacion_if"""
    print('Si con else')
    heredado: SiContrario = p[1]['heredado']
    if heredado == None:
        base: Si = p[1]['base']
        base._else = p[2]
    else:
        heredado.sentencias_false = p[2]
    p[0] = p[1]['base']


def p_condicional_if2(p):
    """condicional_if : si_continuacion_if"""
    print('Si con else if')
    # print(p[1])
    p[0] = p[1]['base']


def p_si_continuacion_if(p):
    """si_continuacion_if : si_continuacion_if ELSE IF LPAR exprecion RPAR LKEY instrucciones RKEY
                          | si_continuacion_if ELSE IF LPAR exprecion RPAR LKEY RKEY
                          | if_simple"""
    if len(p) == 10:
        print('Si else con instrucciones')
        memoria.desapilar()
        heredado = SiContrario(resultado, p.lineno(
            2), find_column(input, p.slice[2]), p[5], None, None)
        p[0] = manejo_if(p, heredado, p[8])
    elif len(p) == 9:
        print('Si else sin instrucciones')
        heredado = SiContrario(resultado, p.lineno(
            2), find_column(input, p.slice[2]), p[5], None, None)
        p[0] = manejo_if(p, heredado, None)
    else:
        p[0] = {'base': p[1], 'heredado': None}
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_SENTENCIA)


def manejo_if(p, heredado: SiContrario, instrucciones):
    heredado.sentencias_true = instrucciones
    if p[1]['heredado'] == None:
        base: Si = p[1]['base']
        base._else = heredado
        return {'base': p[1]['base'], 'heredado': heredado}
    else:
        si_contrario: SiContrario = p[1]['heredado']
        si_contrario.sentencias_false = heredado
        return {'base': p[1]['base'], 'heredado': heredado}


def p_base_if(p):
    """if_simple : IF LPAR exprecion RPAR LKEY RKEY
                 | IF LPAR exprecion RPAR LKEY instrucciones RKEY"""
    if len(p) == 8:
        print('Si con instrucciones')
        memoria.desapilar()
        p[0] = Si(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[3], p[6], None)
    else:
        print('Si sin instrucciones')
        p[0] = Si(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[3], None, None)
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_SENTENCIA)


def p_continuacion_if(p):
    """continuacion_if : ELSE LKEY RKEY
                       | ELSE LKEY instrucciones RKEY"""
    if len(p) == 5:
        print('Else con intrucciones')
        memoria.desapilar()
        p[0] = Contrario(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[3])
    else:
        print('Else sin instrucciones')
        p[0] = Contrario(resultado, p.lineno(
            1), find_column(input, p.slice[1]), None)
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_SENTENCIA)

# Declaracion de un struct


def p_struct(p):
    """struct : INTERFACE ID LKEY valores RKEY"""

# Declarion del interior de la interfaz del programa


def p_valores(p):
    """valores : ID COLON tipo SEMICOLON
               | valores ID COLON tipo SEMICOLON"""

# Intruccion de llamado de funcion


def p_llamar_funcion(p):
    """llamar_funcion : ID LPAR RPAR SEMICOLON
                      | ID LPAR parametros RPAR SEMICOLON"""
    if len(p) == 5:
        p[0] = CallFuncion(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[1], None)
    else:
        p[0] = CallFuncion(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[1], p[3])

# Parametros de llamado de funcion o metodo


def p_parametros(p):
    """parametros : parametros COMMA exprecion"""
    params: list = p[1]
    params.append(p[3])
    p[0] = params


def p_parametros_2(p):
    """parametros : exprecion"""
    params = [p[1]]
    p[0] = params

# Ciclo while de un funcion


def p_ciclo_while(p):
    """ciclo_while : WHILE LPAR exprecion RPAR LKEY RKEY
                   | WHILE LPAR exprecion RPAR LKEY instrucciones RKEY"""
    # Apilamos la instruccion ciclo para verificacion
    memoria_entornos_intrucciones_interrupcion.apilar(ESPACIO_CICLO)
    if len(p) == 7:
        p[0] = Mientras(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[3], None)
    else:
        memoria.desapilar()
        p[0] = Mientras(resultado, p.lineno(
            1), find_column(input, p.slice[1]), p[3], p[6])

# Declaracion de una funcion


def p_funcion(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY RKEY 
               | FUNCTION ID LPAR RPAR COLON tipo LKEY RKEY"""
    # memoria.desapilar()
    if p[5] == ":":
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[6]['tipo'], p[6]['tipo_secundario'], None, None)
    else:
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], TipoEnum.ANY, None, None, None)
    set_memoria_funcion()


def p_funcion_2(p):
    """funcion : FUNCTION ID LPAR lista_parametros RPAR LKEY RKEY
               | FUNCTION ID LPAR lista_parametros RPAR COLON tipo LKEY RKEY"""
    # memoria.desapilar()
    if p[6] == ":":
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[7]['tipo'], p[7]['tipo_secundario'], p[4], None)
    else:
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], TipoEnum.ANY, None, p[4], None)
    set_memoria_funcion()


def p_funcion_3(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY instrucciones RKEY
               | FUNCTION ID LPAR RPAR COLON tipo LKEY instrucciones RKEY"""
    memoria.desapilar()
    if p[5] == ":":
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[6]['tipo'], p[6]['tipo_secundario'], None, p[8])
    else:
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], TipoEnum.ANY, None, None, p[6])
    set_memoria_funcion()


def p_funcion_4(p):
    """funcion : FUNCTION ID LPAR lista_parametros RPAR LKEY instrucciones RKEY
               | FUNCTION ID LPAR lista_parametros RPAR COLON tipo LKEY instrucciones RKEY"""
    memoria.desapilar()
    if p[6] == ":":
        # Funcion con tipo
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[7]['tipo'], p[7]['tipo_secundario'], p[4], p[9])
    else:
        p[0] = Funcion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[2], TipoEnum.ANY, None, p[4], p[7])
    set_memoria_funcion()

# Seccion de declaracion de parametros de una funcion


def p_lista_parametros(p):
    """lista_parametros : lista_parametros COMMA variable_funcion"""
    lista_def_params: list = p[1]
    lista_def_params.append(p[3])
    p[0] = lista_def_params


def p_lista_parametros_2(p):
    """lista_parametros : variable_funcion"""
    lista_def_params: list = []
    lista_def_params.append(p[1])
    p[0] = lista_def_params


def p_variables_funcion(p):
    """variable_funcion : ID COLON tipo
                        | ID"""
    if len(p) == 4:
        b: dict = p[3]
        decla: Declaracion = Declaracion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[1], b['tipo'], b['tipo_secundario'], None)
        p[0] = decla
    else:
        decla: Declaracion = Declaracion(resultado, p.lineno(1), find_column(
            input, p.slice[1]), p[1], TipoEnum.ANY, None, None)
        p[0] = decla

# instruccion de declaracion de variables


def p_declaracion(p):
    """declaracion : LET ID COLON tipo IGUAL exprecion SEMICOLON"""
    b: dict = p[4]
    p[0] = Declaracion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[2], b['tipo'], b['tipo_secundario'], p[6])


def p_declaracion_2(p):
    """declaracion : LET ID IGUAL exprecion SEMICOLON"""
    p[0] = Declaracion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[2], TipoEnum.ANY, None, p[4])


def p_declaracion_3(p):
    """declaracion : LET ID COLON tipo SEMICOLON"""
    b: dict = p[4]
    p[0] = Declaracion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[2], b['tipo'], b['tipo_secundario'], None)


def p_declaracion_4(p):
    """declaracion : LET ID SEMICOLON"""
    p[0] = Declaracion(resultado, p.lineno(1), find_column(
        input, p.slice[1]), p[2], TipoEnum.ANY, None, None)

# Instruccion de asignacion


def p_asignacion(p):
    """asignacion : ID IGUAL exprecion SEMICOLON"""
    p[0] = Asignacion(resultado, p.lineno(
        1), find_column(input, p.slice[1]), p[1], p[3])

# Producciones referentes al tipo de dato


def p_tipo(p):
    """tipo : base
            | base LBRA RBRA"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        b: dict = p[1]
        tipo_heredado = b['tipo']
        b['tipo_secundario'] = tipo_heredado.value
        b['tipo'] = TipoEnum.ARRAY
        p[0] = b


def p_base(p):
    """base : NUMBER
            | ANY
            | BOOLEAN
            | STRING
            | ID"""

    if (p[1] == 'number'):
        p[0] = {"tipo": TipoEnum.NUMBER, "tipo_secundario": None}
    elif (p[1] == 'any'):
        p[0] = {"tipo": TipoEnum.ANY, "tipo_secundario": None}
    elif (p[1] == 'boolean'):
        p[0] = {"tipo": TipoEnum.BOOLEAN, "tipo_secundario": None}
    elif (p[1] == 'string'):
        p[0] = {"tipo": TipoEnum.STRING, "tipo_secundario": None}
    else:
        p[0] = {"tipo": TipoEnum.STRUCT, "tipo_secundario": p[1]}


# Asociación de operadores y precedencia anterior
# precedence = (
#    ('left', 'OR'),
#    ('left', 'AND'),
#    ('left', 'NOT'),
#    ('nonassoc', 'MAQ', 'MEQ', 'MAIQ', 'MEIQ', 'EQ', 'NEQ'),
#    ('left', 'MAS', 'MENOS'),
#    ('left', 'MULT', 'DIV', 'MOD'),
#    ('right', 'UMINUS'),  # Operador unario
#    ('right', 'POTENCIA'),
# )

# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'MAQ', 'MEQ', 'MAIQ', 'MEIQ'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'POTENCIA'),
    ('right', 'UMINUS'),  # Operador unario
)
# ('left', 'LPAR', 'RPAR'), #Precedencia de parentesis

# Expreciones -> operaciones entre variables, constantes, funciones y metodos


def p_exprecion(p):
    """exprecion : MENOS exprecion %prec UMINUS"""
    izquiera = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NUMBER, -1)
    p[0] = Aritmetica(resultado, p.lineno(1), find_column(
        input, p.slice[1]), izquiera, p[2], '*')


def p_exprecion_2(p):
    """exprecion : exprecion MAS exprecion
                 | exprecion MENOS exprecion
                 | exprecion MULT exprecion
                 | exprecion DIV exprecion
                 | exprecion POTENCIA exprecion
                 | exprecion MOD exprecion"""
    p[0] = Aritmetica(resultado, p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[2])


def p_exprecion_3(p):
    """exprecion : exprecion MAQ exprecion
                 | exprecion MEQ exprecion
                 | exprecion MAIQ exprecion
                 | exprecion MEIQ exprecion
                 | exprecion NEQ exprecion
                 | exprecion EQ exprecion"""
    p[0] = Relacional(resultado, p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[2])


def p_exprecion_4(p):
    """exprecion : exprecion OR exprecion
                 | exprecion AND exprecion"""
    p[0] = Logico(resultado, p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[2])


def p_exprecion_5(p):
    """exprecion : NOT exprecion"""
    p[0] = Logico(resultado, p.lineno(1), find_column(
        input, p.slice[1]), None, p[2], p[1])


def p_exprecion_6(p):
    """exprecion : sub_exprecion"""
    p[0] = p[1]

# Valores atomicos es decir, el valor de una variable, constante o resultado de una
# funcion o metodo


def p_sub_exprecion(p):
    """sub_exprecion : LPAR exprecion RPAR"""
    p[0] = p[2]


def p_sub_exprecion_2(p):
    """sub_exprecion : NULL"""
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NULL, None)


def p_sub_exprecion_3(p):
    """sub_exprecion : NUM"""
    result = 0
    try:
        result = float(p[1])
    except ValueError:
        print("Float value too large %d", p[1])
        resultado.add_error('Sintanctico', ("Float value too large %d", p[1]), p.lineno(1), find_column(
            input, p.slice[1]))
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NUMBER, result)


def p_sub_exprecion_4(p):
    """sub_exprecion : FLOAT"""
    result = 0
    try:
        result = float(p[1])
    except ValueError:
        print("Float value too large %d", p[1])
        resultado.add_error('Sintanctico', ("Float value too large %d", p[1]), p.lineno(1), find_column(
            input, p.slice[1]))
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.NUMBER, result)


def p_sub_exprecion_5(p):
    """sub_exprecion : STR"""
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]),  TipoEnum.STRING, p[1])


def p_sub_exprecion_6(p):
    """sub_exprecion : STRCS"""
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]),  TipoEnum.STRING, p[1])


def p_sub_exprecion_7(p):
    """sub_exprecion : TRUE"""
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.BOOLEAN, True)


def p_sub_exprecion_8(p):
    """sub_exprecion : FALSE"""
    p[0] = Primitivo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.BOOLEAN, False)


def p_sub_exprecion_9(p):
    """sub_exprecion : LBRA exp_array RBRA"""
    p[0] = Arreglo(resultado, p.lineno(1), find_column(
        input, p.slice[1]), TipoEnum.ARRAY, None, p[2])


def p_exp_array(p):
    """exp_array : exp_array COMMA exprecion"""
    lista: list = p[1]
    lista.append(p[3])
    p[0] = lista


def p_exp_array_2(p):
    """exp_array : exprecion"""
    lista: list = []
    lista.append(p[1])
    p[0] = lista


def p_sub_exprecion_10(p):
    """sub_exprecion : ID"""
    p[0] = Acceder(resultado, p.lineno(
        1), find_column(input, p.slice[1]), p[1])


def p_sub_exprecion_11(p):
    """sub_exprecion : exprecion LBRA exprecion RBRA"""
    p[0] = AccederArray(resultado, p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3])


def p_sub_exprecion_12(p):
    """sub_exprecion : ID LPAR RPAR
                     | ID LPAR parametros RPAR
                     | ID DOT ID
                     | ID DOT ID LPAR RPAR
                     | ID DOT ID LPAR exprecion RPAR"""
    if (p[2] == '('):
        if p[3] == ')':
            p[0] = ValFuncion(resultado, p.lineno(1), find_column(
                input, p.slice[1]), p[1], [])
        else:
            if p[1] == 'String':
                # Funcion nativa string
                print('Hacer funcion nativa String(val)')
            else:
                p[0] = ValFuncion(resultado, p.lineno(
                    1), find_column(input, p.slice[1]), p[1], p[3])
    elif (p[2] == '.'):
        if (len(p) == 6):

            if (p[3] == 'toString'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = ToString(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder)
            elif (p[3] == 'toLowerCase'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = ToLowerCase(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder)
            elif (p[3] == 'toUpperCase'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = ToUpperCase(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder)
        elif (len(p) == 7):
            if (p[3] == 'concat'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = Concat(resultado, p.lineno(
                    1), find_column(input, p.slice[1]), acceder, p[5])
            elif (p[3] == 'split'):
                acceder = Acceder(resultado, p.lineno(
                    1), find_column(input, p.slice[1]), p[1])
                p[0] = Split(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder, p[5])
            elif (p[3] == 'toFixed'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = ToFixed(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder, p[5])
            elif (p[3] == 'toExponential'):
                acceder = Acceder(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), p[1])
                p[0] = ToExponential(resultado, p.lineno(1), find_column(
                    input, p.slice[1]), acceder, p[5])

        print('Acceso a struct o funcion nativa')

# Definicion de error del analisis sintactico


def p_error(t):
    print('Error Parser p_error ->', t, type(t))
    print("Error sintáctico en '%s'" % t.value)
    if isinstance(t, LexToken):
        resultado.add_error(
            'Sintactico', "Error sintáctico en '%s'" % t.value,  t.lineno, 'n/a')
    else:
        resultado.add_error(
            'Sintactico', "Error sintáctico en '%s'" % t.value,  0, 0)


# Declaracion de inicio del parser
parser = yacc.yacc()

input = ''


def parse(ip):
    global input
    input = ip
    return parser.parse(ip)
