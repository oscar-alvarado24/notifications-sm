from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from app.config import init_database, get_db_connection
from app.repository.NotificationsRepository import NotificationRepository
from app.service.NotificationsService import NotificationService
from app.helper.exception import NotificationNotFoundException, GetNotificationsException, CreateNotificationException, UpdateReadStatusException, DeleteNotificationException
from app.model.Notification import Notification
from app.helper.Constants import Constants

app = Flask(__name__) 

init_database()

# Configurar cierre limpio de la aplicación
@app.teardown_appcontext
def close_db(error):
    """Cierra la conexión al final de cada request"""
    pass

def get_notification_service():
    """Factory function para crear el servicio con una nueva conexión"""
    connection = get_db_connection()
    repository = NotificationRepository(connection)
    return NotificationService(repository)
# Endpoint for create a notifications 
@app.route('/notifications', methods=['POST']) 
def create_notification(): 
    try:
        data = request.get_json()  # Esto lanza excepción si el cuerpo está vacío
    except BadRequest as error:
        # Captura específicamente el error de JSON vacío
         return jsonify({
            "success": False,
            "error": Constants.BAD_BODY_ERROR,
            "type": error.name
        }), 400
    if not data:
        return jsonify({
            "success": False,
            "error": Constants.BODY_EMPTY_ERROR,
            "type": BadRequest.name
        }), 400

    notification_service = get_notification_service()

    try:
        notification_data = Notification.from_dict(data)
        notification = notification_service.create_notification(notification_data)
        return jsonify({
            "success": True,
            "notifications": notification
        }), 201 
    except CreateNotificationException as exception:
         return jsonify({
            "success": False,
            "error": exception.mensaje,
            "type": exception.name
        }), 500
    except Exception as exception: 
        print(f"Error inesperado al crear la notificación: {exception}")
        return jsonify({
            "success": False,
            "error": 'Error inesperado al crear la notificación',
            "type": Constants.EXCEPTION_DEFAULT_NAME
        }), 500

# Endpoint for get notifications by user
@app.route('/notifications/<int:user_id>', methods=['GET']) 
def get_notifications(user_id): 
    try:
        notification_service = get_notification_service()
        notifications = notification_service.find_all_notifications_by_user(user_id)
        return jsonify({
            "success": True,
            "notifications": [n.json for n in notifications],
        }), 200
    except NotificationNotFoundException as exception:
        return jsonify({
            "success": False,
            "error": exception.mensaje,
            "type": exception.name
        }), 404
    except GetNotificationsException as exception:
        return jsonify({
            "success": False,
            "error": exception.mensaje,
            "type": exception.name
        }), 500
    except Exception as exception:
        print(f"Error inesperado al obtener las notificaciones: {exception}")
        return jsonify({
            "success": False,
            "error": Constants.UNEXPECTED_ERROR,
            "type": Constants.EXCEPTION_DEFAULT_NAME
        }), 500

# Endpoint to get unread notifications by user
@app.route('/notifications/unread/<int:user_id>', methods=['GET'])
def get_unread_notifications(user_id):
    try:
        notification_service = get_notification_service()
        notifications = notification_service.get_notification_with_status_unread(user_id)
        return jsonify({
            "success": True,
            "notifications": [n.json for n in notifications],
        }), 200
    except NotificationNotFoundException as e:
        return jsonify({
            "success": False,
            "error": e.mensaje,
            "type": e.name
        }), 404
    except GetNotificationsException as e:
        return jsonify({
            "success": False,
            "error": e.mensaje,
            "type": e.name
        }), 500
    except Exception as e:
        print(f"Error inesperado al obtener las notificaciones: {e}")
        return jsonify({
            "success": False,
            "error": Constants.UNEXPECTED_ERROR,
            "type": Constants.EXCEPTION_DEFAULT_NAME
        }), 500
    
# Endpoint for delete a notifications
@app.route('/notifications/<int:id>', methods=['DELETE'])
def delete_notification(id):
    try:
        notification_service = get_notification_service()
        result = notification_service.delete_notification(id)
        return jsonify({
            "success": True,
            "message": result
        }), 200
    except DeleteNotificationException as e:
        return jsonify({
            "success": False,
            "error": e.mensaje,
            "type": e.name
        }), 500
    except Exception as e:
        print(f"Error inesperado al eliminar las notificaciones: {e}")
        return jsonify({
            "success": False,
            "error": Constants.UNEXPECTED_ERROR,
            "type": Constants.EXCEPTION_DEFAULT_NAME
        }), 500

# Endpoint for update read status  
@app.route('/notifications', methods=['PUT']) 
def update_notification_status(): 
    try:
        data = request.get_json()
        notification_ids = data.get('notification_ids', [])
        
        if not notification_ids:
            return jsonify({
                "success": False,
                "error": Constants.NOTIFICATION_ID_EMPTY
            }), 400
            
        if not all(isinstance(id, int) and id > 0 for id in notification_ids):
            return jsonify({
                "success": False,
                "error": Constants.NOTIFICATION_ID_SHOULD_BE_POSITIVE
            }), 400
        
        notification_service = get_notification_service()
        result = notification_service.update_read_value(notification_ids)
        return jsonify({
            "success": True,
            "message": result
        }), 200
    except UpdateReadStatusException as e:
        return jsonify({
            "success": False,
            "error": e.mensaje
        }), 500
    except Exception as e:
        print(f"Error inesperado al actualizar el estado de lectura de  las notificaciones: {e}")
        return jsonify({
            "success": False,
            "error": Constants.UNEXPECTED_ERROR
        }), 500
