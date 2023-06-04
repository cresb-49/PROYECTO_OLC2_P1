import ply.lex as lex

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
    'ID',  # Identificador
    'STR',  # Cadena string
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
    'MAS',  # +
    'MENOS',  # -
    'MULT',  # *
    'DIV',  # /
    'MOD',  # %
    'COMMA',  # ,
    'DOT',  # .
    'SEMICOLON',  # ;
]+list(reservadas.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_STR(t):
    r'\".*?\"'
    t.value = t.value[1:-1].encode().decode("unicode_escape")
    return t


def t_NUM(t):
    r'(\d+|\d+\.\d+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
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
t_MAS = r'\+'
t_MENOS = r'-'
t_NOT = r'\!'
t_OR = r'\|\|'
t_AND = r'\$\$'
t_POTENCIA = r'\^'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'\%'
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
    print('Comentario encontrado')
    t.lexer.lineno += 1


# Caracteres ignorados space,tabulador,retorno de carro(windows)
t_ignore = " \t\r"

# Aumento para el conteo de lineas en la lectura de archivos


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Control de errores de analizador lexico


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construcion del Lexer
lexer = lex.lex()

# Apertura y lectura del archivo de entrada
archivo = open(
    "/home/ben/Documents/GitHub/PROYECTO_OLC2_P1/backend/entrada.ts", "r")
input = archivo.read()

lexer.input(input)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
