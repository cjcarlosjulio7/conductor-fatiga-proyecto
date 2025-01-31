from playsound import playsound
import os

# Ruta absoluta al archivo de sonido
sound_path = os.path.abspath("resources/sounds/microsleep.mp3")

if os.path.exists(sound_path):
    print(f"Reproduciendo: {sound_path}")
    playsound(sound_path)
else:
    print(f"No se encontró el archivo: {sound_path}")
