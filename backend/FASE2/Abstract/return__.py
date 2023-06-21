class Return:
    def __init__(self, val, ret_type, is_temp, aux_type, length=0, referencia=''):
        self.value = val
        self.type = ret_type
        self.aux_type = aux_type
        self.length = length
        self.referencia = referencia
        self.is_temp = is_temp
        self.list_true_lbls = []
        self.list_false_lbls = []

    def __str__(self):
        return f"Value: {self.value}, Type: {self.type}, Aux Type: {self.aux_type}, True Labels: {self.list_true_lbls}, False Labels: {self.list_false_lbls}"

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

    def add_true_lbl(self, true_lbl):
        self.list_true_lbls.append(true_lbl)

    def add_false_lbl(self, false_lbl):
        self.list_false_lbls.append(false_lbl)

    def get_true_lbls(self):
        return self.list_true_lbls

    def get_false_lbls(self):
        return self.list_false_lbls

    def set_true_lbls(self, true_lbls):
        self.list_true_lbls = true_lbls

    def set_false_lbls(self, false_lbls):
        self.list_false_lbls = false_lbls
