"""from asistente import AsistenteVoz


class Aprendizaje(AsistenteVoz):

    def __init__(self):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()
        print("...probando aprendizaje")

    def ejecutar(self):
        print("Hola mundo")
        self.texto_a_audio("Hola mundo")
        #self.capturar_voz();




#Para ejecutar sin necesidad de usar project.py
prueba = Aprendizaje()
prueba.ejecutar()"""
import time
from asistente import AsistenteVoz
import customtkinter as ctk
import csv
from PIL import Image, ImageTk
from model import KeyPointClassifier
from os import listdir
from os.path import isfile, join
from itertools import cycle

from test import Test

class Aprendizaje(AsistenteVoz):
    def __init__(self, callback):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()
        self.callback = callback
        # Inicialización de variables y configuración inicial
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.keypoint_classifier_labels = []
        self.letter = None

        # Nueva variable para almacenar la lista de imágenes
        self.abecedario_path = "AbecedarioSeñas/"
        self.image_files = [f for f in listdir(self.abecedario_path) if isfile(join(self.abecedario_path, f))]
        self.image_cycle = cycle(self.image_files)

        # Variable para almacenar la imagen actual
        self.current_image = None

        self.static_image_label = None

    def mostrar_ventana_aprendizaje(self):
        # Load the KeyPointClassifier model
        self.keypoint_classifier = KeyPointClassifier()

        # Read labels from a CSV file
        with open('model/keypoint_classifier/label.csv', encoding='utf-8-sig') as f:
            keypoint_classifier_labels_reader = csv.reader(f)
            self.keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels_reader]

        # Set the appearance mode and color theme for the custom tkinter library
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Create the main window
        window = ctk.CTk()
        window.geometry('1080x1080')
        window.title("APRENDIZAJE")

        # Create the main frame
        main_frame = ctk.CTkFrame(master=window, height=770, corner_radius=8)
        main_frame.pack(fill=ctk.X, padx=(10, 10), pady=(5, 0))

        # Create the title label
        title = ctk.CTkFont(family='Consolas', weight='bold', size=25)
        Label = ctk.CTkLabel(
            window,
            text='APRENDIZAJE',
            fg_color='steelblue',
            text_color='white',
            height=40,
            font=title,
            corner_radius=8
        )
        Label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 4), padx=(10, 10))

        # Create the video frame
        video_frame = ctk.CTkFrame(master=main_frame, height=340, width=365, corner_radius=12)
        video_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE, padx=(10, 10), pady=(10, 5))

        # Crear la imagen inicial
        initial_image_path = join(self.abecedario_path, self.image_files[0])
        self.current_image = Image.open(initial_image_path)
        self.current_image = ImageTk.PhotoImage(self.current_image)
        self.static_image_label = ctk.CTkLabel(master=video_frame, image=self.current_image)
        self.static_image_label.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))

        # Create a button to start the camera feed (replace this with your text)
        Button_feed_start = ctk.CTkButton(master=main_frame, text='NEXT', height=40, width=250, border_width=0,
                                           corner_radius=12, command=lambda: self.mostrarImagen())
        Button_feed_start.pack(side=ctk.TOP, pady=(5, 10))
        Button_back_to_options = ctk.CTkButton(master=main_frame, text='Volver a Opciones', height=40, width=250,
                                           border_width=0, corner_radius=12, command=lambda: self.cerrar_ventana_aprendizaje(window))
        Button_back_to_options.pack(side=ctk.TOP, pady=(5, 10))
        # Create a frame for the letter display
        letter_frame = ctk.CTkFrame(master=main_frame, height=375)
        letter_frame.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Create a font for displaying letters
        myfont = ctk.CTkFont(family='Consolas', weight='bold', size=200)
        self.letter = ctk.CTkLabel(letter_frame, font=myfont, fg_color='#2B2B2B', justify=ctk.CENTER)
        self.letter.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        self.letter.configure(text='A')

        # Create a textbox for displaying a sentence
        sentence_frame = ctk.CTkFrame(master=window, height=175, corner_radius=12)
        sentence_frame.pack(fill=ctk.X, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Create a textbox for displaying a sentence
        Sentence = ctk.CTkTextbox(sentence_frame, font=("Consolas", 24))
        Sentence.pack(fill=ctk.X, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Start the tkinter main loop
        window.mainloop()

    def mostrarImagen(self):
        # Reproduce el mensaje antes de cambiar la imagen
        # self.texto_a_audio("Siguiente letra")

        # Ocultar el texto antes de cambiar la imagen
        self.static_image_label.configure(text='')

        # Cambiar la imagen al siguiente en la lista
        next_image = next(self.image_cycle)
        image_path = join(self.abecedario_path, next_image)

        # Cambiar la imagen en la variable de imagen actual
        self.current_image = Image.open(image_path)
        self.current_image = ImageTk.PhotoImage(self.current_image)
        self.static_image_label.configure(image=self.current_image)
        self.static_image_label.image = self.current_image

        # Redimensionar la imagen al tamaño fijo
        resized_image = Image.open(image_path).resize((250, 250))
        self.current_image = ImageTk.PhotoImage(resized_image)
        self.static_image_label.configure(image=self.current_image)
        self.static_image_label.image = self.current_image

        # Cambiar el texto a la letra correspondiente
        letra = next_image.split(".")[0]
        self.letter.configure(text=letra)

        # Verificar si hemos alcanzado la última letra
        if letra == 'Z':
            # Cambiar el texto a "END"
            self.letter.configure(text='END')

            # Después de 2 segundos, cerrar la ventana y volver al asistente virtual
            self.static_image_label.after(2000, self.cerrar_ventana_aprendizaje)

    def cerrar_ventana_aprendizaje(self):
        # Destruir la ventana de aprendizaje
        self.static_image_label.master.master.destroy()

        # Volver al asistente virtual
        self.volver_al_asistente_virtual()

    def volver_al_asistente_virtual(self):
        # Agrega el código para volver al asistente virtual y ofrecer opciones adicionales
        self.texto_a_audio("Terminaste la fase de aprendizaje. Ahora voy a explicarte sobre las otras opciones que tiene este programa. Tienes 2 opciones para escoger.")
        text = (
        "\n 1) Test"
        "\n 2) Juego"
        )
        print(text)
        self.texto_a_audio(text)

        text = (
            "\n La opción Test es donde podrás poner en práctica lo que aprendiste mediante exámenes."
            "\n La opción Juego, donde también podrás demostrar lo que aprendiste jugando."
        )
        print(text)
        self.texto_a_audio(text)

        text = "¿Qué opción eliges?"
        print(text)
        self.texto_a_audio(text)
        time.sleep(0.5)
        self.texto_a_audio("¿Tests? o ¿Juego?")
        print("dime")
        self.texto_a_audio("dime")

        while True:
            respuesta = self.enviar_voz()
            print("Tu respuesta " + respuesta)

            text = f"\nElegiste la opción de {respuesta}"

            if respuesta in ["test", "juego"]:
                print(text)
                self.texto_a_audio(text)

                if respuesta == "test":
                    # Inicia la opción de Test
                    mi_test = Test()
                    mi_test.ejecutar()
                
                elif respuesta == "juego":
                    # Inicia la opción de Juego
                    # mi_camara = Camera()
                    # mi_camara.ejecutar()

                    # Inicia la opción de Test por el momento
                    mi_test = Test()
                    mi_test.ejecutar()
                break
    
            else:
                text = (
                    f"{self.nombre} creo que no has respondido con alguna de las instrucciones indicadas anteriormente."
                    "\nResponde con una de las alternativas mencionadas."
                )
                print(text)
                self.texto_a_audio(text)

    def ejecutar(self):
        # self.texto_a_audio("Bienvenido a la interfaz de Aprendizaje, se mostraran el abecedario en señas, con presionar next puedes moverte a la siguiente letra")
        self.mostrar_ventana_aprendizaje()


# Para ejecutar sin necesidad de usar project.py
prueba = Aprendizaje()
prueba.ejecutar()
