# Constantes globales
import cv2

DIRECTORIO_GRABACIONES = "Grabaciones_Caidas"
fall_threshold = 300
slow_motion_threshold = 0.7
torso_inclination_threshold = 60
leg_angle_threshold = 140
destinatario_email = "destinatario@ejemplo.com"
sala = "Sala 1"
lista_numeros = "+5491100000000"

def obtenerParametros():
    return fall_threshold, slow_motion_threshold, torso_inclination_threshold, leg_angle_threshold, destinatario_email, sala, lista_numeros

def actualizarParametros(fall, slow, torso, leg, email, room, numeros):
    global fall_threshold, slow_motion_threshold, torso_inclination_threshold, leg_angle_threshold, destinatario_email, sala, lista_numeros
    fall_threshold = fall
    slow_motion_threshold = slow
    torso_inclination_threshold = torso
    leg_angle_threshold = leg
    destinatario_email = email
    sala = room
    lista_numeros = numeros

# Función para centrar texto
def centrarTexto(img, texto, y_pos, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.7, color=(0, 255, 0), thickness=2):
    text_size = cv2.getTextSize(texto, font, font_scale, thickness)[0]
    x_pos = (img.shape[1] - text_size[0]) // 2  # Centra en la coordenada x
    cv2.putText(img, texto, (x_pos, y_pos), font, font_scale, color, thickness)

def ajustarLuz(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    brillo_promedio = cv2.mean(gray)[0]  # Calcular brillo promedio

    if brillo_promedio < 50:  # Si es muy oscuro
        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=50)  # Ajustar brillo y contraste

    return frame