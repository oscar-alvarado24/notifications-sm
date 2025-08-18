class DeleteNotificationException(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.name = "DeleteNotificationException"
        super().__init__(self.mensaje)