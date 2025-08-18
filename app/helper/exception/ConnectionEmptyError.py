class ConnectionEmptyError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "ConnectionEmptyError"
        super().__init__(self.mensaje)