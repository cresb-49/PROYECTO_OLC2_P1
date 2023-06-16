from decimal import Decimal


class FuncionNativa():

    def __init__(self) -> None:
        pass

    def hacer_split(self, cadena: str, separador: str):
        return cadena.split(separador)

    # Devuelve el parametro convertido en string
    def hacer_to_string(self, numero):
        return str(numero)  # retronar la conversion a String del parametro

    # Convierte la cadena recibida en lower case con la funcon nativa .lower()
    def hacer_to_lower_case(self, cadena: str):
        return cadena.lower()

    # Convierte la cadena recibida en Upper case con la funcionn nativa .upper()
    def hacer_to_upper_case(self, cadena: str):
        return cadena.upper()

    # Une dos arrays solamente sumando uno con el otro (media vez sean arrys se hace la agregacion)
    def hacer_concat(self, array1, array2):
        return array1 + array2

    # Hace un round al numero especificado con el numero de dcimales especificado
    def hacer_to_fixed(self, numero: float, no_decimales: float):
        return round(numero,  int(no_decimales))

    def hacer_to_exponential(self, numero: float, numeroExponencial: float):
        xx = f"{numero:.{int(numeroExponencial)}E} "
        return xx

    # devuelve la conversion ha string de algo
    def string(self, param):
        return str(param)

    # devuelve la conversion ha string de algo
    def number(self, param):
        try:
            return float(param)
        except ValueError as verr:
            return None

    def length(self, param):
        return len(param)

        # devuelve la conversion ha string de algo
    def push(self, array, param):
        array.append(param)
