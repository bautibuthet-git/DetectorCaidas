import time
import psutil
import pywhatkit
from tkinter import messagebox
import os

# Función para limpiar el número, eliminando espacios, guiones y otros caracteres no numéricos
def limpiar_numero(numero):
    # Elimina espacios, guiones o paréntesis
    numero = numero.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    # Asegúrate de que el número tenga el formato adecuado con el prefijo "+"
    if not numero.startswith('+'):
        numero = f"+{numero}"
    return numero

# Función para enviar el mensaje de WhatsApp a múltiples destinatarios
def enviarAlertaWpp(sala, fecha_hora, lista_numeros, email):
    mensaje = f"🚨 Se ha detectado una posible caída en {sala} el {fecha_hora}. Por favor, verifique la situación. Se envió un mail con el video adjunto a {email}."

    try:
        for numero in lista_numeros:
            # Limpia el número de teléfono antes de enviarlo
            numero_limpio = limpiar_numero(numero)
            pywhatkit.sendwhatmsg_instantly(numero_limpio, mensaje)
            time.sleep(17)
            # Cierra todas las ventanas de Microsoft Edge o Chrome si usa Chrome
            for proceso in psutil.process_iter(['name']):
                if proceso.info['name'] == 'msedge.exe':
                    os.system("taskkill /im msedge.exe /f")
                    print("Microsoft Edge ha sido cerrado.")
                    break
                elif proceso.info['name'] == 'chrome.exe':
                    os.system("taskkill /im chrome.exe /f")
                    print("Google Chrome ha sido cerrado.")
                    break
                
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

