import tkinter as tk
from tkinter import scrolledtext
from asistente import AsistenteVoz
from aprendizaje import Aprendizaje
from test import Test
from juego_ia import Juego_senias

class VirtualAssistantGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Asistente Virtual")
        self.root.geometry("600x400")

        self.asistente_voz = AsistenteVoz()
        self.mi_aprendizaje = Aprendizaje(callback=self.presentar_opciones)
        self.mi_test = Test(callback=self.presentar_opciones)

        self.mostrar_ventana_asistente()

    def mostrar_ventana_asistente(self):
        self.root.configure(bg="#2B2B2B")  # Fondo negro
        title_label = tk.Label(self.root, text="Juego Interactivo de Señas con Asistente Virtual", font=("Consolas", 16), pady=20, fg="steelblue", bg="#2B2B2B")
        title_label.pack()

        iniciar_button = tk.Button(self.root, text="Iniciar", command=self.iniciar_asistente, height=2, width=15, font=("Consolas", 12), fg="white", bg="steelblue")
        iniciar_button.pack()

    def iniciar_asistente(self):
        self.root.destroy()  # Cerrar la ventana inicial
        self.root = tk.Tk()
        self.root.title("Asistente Virtual")
        self.root.geometry("600x400")

        self.text_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=15, font=("Consolas", 12))
        self.text_box.pack(padx=10, pady=10)

        self.text_to_speech("Hola. Soy tu Asistente Virtual. Fui creada para instruirte sobre el lenguaje de señas. Antes de empezar ¿Podrías decirme tu nombre?")
        self.root.after(1000, self.saludar_usuario)

    def text_to_speech(self, text):
        self.text_box.insert(tk.END, f"{text}\n")
        self.text_box.see(tk.END)
        self.asistente_voz.texto_a_audio(text)

    def saludar_usuario(self):
        self.root.after(1000, lambda: self.text_to_speech("Di tu nombre: "))
        self.root.after(2000, lambda: self.text_to_speech("dime"))
        self.root.after(3000, self.capturar_nombre)

    def capturar_nombre(self):
        nombre = self.enviar_voz()
        text = f"Hola {nombre}, mucho gusto"
        self.text_to_speech(text)
        self.root.after(1000, self.introduccion)

    def introduccion(self):
        concepto = "El lenguaje de señas es un sistema de comunicación que utiliza gestos, movimientos de manos y expresiones faciales para transmitir mensajes, especialmente diseñado para personas con discapacidad auditiva."
        self.text_to_speech(concepto)
        self.root.after(1000, self.opciones)

    def opciones(self):
        text = (
            "\n 1) Aprendizaje"
            "\n 2) Test"
            "\n 3) Juego"
        )
        self.text_to_speech(text)

        text = (
            "\n La opción Aprendizaje es donde podrás aprender todo con respecto al lenguaje de señas."
            "\n La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes."
            "\n Y por último, la tercer opción, es Juego, donde también podrás demostrar lo que aprendiste jugando."
        )
        self.text_to_speech(text)

        self.root.after(1000, self.presentar_opciones)

    def capturar_voz(self):
        return self.asistente_voz.capturar_voz()

    def enviar_voz(self):
        return self.asistente_voz.enviar_voz()

    def presentar_opciones(self):
        text = "¿Qué opción eliges?"
        self.text_to_speech(text)
        self.root.after(1000, lambda: self.text_to_speech("¿Aprendizaje? ¿Tests? ¿Juegos?"))
        self.root.after(2000, lambda: self.text_to_speech("dime"))
        self.root.after(3000, self.elegir_opcion)

    def elegir_opcion(self):
        respuesta = self.enviar_voz()
        text = f"\nElegiste la opción de {respuesta}"
        self.text_to_speech(text)

        if respuesta in ["aprendizaje", "prueba", "juego"]:
            if respuesta == "aprendizaje":
                self.mi_aprendizaje.ejecutar()

            elif respuesta == "prueba":
                self.mi_test.ejecutar()

            elif respuesta == "juego":
                self.text_to_speech("\nINICIALIZANDING...")
                self.root.after(1000, lambda: Juego_senias().ejecutar())
        else:
            text = (
                f"Creo que no has respondido con alguna de las instrucciones indicadas anteriormente."
                "\nResponde con una de las alternativas mencionadas."
            )
            self.text_to_speech(text)
            self.root.after(1000, self.presentar_opciones)

    def ejecutar_programa(self):
        self.root.mainloop()

# Usage
if __name__ == "__main__":
    virtual_assistant = VirtualAssistantGUI()
    virtual_assistant.ejecutar_programa()
