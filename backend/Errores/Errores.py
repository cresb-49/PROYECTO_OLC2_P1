from datetime import datetime


class Error:
    def __init__(self, tipo, descripcion, linea, columna, fecha_hora):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
        self.fecha_hora = fecha_hora


class TablaErrores:
    def __init__(self):
        self.errores = []

    def addError(self, tipo, descripcion, linea, columna) -> None:
        fecha_hora_actual = datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M")
        error = Error(tipo, descripcion, linea, columna, fecha_hora_formateada)
        self.errores.append(error)

    def erroresOrdenadosFechaHora(self) -> list:
        errores = sorted(self.errores, key=lambda error: error.fecha_hora)
        return errores
