"""
Paquete de excepciones para notificaciones
"""

from .ConnectionEmptyError import ConnectionEmptyError
from .CreateNotificationException import CreateNotificationException
from .DeleteNotificationException import DeleteNotificationException
from .GetNotificationsException import GetNotificationsException
from .NotificationNotFoundException import NotificationNotFoundException
from .UpdateReadStatusException import UpdateReadStatusException

# Exportar todas las excepciones
__all__ = [
    'ConnectionEmptyError',
    'CreateNotificationException',
    'DeleteNotificationException', 
    'GetNotificationsException',
    'NotificationNotFoundException',
    'UpdateReadStatusException'
]