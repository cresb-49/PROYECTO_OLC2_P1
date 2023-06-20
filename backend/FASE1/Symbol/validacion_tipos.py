from FASE1.Symbol.tipoEnum import TipoEnum

def validar_aritmetica(tipo_izq,tipo_der,signo_operacion):
    if signo_operacion == '+':
        if tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.NUMBER:
            return TipoEnum.NUMBER 
        if tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.ANY:
            return TipoEnum.NUMBER 
        if tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.NUMBER:
            return TipoEnum.NUMBER
        elif tipo_izq == TipoEnum.STRING and tipo_der == TipoEnum.STRING:
            return TipoEnum.STRING
        elif tipo_izq == TipoEnum.STRING and tipo_der == TipoEnum.ANY:
            return TipoEnum.STRING
        elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.STRING:
            return TipoEnum.STRING
        if tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.ANY:
            return TipoEnum.ANY
    else:
        if tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.NUMBER:
            return TipoEnum.NUMBER 
        elif tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.ANY:
            return TipoEnum.NUMBER
        elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.NUMBER:
            return TipoEnum.NUMBER
        elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.ANY:
            return TipoEnum.ANY
        else: 
            return TipoEnum.ERROR

def validar_logica(tipo_izq,tipo_der,signo_operacion):
    if signo_operacion == '!':
        if tipo_der == TipoEnum.BOOLEAN:
            return TipoEnum.BOOLEAN
        elif tipo_der == TipoEnum.ANY:
            return TipoEnum.ANY
        else:
            return TipoEnum.ERROR
    else:
        if tipo_izq == TipoEnum.BOOLEAN and tipo_der == TipoEnum.BOOLEAN:
            return TipoEnum.BOOLEAN
        elif tipo_izq == TipoEnum.BOOLEAN and tipo_der == TipoEnum.ANY:
            return TipoEnum.BOOLEAN
        elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.BOOLEAN:
            return TipoEnum.BOOLEAN
        elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.ANY:
            return TipoEnum.ANY
        else:
            return TipoEnum.ERROR

def validar_comparacion(tipo_izq,tipo_der):
    if tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.NUMBER:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.STRING and tipo_der == TipoEnum.STRING:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.NUMBER and tipo_der == TipoEnum.ANY:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.NUMBER:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.STRING and tipo_der == TipoEnum.ANY:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.STRING:
        return TipoEnum.BOOLEAN
    elif tipo_izq == TipoEnum.ANY and tipo_der == TipoEnum.ANY:
        return TipoEnum.BOOLEAN
    else:
        return TipoEnum.ERROR