
import time
from asistente import AsistenteVoz
from camera_senias import Camera
from aprendizaje import Aprendizaje
from test import Test
from juego_ia import Juego_senias

class VirtualAssistant:
    def __init__(self):
        self.asistente_voz = AsistenteVoz()
        self.mi_aprendizaje = Aprendizaje(callback=self.presentar_opciones)
        self.mi_test = Test()
        self.mi_camara = Camera()
        self.juego = Juego_senias()
    def texto_a_audio(self, comando):
        self.asistente_voz.texto_a_audio(comando)

    def capturar_voz(self):
        return self.asistente_voz.capturar_voz()

    def enviar_voz(self):
        return self.asistente_voz.enviar_voz()

    def presentar_opciones(self):
        text = "¿Qué opción eliges?"
        print(text)
        self.texto_a_audio(text)
        time.sleep(0.5)
        self.texto_a_audio("¿Aprendizaje? ¿Tests? ¿Juegos?")
        print("dime")
        self.texto_a_audio("dime")
        
        while True:
            respuesta = self.enviar_voz()
            print("Tu respuesta " + respuesta)

            text = f"\nElegiste la opción de {respuesta}"

            if respuesta in ["aprendizaje", "test", "juego"]:
                print(text)
                self.texto_a_audio(text)

                if respuesta == "aprendizaje":
                    self.mi_aprendizaje.ejecutar()

                elif respuesta == "test":
                    self.mi_test.ejecutar()

                elif respuesta == "juego":
                    print("\n INICIALIZANDING...")
                    self.juego.ejecutar()
                break

            else:
                text = (
                    f"Creo que no has respondido con alguna de las instrucciones indicadas anteriormente."
                    "\nResponde con una de las alternativas mencionadas."
                )
                print(text)
                self.texto_a_audio(text)

class VirtualAssistant:
    def __init__(self):
        self.asistente_voz = AsistenteVoz()
        self.mi_aprendizaje = Aprendizaje(callback=self.presentar_opciones)
        self.mi_test = Test()
        self.mi_camara = Camera()

    def saludar_usuario(self):
        print("\nSALUDO:")
        bienvenida = "Hola. Soy tu Asistente Virtual. Fui creada para instruirte sobre el lenguaje de señas. Antes de empezar ¿Podrías decirme tu nombre?"
        self.texto_a_audio(bienvenida)
        print("Di tu nombre: ")
        nombre = self.enviar_voz()
        text = f"Hola {nombre}, mucho gusto"
        print(text)
        self.texto_a_audio(text)
        return nombre

    def introduccion(self):
        print("\nINTRODUCCIÓN:")
        concepto = "El lenguaje de señas es un sistema de comunicación que utiliza gestos, movimientos de manos y expresiones faciales para transmitir mensajes, especialmente diseñado para personas con discapacidad auditiva."
        print(concepto)
        self.texto_a_audio(concepto)

    def opciones(self, nombre):
        print("\nOPCIONES:")
        text = f"{nombre} ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger."
        print(text)
        self.texto_a_audio(text)

        text = (
            "\n 1) Aprendizaje"
            "\n 2) Test"
            "\n 3) Juego"
        )
        print(text)
        self.texto_a_audio(text)

        text = (
            "\n La opción Aprendizaje es donde podrás aprender todo con respecto al lenguaje de señas."
            "\n La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes."
            "\n Y por último, la tercer opción, es Juego, donde también podrás demostrar lo que aprendiste jugando."
        )
        print(text)
        self.texto_a_audio(text)

    def ejecutar_programa(self):
        nombre = self.saludar_usuario()
        self.introduccion()
        self.opciones(nombre)
        self.presentar_opciones()

        
# Usage
if __name__ == "__main__":
    virtual_assistant = VirtualAssistant()
    virtual_assistant.ejecutar_programa()
