import ply.yacc as yacc
import pyTypeLex as lex




# Definicion de error del analisis sintactico
def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


# Declaracion de inicio del parser
parser = yacc.yacc()


def parse(input):
    return parser.parse(input)
