import math
import cv2
import mediapipe as mp
import time
import threading
import os
from grabar import grabarVideo
from alertas.mailAlerta import enviarAlertaMail
from alertas.wppAlerta import enviarAlertaWpp
from configuraciones.parametros import ajustarLuz, obtenerParametros,centrarTexto

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

tiempoCaido = 10

# Variables para rastrear la posición de la cabeza y el tiempo
prev_head_y = None
prev_time = None
fall_detected = False
cap = None

# Función para calcular el ángulo entre tres puntos (a, b, c)
def calcularAngulo(a, b, c):
    angulo = math.degrees(math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    return abs(angulo)

def detectarLevantarse(frame, referencia_altura_cabeza,referencia_altura_cadera):
    """
    Detecta si una persona se levanta en función de la posición de las caderas y hombros.
    
    Parámetros:
    - frame: Fotograma de la cámara.
    - referencia_altura: Altura inicial de la persona en posición sentada (calculada con las caderas).

    Retorna:
    - True si la persona se ha levantado, False si permanece sentada.
    """
    # Convertir la imagen de BGR a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultados = pose.process(frame_rgb)
    
    if resultados.pose_landmarks:
        # Obtener la posición Y de las caderas
        cabeza = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        cadera_izquierda_y = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        cadera_derecha_y = resultados.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y
        altura_actual_caderas = (cadera_izquierda_y + cadera_derecha_y) / 2


        # Comparar con la altura de referencia (ajustar este umbral si es necesario)
        if altura_actual_caderas < referencia_altura_cadera * 0.8:  # La persona está de pie si la altura es menor
            return True  # Se ha levantado
        if cabeza < referencia_altura_cabeza * 0.8:  # La persona está de pie si la altura es menor
            return True  # Se ha levantado
    return False  # Permanece sentado

# Función para iniciar la detección de caídas
def iniciarDeteccion():
    fall_threshold, slow_motion_threshold, torso_inclination_threshold, leg_angle_threshold, destinatario_email, sala, lista_numeros = obtenerParametros()
    global prev_head_y, prev_time, fall_detected, cap
    cap = cv2.VideoCapture(0)
   
    # # Establecer ventana de captura en pantalla completa
    # cv2.namedWindow('Detector de Caidas', cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty('Detector de Caidas', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        referencia_altura = None
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (800, 600))  # Ajusta 800x600 según el tamaño deseado
        frame = ajustarLuz(frame)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        # Obtener la fecha y hora actual en tiempo real
        current_time_str = time.strftime("%d/%m/%Y %H:%M:%S")
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Mostrar la fecha y hora actual en el centro superior
            centrarTexto(frame, current_time_str, 20) # centrarTexto(frame, f"Fecha y Hora: {current_time_str}", 20)
            centrarTexto(frame, sala, 40) # centrarTexto(frame, f"Sala: {sala}", 40)

            # Detección de caídas
            cabeza = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
            cadera_derecha = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            rodilla_derecha = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            cadera_izquierda = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            rodilla_izquierda = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]

            inclinacion_torso = calcularAngulo(cabeza, cadera_derecha, cadera_izquierda)
            angulo_pierna_derecha = calcularAngulo(cadera_derecha, rodilla_derecha, results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE])
            angulo_pierna_izquierda = calcularAngulo(cadera_izquierda, rodilla_izquierda, results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE])

            head_y = cabeza.y * frame.shape[0]
            current_time = time.time()

            if prev_head_y is not None and prev_time is not None:
                time_diff = current_time - prev_time
                position_change = abs(prev_head_y - head_y)
                velocity = position_change / time_diff

                if (velocity > fall_threshold and velocity > slow_motion_threshold and 
                                    inclinacion_torso > torso_inclination_threshold and 
                                    (angulo_pierna_derecha < leg_angle_threshold or angulo_pierna_izquierda < leg_angle_threshold)):
                                    
                    centrarTexto(frame, 'Caída detectada!', 50, font_scale=1, color=(0, 0, 255))
                    fall_detected = True
                    ruta_video = grabarVideo(cap, sala)
                    threading.Thread(target=enviarAlertaMail, args=(ruta_video, sala, current_time_str, destinatario_email)).start()
                    #fall_detected = False

                    start_time = time.time()  # Inicializa el tiempo al detectar la caída
                    # referencia_altura_cabeza = cabeza.y
                    # referencia_altura_cadera = (cadera_izquierda.y + cadera_derecha.y) / 2

                    while fall_detected and start_time is not None:

                        cabeza = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
                        cadera_derecha = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                        rodilla_derecha = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
                        cadera_izquierda = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                        rodilla_izquierda = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
                        referencia_altura_cabeza = cabeza.y
                        referencia_altura_cadera = (cadera_izquierda.y + cadera_derecha.y) / 2
                        
                        ret, frame = cap.read()
                        if not ret:
                            break

                        levantado = detectarLevantarse(frame, referencia_altura_cabeza, referencia_altura_cadera)

                        if levantado:
                            print("Se levantó")
                            centrarTexto(frame, 'Se levantó!', 50, font_scale=1, color=(0, 255, 0))
                            fall_detected = False
                        elif time.time() - start_time >= tiempoCaido:
                            print("Enviando alerta por WPP")
                            enviarAlertaWpp(sala, current_time_str, lista_numeros, destinatario_email)
                            fall_detected = False

            prev_head_y = head_y
            prev_time = current_time

        cv2.imshow('Detector de Caidas', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()