import ply.yacc as yacc  # Import de yacc para generar el analizador sintactico
from pyTypeLex import lexer  # Import del lexer realizado por el usuario
# Import de los tokens del lexer, es necesario por tenerlo en archivos separados
from pyTypeLex import tokens

# Seccion para importar las abstracciones y ED para verificar la infomacion
from ED.Pila import Pila
from pyTypeLex import tabla_errores  # Impotado de la tabla de errores del lexer

# Clases referentes a la tabla de simbolos

# Inicio de la gramatica


def p_init(p):
    """init : limit_intrucciones"""

# Intrucciones limitadas solo al ambito global


def p_limit_intrucciones(p):
    """limit_intrucciones : limit_intrucciones limit_intruccion
                          | limit_intruccion"""
    # TODO: Aqui es donde se inicializa el scope global, este es el scope 0


def p_limit_intruccion(p):
    """limit_intruccion : instruccion
                        | funcion"""

# Intrucciones que pueden estar dentro de sentencias de control, no podemos
# declarar funciones dentro de las sentencias de control


def p_instrucciones(p):
    """instrucciones : instrucciones instruccion"""


def p_instrucciones_2(p):
    """instrucciones : instruccion"""
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

# Intrucion console.log


def p_print(p):
    """print : CONSOLE DOT ID LPAR exprecion RPAR SEMICOLON"""


# Instruccion continue


def p_continuar(p):
    """continuar : CONTINUE SEMICOLON"""

# Instruccion break


def p_romper(p):
    """romper : BREAK SEMICOLON"""

# Instruccion return


def p_retorno(p):
    """retorno : RETURN SEMICOLON
               | RETURN exprecion SEMICOLON"""

# Producciones de la intruccion for


def p_ciclo_for(p):
    """ciclo_for : FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY RKEY
                 | FOR LPAR declaracion_for SEMICOLON exprecion SEMICOLON sumador RPAR LKEY instrucciones RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY instrucciones RKEY"""


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


def p_continuacion_if(p):
    """continuacion_if : ELSE LKEY RKEY
                       | ELSE LKEY instrucciones RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY instrucciones RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY RKEY
                       | ELSE IF LPAR exprecion RPAR LKEY instrucciones RKEY continuacion_if
                       | ELSE IF LPAR exprecion RPAR LKEY RKEY continuacion_if"""

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

# Parametros de llamado de funcion o metodo


def p_parametros(p):
    """parametros : exprecion
                  | parametros COMMA exprecion"""

# Ciclo while de un funcion


def p_ciclo_while(p):
    """ciclo_while : WHILE LPAR exprecion RPAR LKEY RKEY
                   | WHILE LPAR exprecion RPAR LKEY instrucciones RKEY"""

# Declaracion de una funcion


def p_funcion(p):
    """funcion : FUNCTION ID LPAR RPAR LKEY RKEY
               | FUNCTION ID LPAR lista_parametros RPAR LKEY RKEY
               | FUNCTION ID LPAR RPAR LKEY instrucciones RKEY
               | FUNCTION ID LPAR lista_parametros RPAR LKEY instrucciones RKEY"""

    # TODO: Eliminar prueba de codigo de funciones
    print("Funcion encontrada", p[2])

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

    print("Declaracion de variable", p[2])

# Instruccion de asignacion


def p_asignacion(p):
    """asignacion : ID IGUAL exprecion SEMICOLON"""

# Producciones referentes al tipo de dato


def p_tipo(p):
    """tipo : base
            | base LBRA RBRA"""


def p_base(p):
    """base : NUMBER
            | ANY
            | BOOLEAN
            | STRING
            | ID"""


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
    # ('left', 'LPAR', 'RPAR'), #Precedencia de parentesis
    ('right', 'UMINUS'),  # Operador unario
)

# Expreciones -> operaciones entre variables, constantes, funciones y metodos


def p_exprecion(p):
    """exprecion : MENOS exprecion %prec UMINUS
                 | exprecion MAS exprecion
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
                 | exprecion AND exprecion
                 | NOT exprecion
                 | sub_exprecion"""

# Valores atomicos es decir, el valor de una variable, constante o resultado de una
# funcion o metodo


def p_sub_exprecion(p):
    """sub_exprecion : LPAR exprecion RPAR
                     | NULL
                     | NUM
                     | STR
                     | TRUE
                     | FALSE
                     | ID
                     | ID LPAR RPAR
                     | ID LPAR parametros RPAR
                     | ID DOT ID
                     | ID DOT ID LPAR RPAR
                     | ID DOT ID LPAR exprecion RPAR"""


# Definicion de error del analisis sintactico


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)
    # TODO: Realizar implementacion para recuperar numero de linea y columna en error sintactico
    tabla_errores.addError(
        'Sintactico', "Error sintáctico en '%s'" % t.value, 0, 0)


# Declaracion de inicio del parser
parser = yacc.yacc()

# Apertura y lectura del archivo de entrada
archivo = open("backend/entrada.ts", "r")
input = archivo.read()


def parse(input):
    return parser.parse(input)


parse(input)