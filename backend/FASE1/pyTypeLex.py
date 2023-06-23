import FASE1.ply.lex as lex  # Import del lex para la generacion del analizadoz lexico
from FASE1.Models.resultado import Resultado
# Import de las clases auxiliares
from FASE1.Errores.Errores import TablaErrores
from FASE1.Errores.Errores import Error

import re
from datetime import datetime

tabla_errores = TablaErrores()
resultado = Resultado([], [])
errores_lexer = []


# Definicion de tokens
reservadas = {
    "let": "LET",
    "for": "FOR",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "of": "OF",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "function": "FUNCTION",
    "interface": "INTERFACE",
    "number": "NUMBER",
    "any": "ANY",
    "boolean": "BOOLEAN",
    "string": "STRING",
    "null": "NULL",
    "true": "TRUE",
    "false": "FALSE",
    "console": "CONSOLE"
}

tokens = [
    'STR',  # Cadena string ""
    'STRCS',  # Cadena string ''
    'FLOAT',  # valor con punto decimal
    'NUM',  # Valor numerico
    'LPAR',  # (
    'RPAR',  # )
    'LBRA',  # [
    'RBRA',  # ]
    'LKEY',  # {
    'RKEY',  # }
    'COLON',  # :
    'EQ',  # ===
    'NEQ',  # !==
    'IGUAL',  # =
    'MEQ',  # <
    'MAQ',  # >
    'MEIQ',  # <=
    'MAIQ',  # >=
    'NOT',  # !
    'OR',  # ||
    'AND',  # $$
    'POTENCIA',  # ^
    'SUM',  # ++
    'RES',  # --
    'MAS',  # +
    'MENOS',  # -
    'MULT',  # *
    'DIV',  # /
    'MOD',  # %
    'COMMA',  # ,
    'DOT',  # .
    'SEMICOLON',  # ;
    'ID',  # Identificador
]+list(reservadas.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica en las palabras reservadas
    # t.type = reservadas.get(t.value.lower(), 'ID')
    t.type = reservadas.get(t.value, 'ID')
    return t


def t_STR(t):
    r'\".*?\"'
    t.value = t.value[1:-1].encode().decode("unicode_escape")
    return t


def t_STRCS(t):
    r'\'.*?\''
    t.value = t.value[1:-1].encode().decode("unicode_escape")
    return t


def t_FLOAT(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    return t


def t_NUM(t):
    r'(\d+)'
    return t


t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRA = r'\['
t_RBRA = r'\]'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_COLON = r':'
t_MEIQ = r'<='
t_MAIQ = r'>='
t_NEQ = r'!=='
t_EQ = r'==='
t_IGUAL = r'='
t_MEQ = r'<'
t_MAQ = r'>'
t_SUM = r'\+\+'
t_RES = r'--'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'\%'
t_NOT = r'\!'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_POTENCIA = r'\^'
t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'

# Comentario de múltiples líneas /* .. */


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...


def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados space,tabulador,retorno de carro(windows)
t_ignore = " \t\r"

# Aumento para el conteo de lineas en la lectura de archivos


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Control de errores de analizador lexico


def t_error(t):
    error = "Caracter ilegal '%s'" % t.value[0]
    # resultado.add_error('Lexico', error, t.lexer.lineno, 0)
    lexer_add_error('Lexico', error, t.lexer.lineno, 0)
    t.lexer.skip(1)


def lexer_add_error(tipo, desc, linea, columna):
    fecha_hora_actual = datetime.now()
    fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M")
    error = Error(tipo, desc, linea, columna, fecha_hora_formateada)
    errores_lexer.append(error)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos - line_start) + 1


def get_errores_lexer():
    return errores_lexer


def clear_errores_lexer():
    errores_lexer.clear()


# Construcion del Lexer
# lexer = lex.lex()
lexer = lex.lex(reflags=re.IGNORECASE)  # TODO: tomar en si no funciona

# Apertura y lectura del archivo de entrada
# archivo = open("backend/entrada.ts", "r")
# input = archivo.read()

# lexer.input(input)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
