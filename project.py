import speech_recognition as sr
import pyttsx3
import time
import sys
import tkinter as tk
import random
import json
from tkinter import messagebox
from PIL import Image, ImageTk

import pyttsx3
import speech_recognition as sr

from camera_senias import Camera

# Inicializa la instancia de pyttsx3 fuera de la función
motor_voz = pyttsx3.init()

# Convierte cadenas de texto a audio y reproduce
def texto_a_audio(comando):
    global motor_voz
    motor_voz.say(comando)
    motor_voz.runAndWait()

# Captura audio desde el micrófono y analiza posibles errores
def capturar_voz(reconocer, microfono, tiempo_ruido=1.0):
    if not isinstance(reconocer, sr.Recognizer):
        raise TypeError("'reconocer' no es una instancia de 'Recognizer'")

    if not isinstance(microfono, sr.Microphone):
        raise TypeError("'microfono' no es una instancia de 'Microphone'")

    with microfono as fuente:
        reconocer.adjust_for_ambient_noise(fuente, duration=tiempo_ruido)
        audio = reconocer.listen(fuente)

    respuesta = {"suceso": True, "error": None, "mensaje": None}
    try:
        respuesta["mensaje"] = reconocer.recognize_google(audio, language="es-PE")
    except sr.RequestError:
        respuesta["suceso"] = False
        respuesta["error"] = "API no disponible"
    except sr.UnknownValueError:
        respuesta["error"] = "Habla ininteligible"
    return respuesta

# Convierte a una cadena de texto en minúscula el audio enviado por el micrófono
def enviar_voz():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        palabra = capturar_voz(recognizer, microphone)
        
        if palabra["suceso"] and palabra["mensaje"]:
            return palabra["mensaje"].lower()

        if not palabra["suceso"]:
            print(f"\nAlgo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado. <{palabra['error']}>")
            texto_a_audio("Algo no está bien. No puedo reconocer tu micrófono o no lo tienes enchufado.")
            exit(1)

        print("\nNo pude escucharte, ¿podrías repetirlo?")
        texto_a_audio("No pude escucharte, ¿podrías repetirlo?")


#BASE DE DATOS DONDE SE ENCUENTRA TODA LA INFORMACION CONCERNIENTE

#with open('basedatos.json', 'r') as archivo:       aun no lo usamos
#    datos = json.load(archivo)

#Acceder a la parte especifica que se desea imprimir


#INICIO
if __name__ == "__main__":

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    salir = False

    mi_camara = Camera()

    #PRIMERA PARTE (SALUDO Y NOMBRE)
    print("\nSALUDO:")
    bienvenida = "Hola. Soy tu Asistente Virtual. Fui creada para instruirte sobre el lenguaje de señas. Antes de empezar ¿Podrias decirme tu nombre?"
    texto_a_audio(bienvenida)
    print("Di tu nombre: ")
    nombre = enviar_voz()
    text = f"Hola {nombre}, mucho gusto"
    print(text)
    texto_a_audio(text)


    #SEGUNDA PARTE (INTRODUCCION)
    print("\nINTRODUCCIÓN:")
    concepto = "El lenguaje de señas es un sistema de comunicación que utiliza gestos, movimientos de manos y expresiones faciales para transmitir mensajes, especialmente diseñado para personas con discapacidad auditiva."
    print(concepto)
    texto_a_audio(concepto)


    #TERCERA PARTE (OPCIONES)
    print("\nOPCIONES:")

    #text = f"{nombre} ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger."
    #print(text)
    #texto_a_audio(text)

    text = (
    "\n 1) Aprendizaje"
    "\n 2) Test"
    "\n 3) Juego"
    "\n 4) Juego de señas"
    )
    print(text)
    texto_a_audio(text)

    """text = (
        "\n La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador."
        "\n La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes."
        "\n Y por último, la tercer opción, es Juego, donde tambien podrás demostrar lo que aprendiste jugando."
    )"""
    #print(text)
    #texto_a_audio(text)

    text = "¿Qué opción eliges?"
    print(text)
    texto_a_audio(text)
    time.sleep(0.5)
    """texto_a_audio("¿Aprendizaje? ¿Tests? ¿Juegos? ¿Juego de señas?")
    print("dime")"""
    texto_a_audio("dime")

    
    
    while True:
        respuesta = enviar_voz()
        print("Tu respuesta " + respuesta)

        text = f"\nElegiste la opción de {respuesta}"

        

        if respuesta in ["aprendizaje", "test", "juego"]:
            print(text)
            texto_a_audio(text)

            if respuesta == "aprendizaje":
                print("hola mundo")

            elif respuesta == "test":
                print("hola mundo")
            
            elif respuesta == "juego":
                print("\n INICIALIZANDING...")
                mi_camara.ejecutar()

            break
        
        else:
            text = (
                f"{nombre} creo que no has respondido con alguna de las instrucciones indicadas anteriormente."
                "\nResponde con una de las alternativas mencionadas."
            )
            print(text)
            texto_a_audio(text)

    