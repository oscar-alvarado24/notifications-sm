from typing import List
from app.helper.Constants import Constants
from app.helper.exception import NotificationNotFoundException, GetNotificationsException
from app.model.Notification import Notification  

class NotificationService:
    """
    Servicio para gestionar las operaciones CRUD de notificaciones.
    Implementa la lógica de negocio entre el controlador y el repositorio.
    """

    def __init__(self, notification_repository):
        """
        Notifications service constructor.
        
        Args:
            notification_repository: Notifications repository previously built
        """
        self.repository = notification_repository

    def find_all_notifications_by_user(self, user_id: int) -> List[Notification]:
        """
        Get all notifications for a specific user.

        Args:
            user_id: ID of user to get notifications
            
        Returns:
            Notifications list of user
        """
        try:
            notification_dicts = self.repository.find_all_notifications_by_user(user_id)

            # 1. Crear una lista vacía para almacenar los resultados
            notifications_list = []

            # 2. Iterar sobre cada diccionario en la lista de entrada
            for notification_dict in notification_dicts:
                
                # 3. Convertir el diccionario en un objeto Notification
                notification_obj = Notification.from_dict(notification_dict)
                
                # 4. (Opcional) Validación/Depuración - puedes agregar logs o comprobaciones
                # Ejemplo: verificar que la conversión fue exitosa
                if not isinstance(notification_obj, Notification):
                    # Manejar error o registrar advertencia
                    print(f"Advertencia: Falló la conversión para {notification_dict}")
                    continue  # Saltar este elemento
                
                # 5. Agregar el objeto a la lista
                notifications_list.append(notification_obj)

            # 6. Retornar la lista completa de objetos
            return notifications_list
        except NotificationNotFoundException as exception:
            raise exception
        except GetNotificationsException as exception:
            raise exception
        except Exception as exception:
            print(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id), exception)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
    
    def get_notification_with_status_unread(self, user_id: int) -> List[Notification]:
        """
        Get all unread notifications for a specific user.

        Args:
            user_id: ID of user to get unread notifications
            
        Returns:
            Unread notifications list of user
        """
        try:
            notification_dicts = self.repository.get_notification_with_status_unread(user_id)

            return [Notification.from_dict(notification_dict) for notification_dict in notification_dicts]
        except NotificationNotFoundException | GetNotificationsException as exception:
            raise exception
        except Exception as exception:
            print(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id), exception)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
        
    def delete_notification(self, notification_id: int) -> str:
        """
        Delete a notification by its ID.

        Args:
            notification_id: ID of the notification to delete
            
        Returns:
            str: Success or don't exist message
        """
        result= self.repository.delete_notification(notification_id)

        if (result):
            return Constants.DELETE_NOTIFICATION_SUCESFULLY.format(notification_id=notification_id)
        return Constants.NOTIFICATION_NOT_EXIST.format(notification_id=notification_id)
    
    def create_notification(self, model: Notification) -> str:
        """
        Create a new notification.

        Args:
            model: Notification object to create
            
        Returns:
            Success message if creation was successful
        """
        return self.repository.create_notification(model)
    
    def update_read_value(self, notification_ids: List[int]) -> str:
        """
        Update the read status of multiple notifications.

        Args:
            notification_ids: List of notification IDs to update

        Returns:
            Success message if update was successful
        """
        return self.repository.update_read_value(notification_ids)
    
