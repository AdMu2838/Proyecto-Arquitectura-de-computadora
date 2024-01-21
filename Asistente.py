import os

import speech_recognition as sr
import pyttsx3
import time
import sys
import tkinter as tk
import random
import json
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
#from Reconocimiento_senias.app import App

#CONVERTIR CADENAS DE TEXTO A AUDIO Y REPRODUCIRLAS
def texto_a_audio(comando):
    palabra = pyttsx3.init()
    palabra.say(comando)
    palabra.runAndWait()

#CAPTURA AUDIO DESDE EL MICROFONO Y ANALIZA POSIBLES ERRORES
def capturar_voz(reconocer, microfono, tiempo_ruido = 1.0):
    if not isinstance(reconocer, sr.Recognizer):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")

    if not isinstance(microfono, sr.Microphone):
        raise TypeError("'reconocer' no es de la instacia 'Recognizer'")
    
    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration = tiempo_ruido)
        audio = reconocer.listen(fuente)

    respuesta = {
        "suceso": True,
        "error": None,
        "mensaje": None,
    }
    try:
        respuesta["mensaje"] = reconocer.recognize_google(audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla inteligible"
    return respuesta

#CONVIERTE A UNA CADENA DE TEXTO EN MINUSCULA EL AUDIO ENVIADO POR MICROFONO
def enviar_voz():
    while (1):
        palabra = capturar_voz(recognizer, microphone)
        if palabra["mensaje"]:
            break
        if not palabra["suceso"]:
            print("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <", nombre["error"],">")
            texto_a_audio("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)
        print("No pude escucharte, ¿podrias repetirlo?\n")
        texto_a_audio("No pude escucharte, ¿podrias repetirlo?")
    return palabra["mensaje"].lower()


#INICIO
if __name__ == "__main__":

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    """bienvenida = "Hola. Soy tu Asistente Virtual. Fui creada para instruirte todo respecto a la Estructura de un computador. Antes de empezar ¿Podrias decirme tu nombre?"
    texto_a_audio(bienvenida)
    
    respuesta = enviar_voz()
    time.sleep(0.5)
    print(f"Mucho gusto {respuesta}")
    texto_a_audio(f"Mucho gusto {respuesta}")"""

    os.system("cls")
    time.sleep(1)

    comienzo = "Para empezar el juego dime: JUEGO DE SEÑAS"
    texto_a_audio(comienzo)
    
    respuesta = "JUEGO"
    if respuesta == "JUEGO":
        print("juego iniciado")
        # Ruta del directorio de la carpeta RECONOCIMIENTO_SENIAS
        ruta_carpeta = "D:\4_semestre\Proyecto_Arquitectura_de_computadora\RECONOCIMIENTO_SENIAS"

        # Comando para crear y activar el entorno virtual
        comando_venv = f"{ruta_carpeta}/venv/Scripts/activate"

        # Comando para ejecutar el archivo app.py dentro del entorno virtual
        comando_app = f"python {ruta_carpeta}/app.py"

        # Ejecutar los comandos
        subprocess.run(comando_venv, shell=True)
        subprocess.run(comando_app, shell=True)
    else:
        print("nombre equivocado")
        
    
    
    
    
   