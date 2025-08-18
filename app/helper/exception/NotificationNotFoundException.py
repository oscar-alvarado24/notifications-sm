class NotificationNotFoundException(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "NotificationNotFoundException"
        super().__init__(self.mensaje)