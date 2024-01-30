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
from asistente import AsistenteVoz
import customtkinter as ctk
import csv
from PIL import Image, ImageTk
from model import KeyPointClassifier
from os import listdir
from os.path import isfile, join
from itertools import cycle

class Aprendizaje(AsistenteVoz):
    def __init__(self):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()

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

        # Cambiar el texto a la letra correspondiente
        letra = next_image.split(".")[0]
        self.letter.configure(text=letra)


    def ejecutar(self):
        self.texto_a_audio("Bienvenido a la interfaz de Aprendizaje, se mostraran el abecedario en señas, con presionar next puedes moverte a la siguiente letra")
        self.mostrar_ventana_aprendizaje()


# Para ejecutar sin necesidad de usar project.py
prueba = Aprendizaje()
prueba.ejecutar()
