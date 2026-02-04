import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def enviarAlertaMail(ruta_video, sala, fecha_hora, destinatario):
    remitente = "introduzca su mail de google"
    password = "introduzca su contraseña de google (formato: **** **** **** ****)"

    # Crear el correo
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = "Alerta de caída"

    body = f"Se ha detectado una posible caída en {sala} el {fecha_hora}. Por favor, verifique la situación."
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Adjuntar el archivo de video
    try:
        with open(ruta_video, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(ruta_video))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ruta_video)}"'
            msg.attach(part)
    except Exception as e:
        print(f"Error al adjuntar el video: {e}")

    # Enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        text = msg.as_string()
        server.sendmail(remitente, destinatario, text)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:

        print(f"Error al enviar correo: {e}")
