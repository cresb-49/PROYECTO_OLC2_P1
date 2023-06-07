import ply.yacc as yacc  # Import de yacc para generar el analizador sintactico
from pyTypeLex import lexer  # Import del lexer realizado por el usuario
# Import de los tokens del lexer, es necesario por tenerlo en archivos separados
from pyTypeLex import tokens

# Seccion para importar las abstracciones y ED para verificar la infomacion
from ED.Pila import Pila
from pyTypeLex import find_column
from pyTypeLex import tabla_errores  # Impotado de la tabla de errores del lexer
from Models.resultado import Resultado
# from Symbol.scope import Scope
from Instrucciones.sentencias import Scope

# Clases referentes a las expreciones
from Expresiones.acceder import Acceder
from Expresiones.aritmetica import Aritmetica
from Expresiones.logico import Logico
from Expresiones.primitivo import Primitivo
from Expresiones.relacional import Relacional

# Clases referentes a las intrucciones
from Instrucciones.asignacion import Asignacion
from Instrucciones.callFuncion import CallFuncion
from Instrucciones.declaracion import Declaracion

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

# Inicio de la gramatica

memoria = Pila()
contador = 0
registro = []


def decla_var_fun(instruccion):
    if isinstance(instruccion, Declaracion):
        scope: Scope = memoria.obtener_tope()
        tipo_secundario = None
        scope.declarar_variable(instruccion.id, None, instruccion.tipo,tipo_secundario, instruccion.linea, instruccion.columna)
    if isinstance(instruccion, Funcion):
        scope: Scope = memoria.obtener_tope()
        scope.declarar_funcion(instruccion.id, instruccion)


def p_init(p):
    """init : limit_intrucciones"""
    memoria.desapilar()
    p[0] = Resultado(p[1], tabla_errores, registro)

# Intrucciones limitadas solo al ambito global


def p_limit_intrucciones(p):
    """limit_intrucciones : limit_intrucciones limit_intruccion"""
    sentencias: Sentencias = p[1]
    sentencias.intrucciones.append(p[2])
    decla_var_fun(p[2])
    p[0] = sentencias


def p_limit_intrucciones_2(p):
    """limit_intrucciones : limit_intruccion"""
    sentencias = Sentencias(0, 0, [])
    sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    print('Generacion Entorno Global')
    entorno = Scope(memoria.obtener_tope())
    entorno.tipo = 'Global'
    memoria.apilar(entorno)
    registro.append(entorno)
    decla_var_fun(p[1])
    # TODO: Aqui es donde se inicializa el scope global, este es el scope 0


def p_limit_intruccion(p):
    """limit_intruccion : instruccion
                        | funcion"""
    p[0] = p[1]

# Intrucciones que pueden estar dentro de sentencias de control, no podemos
# declarar funciones dentro de las sentencias de control


def p_instrucciones(p):
    """instrucciones : instrucciones instruccion"""
    sentencias: Sentencias = p[1]
    sentencias.intrucciones.append(p[2])
    decla_var_fun(p[2])
    p[0] = sentencias


def p_instrucciones_2(p):
    """instrucciones : instruccion"""
    sentencias = Sentencias(0, 0, [])
    sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    print('Generacion Entorno Local')
    entorno = Scope(memoria.obtener_tope())
    entorno.tipo = 'Local'
    memoria.apilar(entorno)
    registro.append(entorno)
    decla_var_fun(p[1])
    # TODO: Aqui es donde se inicializa un scope local, crear una pila para numerar los scopes


def p_instruccion(p):
    """instruccion : print
                   | ciclo_for
                   | ciclo_while
                   | condicional_if
                   | struct
                   | llamar_funcion
                   | declaracion
                   | asignacion
                   | continuar
                   | romper
                   | retorno"""
    p[0] = p[1]

# Intrucion console.log


def p_print(p):
    """print : CONSOLE DOT ID LPAR exprecion RPAR SEMICOLON"""
    p[0] = Imprimir(p.lineno(1), find_column(input, p.slice[1]), p[5])

# Instruccion continue


def p_continuar(p):
    """continuar : CONTINUE SEMICOLON"""
    p[0] = Continuar(p.lineno(1), find_column(input, p.slice[1]))
# Instruccion break


def p_romper(p):
    """romper : BREAK SEMICOLON"""
    p[0] = Detener(p.lineno(1), find_column(input, p.slice[1]))

# Instruccion return


def p_retorno(p):
    """retorno : RETURN SEMICOLON
               | RETURN exprecion SEMICOLON"""
    if len(p) == 3:
        p[0] = Retornar(p.lineno(1), find_column(input, p.slice[1]), None)
    else:
        p[0] = Retornar(p.lineno(1), find_column(input, p.slice[1]), p[2])
# Producciones de la intruccion for


def p_ciclo_for(p):
    """ciclo_for : FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY RKEY
                 | FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY instrucciones RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY instrucciones RKEY"""
    scope: Scope = memoria.desapilar()
    anterior = scope.anterior
    scope_interior_for: Scope = Scope(anterior)
    scope_interior_for.tipo = 'Local'
    registro.pop()
    registro.append(scope_interior_for)
    registro.append(scope)
    scope.anterior = scope_interior_for
    memoria.apilar(scope_interior_for)
    decla_var_fun(p[3])
    memoria.desapilar()
    p[0] = Para(p.lineno(1), find_column(
        input, p.slice[1]), 1, p[3], p[5], p[7], None)


def p_declaracion_for(p):
    """declaracion_for : LET ID COLON tipo IGUAL exprecion
                       | LET ID IGUAL exprecion 
    """
    if (p[3] == ':'):
        p[0] = Declaracion(p.lineno(1), find_column(
            input, p.slice[1]), p[2], p[4], p[6])
    else:
        p[0] = Declaracion(p.lineno(1), find_column(
            input, p.slice[1]), p[2], 'any', p[4])


def p_sumador(p):
    """sumador : ID SUM
               | ID RES"""

# Producciones de la intruccion if


def p_condicional_if(p):
    """condicional_if : IF LPAR exprecion RPAR LKEY RKEY
                      | IF LPAR exprecion RPAR LKEY instrucciones RKEY
                      | IF LPAR exprecion RPAR LKEY instrucciones RKEY continuacion_if
                      | IF LPAR exprecion RPAR LKEY RKEY continuacion_if"""
    memoria.desapilar()
    p[0] = Si(p.lineno(1), find_column(input, p.slice[1]), p[3], None, None)


def p_continuacion_if(p):
    """continuacion_if : ELSE LKEY RKEY
                       | ELSE LKEY instrucciones RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY instrucciones RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY instrucciones RKEY continuacion_if
                       | ELSE IF LPAR exprecion RPAR LKEY RKEY continuacion_if"""
    memoria.desapilar()

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
        p[0] = CallFuncion(p.lineno(1), find_column(
            input, p.slice[1]), p[1], None)
    else:
        p[0] = CallFuncion(p.lineno(1), find_column(
            input, p.slice[1]), p[1], p[3])

# Parametros de llamado de funcion o metodo


def p_parametros(p):
    """parametros : exprecion
                  | parametros COMMA exprecion"""

# Ciclo while de un funcion


def p_ciclo_while(p):
    """ciclo_while : WHILE LPAR exprecion RPAR LKEY RKEY
                   | WHILE LPAR exprecion RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    if len(p) == 7:
        p[0] = Mientras(0, 0, p[3], None)
    else:
        p[0] = Mientras(0, 0, p[3], p[6])

# Declaracion de una funcion


def p_funcion(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY RKEY"""
    memoria.desapilar()
    p[0] = Funcion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', None, None)


def p_funcion_2(p):
    """funcion : FUNCTION ID LPAR lista_parametros RPAR LKEY RKEY"""
    memoria.desapilar()
    p[0] = Funcion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', p[4], None)


def p_funcion_3(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    p[0] = Funcion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', None, p[6])


def p_funcion_4(p):
    """funcion : FUNCTION ID LPAR lista_parametros RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    p[0] = Funcion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', p[4], p[7])

# Seccion de declaracion de parametros de una funcion


def p_lista_parametros(p):
    """lista_parametros : ID COLON tipo
                        | lista_parametros COMMA ID COLON tipo"""

# instruccion de declaracion de variables


def p_declaracion(p):
    """declaracion : LET ID COLON tipo IGUAL exprecion SEMICOLON"""
    p[0] = Declaracion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], p[4], p[6])


def p_declaracion_2(p):
    """declaracion : LET ID IGUAL exprecion SEMICOLON"""
    p[0] = Declaracion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', p[4])


def p_declaracion_3(p):
    """declaracion : LET ID COLON tipo SEMICOLON"""
    p[0] = Declaracion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], p[4], None)


def p_declaracion_4(p):
    """declaracion : LET ID SEMICOLON"""
    p[0] = Declaracion(p.lineno(1), find_column(
        input, p.slice[1]), p[2], 'any', None)

# Instruccion de asignacion


def p_asignacion(p):
    """asignacion : ID IGUAL exprecion SEMICOLON"""
    p[0] = Asignacion(p.lineno(1), find_column(input, p.slice[1]), p[1], p[3])

# Producciones referentes al tipo de dato


def p_tipo(p):
    """tipo : base
            | base LBRA RBRA"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = 'array'


def p_base(p):
    """base : NUMBER
            | ANY
            | BOOLEAN
            | STRING
            | ID"""

    if (p[1] == 'number'):
        p[0] = p[1]
    elif (p[1] == 'any'):
        p[0] = p[1]
    elif (p[1] == 'boolean'):
        p[0] = p[1]
    elif (p[1] == 'string'):
        p[0] = p[1]
    else:
        p[0] = 'struct'


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
    izquiera = Primitivo(p.lineno(1), find_column(
        input, p.slice[1]), 'number', -1)
    p[0] = Aritmetica(p.lineno(1), find_column(
        input, p.slice[1]), izquiera, p[2], '*')


def p_exprecion_2(p):
    """exprecion : exprecion MAS exprecion
                 | exprecion MENOS exprecion
                 | exprecion MULT exprecion
                 | exprecion DIV exprecion
                 | exprecion POTENCIA exprecion
                 | exprecion MOD exprecion"""
    p[0] = Aritmetica(p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[1])


def p_exprecion_3(p):
    """exprecion : exprecion MAQ exprecion
                 | exprecion MEQ exprecion
                 | exprecion MAIQ exprecion
                 | exprecion MEIQ exprecion
                 | exprecion NEQ exprecion
                 | exprecion EQ exprecion"""
    p[0] = Relacional(p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[1])


def p_exprecion_4(p):
    """exprecion : exprecion OR exprecion
                 | exprecion AND exprecion"""
    p[0] = Logico(p.lineno(2), find_column(
        input, p.slice[2]), p[1], p[3], p[1])


def p_exprecion_5(p):
    """exprecion : NOT exprecion"""
    p[0] = Logico(p.lineno(1), find_column(
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
    """sub_exprecion : NULL
                     | NUM
                     | STR
                     | STRCS
                     | TRUE
                     | FALSE"""

    if (p[1] == None):
        p[0] = Primitivo(p.lineno(1), find_column(
            input, p.slice[1]), 'null', p[1])
    elif isinstance(p[1], float):
        p[0] = Primitivo(p.lineno(1), find_column(
            input, p.slice[1]), 'number', p[1])
    elif isinstance(p[1], str):
        p[0] = Primitivo(p.lineno(1), find_column(
            input, p.slice[1]), 'string', p[1])
    elif isinstance(p[1], bool):
        p[0] = Primitivo(p.lineno(1), find_column(
            input, p.slice[1]), 'boolean', p[1])


def p_sub_exprecion_3(p):
    """sub_exprecion : ID"""
    p[0] = Acceder(p.lineno(1), find_column(input, p.slice[1]), p[1])


def p_sub_exprecion_4(p):
    """sub_exprecion : ID LPAR RPAR
                     | ID LPAR parametros RPAR
                     | ID DOT ID
                     | ID DOT ID LPAR RPAR
                     | ID DOT ID LPAR exprecion RPAR"""
    if (p[2] == '('):
        if isinstance(p[3], str):
            p[0] = CallFuncion(p.lineno(1), find_column(
                input, p.slice[1]), p[1], [])
        else:
            p[0] = CallFuncion(p.lineno(1), find_column(
                input, p.slice[1]), p[1], p[3])
    elif (p[2] == '.'):
        print('Acceso a struct o funcion nativa')

# Definicion de error del analisis sintactico


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)
    # TODO: Realizar implementacion para recuperar numero de linea y columna en error sintactico
    tabla_errores.addError(
        'Sintactico', "Error sintáctico en '%s'" % t.value, t.lineno(1), find_column(input, t.slice[1]))


# Declaracion de inicio del parser
parser = yacc.yacc()

input = ''


def parse(ip):
    global input
    input = ip
    return parser.parse(ip)
