#!/usr/bin/env python3
"""
Archivo principal para ejecutar el microservicio de notificaciones
Colocar este archivo en la raíz del proyecto
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

if __name__ == '__main__':
    # Importar la aplicación Flask desde el controlador
    from app.controller.NotificationController import app
    
    # Obtener el puerto de las variables de entorno
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Iniciando microservicio de notificaciones...")
    print(f"🌐 Disponible en: http://localhost:{port}")
    print("📋 Endpoints disponibles:")
    print("   POST   /notifications                    - Crear notificación")
    print("   GET    /notifications/<user_id>         - Obtener notificaciones")
    print("   GET    /notifications/unread/<user_id>   - Notificaciones no leídas")
    print("   DELETE /notifications/<id>              - Eliminar notificación")
    print("   PUT    /notifications                    - Marcar como leídas")
    print("\n🛑 Presiona Ctrl+C para detener el servicio\n")
    
    # Ejecutar la aplicación
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)