class UpdateReadStatusException(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "UpdateReadStatusException"
        super().__init__(self.mensaje)