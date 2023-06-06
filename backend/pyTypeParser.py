import ply.yacc as yacc  # Import de yacc para generar el analizador sintactico
from pyTypeLex import lexer  # Import del lexer realizado por el usuario
# Import de los tokens del lexer, es necesario por tenerlo en archivos separados
from pyTypeLex import tokens

# Seccion para importar las abstracciones y ED para verificar la infomacion
from ED.Pila import Pila
from pyTypeLex import tabla_errores  # Impotado de la tabla de errores del lexer
from Models.resultado import Resultado

# Clases referentes a la tabla de simbolos
from logica import Scope
from logica import Literal
from logica import Acceder
from logica import CallFuncion
from logica import Declaracion
from logica import Tipo
from logica import TipoEnum

from logica import Operacion
from logica import OpcionOperacion
from logica import Relacional
from logica import OpcionRelacional
from logica import Logica
from logica import OpcionLogica

from logica import Asignacion
from logica import Funcion
from logica import Si
from logica import Para
from logica import Mientras
from logica import PrintPy
from logica import Retornar
from logica import Continuar
from logica import Detener

from logica import Sentencias

# Inicio de la gramatica

memoria = Pila()
contador = 0
registro = []


def decla_variable(declaracion: Declaracion, tipo: Tipo):
    scope: Scope = memoria.obtener_tope()
    scope.declarar_variable(declaracion.id, None, tipo, 0, 0)


def p_init(p):
    """init : limit_intrucciones"""
    memoria.desapilar()
    p[0] = Resultado(p[1],tabla_errores,registro)

# Intrucciones limitadas solo al ambito global


def p_limit_intrucciones(p):
    """limit_intrucciones : limit_intrucciones limit_intruccion"""
    sentencias: Sentencias = p[1]
    sentencias.intrucciones.append(p[2])
    p[0] = sentencias


def p_limit_intrucciones_2(p):
    """limit_intrucciones : limit_intruccion"""
    sentencias = Sentencias(0, 0, [])
    sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    print('Generacion Entorno Global')
    entorno = Scope(memoria.obtener_tope())
    memoria.apilar(entorno)
    registro.append(entorno)
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
    p[0] = sentencias


def p_instrucciones_2(p):
    """instrucciones : instruccion"""
    sentencias = Sentencias(0, 0, [])
    sentencias.intrucciones.append(p[1])
    p[0] = sentencias
    print('Generacion Entorno Local')
    entorno = Scope(memoria.obtener_tope())
    memoria.apilar(entorno)
    registro.append(entorno)
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
    p[0] = PrintPy(0, 0)

# Instruccion continue


def p_continuar(p):
    """continuar : CONTINUE SEMICOLON"""
    p[0] = Continuar(0, 0)
# Instruccion break


def p_romper(p):
    """romper : BREAK SEMICOLON"""
    p[0] = Detener(0, 0)

# Instruccion return


def p_retorno(p):
    """retorno : RETURN SEMICOLON
               | RETURN exprecion SEMICOLON"""
    if len(p) == 3:
        p[0] = Retornar(0, 0, None)
    else:
        p[0] = Retornar(0, 0, p[2])
# Producciones de la intruccion for


def p_ciclo_for(p):
    """ciclo_for : FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY RKEY
                 | FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY instrucciones RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    p[0] = Para(0, 0, -1, None, 'none', None, None)


def p_declaracion_for(p):
    """declaracion_for : LET ID COLON tipo IGUAL exprecion
                       | LET ID IGUAL exprecion
    """


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
    p[0] = Si(0, 0, p[3], None)


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
    p[0] = CallFuncion(0, 0, p[1], None)

# Parametros de llamado de funcion o metodo


def p_parametros(p):
    """parametros : exprecion
                  | parametros COMMA exprecion"""

# Ciclo while de un funcion


def p_ciclo_while(p):
    """ciclo_while : WHILE LPAR exprecion RPAR LKEY RKEY
                   | WHILE LPAR exprecion RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    p[0] = Mientras(0, 0, p[3], None)

# Declaracion de una funcion


def p_funcion(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY RKEY
               | FUNCTION ID LPAR lista_parametros RPAR LKEY RKEY
               | FUNCTION ID LPAR RPAR LKEY instrucciones RKEY
               | FUNCTION ID LPAR lista_parametros RPAR LKEY instrucciones RKEY"""
    memoria.desapilar()
    p[0] = Funcion(0, 0, p[2], None, None)

# Seccion de declaracion de parametros de una funcion


def p_lista_parametros(p):
    """lista_parametros : ID COLON tipo
                        | lista_parametros COMMA ID COLON tipo"""

# instruccion de declaracion de variables


def p_declaracion(p):
    """declaracion : LET ID COLON tipo IGUAL exprecion SEMICOLON
                   | LET ID IGUAL exprecion SEMICOLON
                   | LET ID COLON tipo SEMICOLON
                   | LET ID SEMICOLON"""
    if (p[3] == ':'):
        p[0] = Declaracion(0, 0, p[2], p[4], Literal(
            0, 0, None, Tipo(TipoEnum.ANY, None)))
    else:
        p[0] = Declaracion(0, 0, p[2], Tipo(TipoEnum.ANY, None), Literal(
            0, 0, None, Tipo(TipoEnum.ANY, None)))

# Instruccion de asignacion


def p_asignacion(p):
    """asignacion : ID IGUAL exprecion SEMICOLON"""
    p[0] = Asignacion(0, 0, p[1], p[3])

# Producciones referentes al tipo de dato


def p_tipo(p):
    """tipo : base
            | base LBRA RBRA"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        tipo: Tipo = p[1]
        tipo.tipo_secundario = tipo.get_tipo_string()
        tipo.type = TipoEnum.ARRAY
        p[0] = tipo


def p_base(p):
    """base : NUMBER
            | ANY
            | BOOLEAN
            | STRING
            | ID"""

    if (p[1] == 'number'):
        p[0] = Tipo(TipoEnum.NUMBER, None)
    elif (p[1] == 'any'):
        p[0] = Tipo(TipoEnum.ANY, None)
    elif (p[1] == 'boolean'):
        p[0] = Tipo(TipoEnum.BOOLEAN, None)
    elif (p[1] == 'string'):
        p[0] = Tipo(TipoEnum.STRING, None)
    else:
        p[0] = Tipo(TipoEnum.STRUCT, p[1])


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


def p_exprecion_2(p):
    """exprecion : exprecion MAS exprecion
                 | exprecion MENOS exprecion
                 | exprecion MULT exprecion
                 | exprecion DIV exprecion
                 | exprecion POTENCIA exprecion
                 | exprecion MOD exprecion
                 | exprecion MAQ exprecion
                 | exprecion MEQ exprecion
                 | exprecion MAIQ exprecion
                 | exprecion MEIQ exprecion
                 | exprecion NEQ exprecion
                 | exprecion EQ exprecion
                 | exprecion OR exprecion
                 | exprecion AND exprecion"""
    if p[2] == '+':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.SUMA)
    elif p[2] == '-':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.RESTA)
    elif p[2] == '*':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.MUL)
    elif p[2] == '/':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.DIV)
    elif p[2] == '^':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.POT)
    elif p[2] == '%':
        p[0] = Operacion(0, 0, p[1], p[3], OpcionOperacion.MOD)
    elif p[2] == '>':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.MAYOR)
    elif p[2] == '<':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.MENOR)
    elif p[2] == '>=':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.MAYOR_IGUAL)
    elif p[2] == '<=':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.MENOR_IGUAL)
    elif p[2] == '<!==':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.DIFERENTE)
    elif p[2] == '===':
        p[0] = Relacional(0, 0, p[1], p[3], OpcionRelacional.IGUAL)
    elif p[2] == '||':
        p[0] = Logica(0, 0, p[1], p[3], OpcionLogica.OR)
    elif p[2] == '&&':
        p[0] = Logica(0, 0, p[1], p[3], OpcionLogica.AND)


def p_exprecion_3(p):
    """exprecion : NOT exprecion"""
    p[0] = Logica(0, 0, None, p[2], OpcionLogica.NOT)


def p_exprecion_4(p):
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
                     | TRUE
                     | FALSE"""

    if (p[1] == None):
        p[0] = Literal(0, 0, p[1], Tipo(TipoEnum.NULL, None))
    elif isinstance(p[1], float):
        p[0] = Literal(0, 0, p[1], Tipo(TipoEnum.NUMBER, None))
    elif isinstance(p[1], str):
        p[0] = Literal(0, 0, p[1], Tipo(TipoEnum.STRING, None))
    elif isinstance(p[1], bool):
        p[0] = Literal(0, 0, p[1], Tipo(TipoEnum.BOOLEAN, None))


def p_sub_exprecion_3(p):
    """sub_exprecion : ID"""
    p[0] = Acceder(0, 0, p[1])


def p_sub_exprecion_4(p):
    """sub_exprecion : ID LPAR RPAR
                     | ID LPAR parametros RPAR
                     | ID DOT ID
                     | ID DOT ID LPAR RPAR
                     | ID DOT ID LPAR exprecion RPAR"""
    if (p[2] == '('):
        if isinstance(p[3], str):
            p[0] = CallFuncion(0, 0, p[1], [])
        else:
            p[0] = CallFuncion(0, 0, p[1], p[3])
    elif (p[2] == '.'):
        print('Acceso a struct o funcion nativa')

# Definicion de error del analisis sintactico


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)
    # TODO: Realizar implementacion para recuperar numero de linea y columna en error sintactico
    tabla_errores.addError(
        'Sintactico', "Error sintáctico en '%s'" % t.value, 0, 0)


# Declaracion de inicio del parser
parser = yacc.yacc()


def parse(input):
    return parser.parse(input)
