# DetectorCaidas

Sistema de Detección de Caídas (Fall Detection System) 🚨
Este proyecto consiste en una aplicación de visión computacional diseñada para monitorear en tiempo real a personas (especialmente adultos mayores o pacientes) y detectar caídas mediante el análisis de la postura corporal. Al detectar un evento, el sistema activa alertas automáticas vía Email y WhatsApp.

🚀 Características principales
Detección en Tiempo Real: Utiliza MediaPipe Pose para el rastreo de puntos clave del cuerpo.

Algoritmo de Multivarianza: Analiza velocidad de caída, inclinación del torso y ángulo de las piernas para reducir falsos positivos.

Interfaz Gráfica (GUI): Construida con Tkinter para configurar umbrales de sensibilidad, destinatarios y nombres de salas.

Alertas Duales: 
Email: Envía un correo con el video adjunto de los 5 segundos posteriores a la caída.
WhatsApp: Envía mensajes instantáneos a múltiples destinatarios si la persona no se levanta tras 10 segundos.

Grabación Automática: Almacena clips de video de los eventos detectados en una carpeta local.

Ajuste de Luz: Algoritmo básico para mejorar el contraste en condiciones de baja iluminación.

📋 Requisitos e Instalación
1. Clonar el repositorio
2. Instalar dependencias: pip install opencv-python mediapipe pywhatkit psutil

Configuración de Email: El sistema utiliza una cuenta de Gmail para enviar alertas. Debes configurar una "Contraseña de Aplicación" en tu cuenta de Google para que el script enviarAlertaMail pueda autenticarse.

🖥️ Uso de la Aplicación
Ejecuta el archivo principal (donde se encuentra inicioInterfaz): python main.py
Configurar Parámetros: En la ventana inicial, ajusta los umbrales si es necesario (velocidad, inclinación, etc.).
Destinatarios: Agrega el email y los números de WhatsApp (formato internacional, ej: +54911...).
Iniciar: Haz clic en "Iniciar Detección". Se abrirá la cámara y comenzará el monitoreo.
Salir: Presiona la tecla q en la ventana del video o haz clic en "Salir" en la interfaz.

⚠️ Notas de Seguridad y Privacidad
Este sistema es una herramienta de asistencia. No reemplaza la supervisión médica profesional. Asegúrese de contar con el consentimiento de las personas monitoreadas, ya que el sistema procesa imágenes de video y almacena grabaciones locales.
