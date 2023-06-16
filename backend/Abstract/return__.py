class Return:
    def __init__(self, val, ret_type, is_temp, aux_type="", length=0, referencia=''):
        self.value = val
        self.type = ret_type
        self.aux_type = aux_type
        self.length = length
        self.referencia = referencia
        self.is_temp = is_temp
        self.true_lbl = ''
        self.false_lbl = ''

    def __str__(self):
        return f"Value: {self.value}, Type: {self.type}, Aux Type: {self.aux_type}, Length: {self.length}, Referencia: {self.referencia}, Is Temp: {self.is_temp}, True Label: {self.true_lbl}, False Label: {self.false_lbl}"

    def get_value(self):
        return self.value

    def get_tipo(self):
        return self.type

    def get_tipo_aux(self):
        return self.aux_type

    def get_length(self):
        return self.length

    def get_referencia(self):
        return self.referencia

    def get_true_lbl(self):
        return self.true_lbl

    def get_false_lbl(self):
        return self.false_lbl

    def set_value(self, value):
        self.value = value

    def set_tipo(self, tipo):
        self.type = tipo

    def set_tipo_aux(self, tipo):
        self.aux_type = tipo

    def set_length(self, length):
        self.length = length

    def set_referencia(self, ref):
        self.referencia = ref

    def set_true_lbl(self, true_lbl):
        self.true_lbl = true_lbl

    def set_false_lbl(self, false_lbl):
        self.false_lbl = false_lbl
