from datetime import datetime
from Errores.Errores import Error

class Resultado:
    def __init__(self, sentencias, errores, tabla_simbolos, consola) -> None:
        self.sentencias = sentencias
        self.errores = errores
        self.tabla_simbolos = tabla_simbolos
        self.consola = consola
    
    def add_error(self, tipo, descripcion, linea, columna) -> None:
        fecha_hora_actual = datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M")
        error = Error(tipo, descripcion, linea, columna, fecha_hora_formateada)
        self.errores.append(error)



    