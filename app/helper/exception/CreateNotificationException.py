class CreateNotificationException(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "CreateNotificationException"
        super().__init__(self.mensaje)