import ply.lex as lex

# Definicion de tokens
reservadas = {
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
    "let": "LET",
    "number": "NUMBER",
    "any": "ANY",
    "boolean": "BOOLEAN",
    "string": "STRING",
    "null": "NULL",
    "true": "TRUE",
    "false": "FALSE",
    "console.log": "LOG",
}

tokens = (
    'NAME',  # Identificador
    'LPAR',  # (
    'RPAR',  # )
    'LBRA',  # [
    'RBRA',  # ]
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
)+list(reservadas.values())

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

# Caracteres ignorados
t_ignore = " \t\r"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construcion del Lexer
lexer = lex.lex()

data = "//Comentario de prueba"

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
