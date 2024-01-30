
import time
from asistente import AsistenteVoz
from camera_senias import Camera
from aprendizaje import Aprendizaje
from test import Test


# Inicializa la instancia de AsistenteVoz
asistente_voz = AsistenteVoz()

def texto_a_audio(comando):
    asistente_voz.texto_a_audio(comando)

def capturar_voz():
    return asistente_voz.capturar_voz()

def enviar_voz():
    return asistente_voz.enviar_voz()


#INICIO
if __name__ == "__main__":

    mi_aprendizaje = Aprendizaje()
    mi_test = Test()
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

    text = f"{nombre} ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger."
    print(text)
    texto_a_audio(text)

    text = (
    "\n 1) Aprendizaje"
    "\n 2) Test"
    "\n 3) Juego"
    )
    print(text)
    texto_a_audio(text)

    text = (
        "\n La opción Aprendizaje es donde podrás aprender todo con respecto a la Estructura de un computador."
        "\n La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes."
        "\n Y por último, la tercer opción, es Juego, donde tambien podrás demostrar lo que aprendiste jugando."
    )
    print(text)
    texto_a_audio(text)

    text = "¿Qué opción eliges?"
    print(text)
    texto_a_audio(text)
    time.sleep(0.5)
    texto_a_audio("¿Aprendizaje? ¿Tests? ¿Juegos?")
    print("dime")
    texto_a_audio("dime")
    
    
    while True:
        respuesta = enviar_voz()
        print("Tu respuesta " + respuesta)

        text = f"\nElegiste la opción de {respuesta}"

        if respuesta in ["aprendizaje", "test", "juego"]:
            print(text)
            texto_a_audio(text)

            if respuesta == "aprendizaje":
                mi_aprendizaje.ejecutar()

            elif respuesta == "test":
                mi_test.ejecutar()
            
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

    
