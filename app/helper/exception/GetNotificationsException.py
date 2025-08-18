class GetNotificationsException(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "GetNotificationsException"
        super().__init__(self.mensaje)