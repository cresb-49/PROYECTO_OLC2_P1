import ply.lex as lex

#Definicion de tokens 



#Construcion del Lexer
lexer = lex.lex()

data = "//Comentario de prueba";

lexer.input(data);

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)