import oracledb
from typing import List, Dict, Any
from app.helper.exception import ConnectionEmptyError, GetNotificationsException, NotificationNotFoundException, DeleteNotificationException, CreateNotificationException, UpdateReadStatusException
from app.model.Notification import Notification
from app.helper.Constants import Constants


class NotificationRepository:
    def __init__(self, connection=None):
        if connection is not None:
            self.connection = connection
        else:    
            raise ConnectionEmptyError(Constants.CONNECTION_EMPTY_MSG)
    
    def cursor(self):
        if self.connection is not None:
            return self.connection.cursor()
        else:
            raise ConnectionEmptyError(Constants.CONNECTION_EMPTY_MSG)
    
    def commit(self):
        if self.connection is not None:
            self.connection.commit()
        else:
            raise ConnectionEmptyError(Constants.CONNECTION_EMPTY_MSG)

    def find_all_notifications_by_user(self, user_id:int) -> List[Dict[str, Any]]:
        """
        get all notifications asociate to user.
        
        Args:
            user_id: identification of the user whose notifications are being searched for
            
        Returns:
            Dictionary list with notifications
        """
        cursor = self.cursor()
        try:
            sql = """SELECT * 
                    FROM notifications 
                    WHERE user_id = :user_id
                    ORDER BY status ASC"""
            params = {'user_id': user_id}
            
            cursor.execute(sql, params)
            results = cursor.fetchall()

            if results is None:
                raise NotificationNotFoundException(Constants.NOT_FIND_NOTIFICATIONS_FOR_USER.format(user_id=user_id))
            
            return self.get_notifications_dict(results)
        except NotificationNotFoundException as error:
            raise error
        except oracledb.Error as error:
            print(Constants.ORACLE_ERROR.format(process=Constants.GET_NOTIFICATION_PROCESS, id=user_id), error)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
        except Exception as error:
            print(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id), error)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
        finally:
            cursor.close()

    def get_notification_with_status_unread(self, user_id:int)->List[Dict[str, Any]]:
        """
        Get all unread notifications for a specific user.
        
        Args:
            user_id: ID of the user whose unread notifications are being searched for
            
        Returns:
            List of dictionaries with unread notifications
        """
        cursor = self.cursor()
        try:
            sql = """SELECT * 
                     FROM notifications 
                     WHERE user_id = :user_id AND status = 'unread'
                     ORDER BY id DESC"""
            params = {'user_id': user_id}
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            
            if results is None:
                raise NotificationNotFoundException(Constants.NOT_FIND_NOTIFICATIONS_FOR_USER.format(user_id=user_id))
            
            return self.get_notifications_dict(results)
        
        except NotificationNotFoundException as error:
            raise error
        except oracledb.Error as error:
            print(Constants.ORACLE_ERROR.format(process=Constants.GET_NOTIFICATION_PROCESS, id=user_id), error)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
        except Exception as error:
            print(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id), error)
            raise GetNotificationsException(Constants.GET_NOTIFICATION_ERROR.format(user_id=user_id))
        finally:
            cursor.close()

    def delete_notification(self, notification_id: int) -> bool:
        """
        Delete a notification.
        
        Args:
            notification_id: ID of the notification to delete
            
        Returns:
            True if deleted, False if it didn't exist or there was an error
        """
        cursor = self.cursor()
        try:
            sql = "DELETE FROM notifications WHERE id = :1"
            cursor.execute(sql, (notification_id,))
            rows_affected = cursor.rowcount
            
            self.commit()
            
            return rows_affected > 0
        except oracledb.Error as error:
            print(Constants.ORACLE_ERROR.format(process=Constants.DELETE_NOTIFICATION_PROCESS, id=notification_id), error)
            raise DeleteNotificationException(Constants.DELETE_NOTIFICATION_ERROR.format(user_id=notification_id))  
        except Exception as error:
            print(Constants.DELETE_NOTIFICATION_ERROR.format(id=notification_id), error)
            raise DeleteNotificationException(Constants.DELETE_NOTIFICATION_ERROR.format(id=notification_id))
        finally:
            cursor.close()    

    def create_notification(self, model: Notification) -> str:
        """
        Create a new notification in the database.
        
        Args:
            model: notification data to save in the database.

        Returns:
            Success message if creation was successful
        """
        cursor = self.cursor()
        try:
            notification_data = model.to_dict()
            status = 'unread'
            
            sql_insert = """INSERT INTO notifications (user_id, message, status)
                        VALUES (:1, :2, :3)
                        RETURNING id INTO :4"""
        
            # Corrección 2: Crear variable para capturar el ID generado
            new_id_var = cursor.var(int)
            
            values = (
                notification_data.get('user_id'),
                notification_data.get('message'),
                status,
                new_id_var  # Variable para capturar el ID
            )
            
            cursor.execute(sql_insert, values)
            
            # Corrección 3: Obtener el ID desde la variable de retorno
            new_id = new_id_var.getvalue()[0]
            
            self.commit()

            return Constants.CREATE_SUCCESS_MSG.format(id=new_id)
        
        except oracledb.Error as error:
            print(Constants.ORACLE_ERROR.format(process=Constants.CREATE_NOTIFICATION_PROCESS, id=model.user_id), error)
            raise CreateNotificationException(Constants.CREATE_NOTIFICATION_ERROR)
        except Exception as error:
            print(Constants.CREATE_NOTIFICATION_ERROR, error)
            raise CreateNotificationException(Constants.CREATE_NOTIFICATION_ERROR)
        finally:
            cursor.close()  

    def update_read_value(self, notification_ids: List[int]) -> str:
        """
        Update the read status  of multiple notifications.
        
        Args:
            notification_ids: List of notifications IDs to update read status
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
                    
        cursor = self.cursor()
        try:
            placeholders = ', '.join([f':{i+1}' for i in range(len(notification_ids))])
            sql = f"""UPDATE notifications 
                     SET status = 'read'
                     WHERE id IN ({placeholders})"""
            
            cursor.execute(sql, tuple(notification_ids))
            rows_affected = cursor.rowcount
            
            self.commit()
            if rows_affected==len(notification_ids):
                return Constants.UPDATE_READ_STATUS_SUCESFULLY.format(rows_affected=rows_affected)
            return Constants.UPDATE_READ_STATUS_ERROR
            
        except oracledb.Error as error:
            print(Constants.ORACLE_ERROR.format(process=Constants.UPDATE_NOTIFICATION_PROCESS, id=Constants.MULTIPLE), error)
            raise UpdateReadStatusException(Constants.UPDATE_READ_STATUS_ERROR)
        except Exception as error:
            print(f"{Constants.UPDATE_READ_STATUS_ERROR}: {str(error)}")
            raise UpdateReadStatusException(Constants.UPDATE_READ_STATUS_ERROR)
        finally:
            cursor.close()

    @staticmethod
    def get_notifications_dict(results: List[tuple]) -> List[Dict[str, Any]]:
        """
        Convert a list of tuples to a list of dictionaries with notification data.
        
        Args:
            results: List of tuples with notification data

        Returns:
            List of dictionaries with notification data
        """
        notifications = []
        for row in results:
            message_content = row[2].read() if row[2] else None
            notification_dict = {
                'id': row[0],
                'user_id': row[1],
                'message': message_content,
                'read': row[3] == 'read'
            }
            notifications.append(notification_dict)
        
        return notifications

            
        