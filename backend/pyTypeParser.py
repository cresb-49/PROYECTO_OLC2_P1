import ply.yacc as yacc
import pyTypeLex as lex

# Inicio de la gramatica


def p_init(p):
    """init : instrucciones_globales"""

# Definicion de el uso de todas las intrucciones


def instrucciones_globales(p):
    """instrucciones_globales : instruccion 
                              | instrucciones_globales instruccion
                              | instrucciones_globales funcion
                              | funcion"""

# Intrucciones que pueden estar dentro de sentencias de control, no podemos
# declarar funciones dentro de las sentencias de control


def p_instrucciones(p):
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


def p_instrucciones(p):
    """instrucciones : instrucciones instruccion
                     | instruccion"""

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
    """ciclo_for : FOR LPAR declaracion SEMICOLON exprecion SEMICOLON sumador RPAR LKEY RKEY
                 | FOR LPAR declaracion SEMICOLON exprecion SEMICOLON sumador RPAR LKEY instrucciones RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY RKEY
                 | FOR LPAR LET ID OF exprecion RPAR LKEY instrucciones RKEY"""


def sumador(p):
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

# Seccion de declaracion de parametros de una funcion


def p_lista_parametros(p):
    """lista_parametros : ID COLON tipo
                        | lista_parametros COMMA ID COLON tipo"""

# instruccion de declaracion de variables


def p_declaracion(p):
    """declaracion : LET ID COLON tipo IGUAL exprecion SEMICOLON
                   | LET ID IGUAL exprecion SEMICOLON"""

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


# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'MAQ', 'MEQ', 'MAIQ', 'MEIQ', 'EQ', 'NEQ'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'UMINUS'),  # Operador unario
    ('right', 'POTENCIA'),
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


# Declaracion de inicio del parser
parser = yacc.yacc()


def parse(input):
    return parser.parse(input)
