from datetime import datetime
from FASE2.Errores.Errores import Error


class Resultado:
    resultado = None

    def __init__(self,erres,consola) -> None:
        self.sentencias = None
        self.errores = []
        self.tabla_simbolos = None
        self.consola = []
        self.scope_global = None
        self.entornos_variables = dict()
        
    def __str__(self):
        return f"sentencias: {self.sentencias}\n" \
            f"errores: {self.errores}\n" \
            f"tabla_simbolos: {self.tabla_simbolos}\n" \
            f"consola: {self.consola}\n" \
            f"scope_global: {self.scope_global}\n" \
            f"entornos_variables: {self.entornos_variables}"

    
    def get_instance(self):
        if Resultado.resultado == None:
            Resultado.resultado = Resultado()
        return Resultado.resultado

    def clean_all(self):
        self.sentencias = None
        self.errores = []
        self.tabla_simbolos = None
        self.consola = []
        self.scope_global = None
        self.entornos_variables = dict()
        Resultado.resultado = Resultado()

    def add_error(self, tipo, descripcion, linea, columna) -> None:
        fecha_hora_actual = datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M")
        error = Error(tipo, descripcion, linea, columna, fecha_hora_formateada)
        self.errores.append(error)

    def add_obj_error(self, error: Error):
        self.errores.append(error)

    def set_scope_global(self, scope):
        self.scope_global = scope

    def get_scope_global(self):
        return self.scope_global

    def agregar_entorno(self, clave, scope):
        self.entornos_variables[clave] = scope
