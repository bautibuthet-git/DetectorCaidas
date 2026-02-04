import cv2
import os
import time
from configuraciones.parametros import DIRECTORIO_GRABACIONES, centrarTexto

# Función para grabar video en la carpeta "grabaciones de caídas" con datos
def grabarVideo(cap, sala):
    if not os.path.exists(DIRECTORIO_GRABACIONES):
        os.makedirs(DIRECTORIO_GRABACIONES)

    timestamp = time.strftime("%d.%m.%Y_%H-%M-%S")
    ruta_video = os.path.join(DIRECTORIO_GRABACIONES, f"caida_detectada_{timestamp}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(ruta_video, fourcc, 20.0, (640, 480))
    start_time = time.time()

    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if ret:
            # Mostrar la fecha y hora actual en el centro superior
            current_time = time.strftime("%d/%m/%Y %H:%M:%S")
            centrarTexto(frame, current_time, 20)
            centrarTexto(frame, sala, 40)
            out.write(frame)

    out.release()
    print(f"Video guardado en {ruta_video}")
    return ruta_video