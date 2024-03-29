from asistente import AsistenteVoz
import customtkinter as ctk
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join
from itertools import cycle

class Aprendizaje(AsistenteVoz):
    def __init__(self, callback):
    # def __init__(self, callback=None):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()
        self.callback = callback
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.keypoint_classifier_labels = []
        self.letter = None

        self.abecedario_path = "AbecedarioSeñas/"
        self.image_files = [f for f in listdir(self.abecedario_path) if isfile(join(self.abecedario_path, f))]
        self.image_cycle = cycle(self.image_files)
        self.current_image = None
        self.static_image_label = None

    def mostrar_ventana_aprendizaje(self):
        # Configuración de la apariencia de la interfaz gráfica
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Creación de la ventana principal
        window = ctk.CTk()
        window.geometry('1080x720')
        window.title("APRENDIZAJE")

        # Creación del marco principal dentro de la ventana
        main_frame = ctk.CTkFrame(master=window, height=770, corner_radius=8)
        main_frame.pack(fill=ctk.X, padx=(10, 10), pady=(5, 0))

        # Creación del marco para el video (inicialmente con tamaño 0)
        video_frame = ctk.CTkFrame(master=main_frame, height=0, width=0, corner_radius=0)
        video_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE, padx=(10, 10), pady=(10, 5))

        # Carga de la imagen inicial en el marco de video
        initial_image_path = join(self.abecedario_path, self.image_files[0])
        self.current_image = Image.open(initial_image_path)
        self.current_image = ImageTk.PhotoImage(self.current_image)
        self.static_image_label = ctk.CTkLabel(master=video_frame)
        self.static_image_label.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))
        self.static_image_label.configure(image=self.current_image)

        # Creación de un marco para la letra con tamaño fijo
        letter_frame = ctk.CTkFrame(master=main_frame, height=375)
        letter_frame.pack(fill=ctk.BOTH, side=ctk.TOP, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Configuración de la fuente y creación de la etiqueta para la letra
        myfont = ctk.CTkFont(family='Consolas', weight='bold', size=100)
        self.letter = ctk.CTkLabel(letter_frame, font=myfont, fg_color='#2B2B2B', justify=ctk.CENTER)
        self.letter.pack(fill=ctk.BOTH, side=ctk.TOP, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        self.letter.configure(text='A')

        # Creación de un marco para los botones en una misma línea
        button_frame = ctk.CTkFrame(master=main_frame)
        button_frame.pack(side=ctk.TOP, pady=(5, 10))

        # Creación de los botones ANTERIOR, SIGUIENTE y VOLVER A OPCIONES
        Button_feed_start_prev = ctk.CTkButton(master=button_frame, text='ANTERIOR', height=40, width=250, border_width=0,
                            corner_radius=12, command=lambda: self.mostrarImagen(anterior=True))
        Button_feed_start_prev.pack(side=ctk.LEFT, padx=(5, 5))

        Button_feed_start_next = ctk.CTkButton(master=button_frame, text='SIGUIENTE', height=40, width=250, border_width=0,
                            corner_radius=12, command=lambda: self.mostrarImagen())
        Button_feed_start_next.pack(side=ctk.LEFT, padx=(5, 5))

        Button_back_to_options = ctk.CTkButton(master=button_frame, text='Volver a Opciones', height=40, width=250,
                                        border_width=0, corner_radius=12, command=lambda: self.cerrar_ventana_aprendizaje(window))
        Button_back_to_options.pack(side=ctk.LEFT, padx=(5, 5))

        # Configuración de la fuente y creación de la etiqueta del título
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

        # Inicio del bucle principal de la interfaz gráfica
        window.mainloop()

    def mostrarImagen(self, anterior=False):
        # Limpiar el texto en la etiqueta estática
        self.static_image_label.configure(text='')

        # Obtener la siguiente o anterior imagen en la lista
        if anterior:
            prev_image = self.image_files.pop()
            self.image_files.insert(0, prev_image)
        else:
            next_image = self.image_files.pop(0)
            self.image_files.append(next_image)

        # Obtener la ruta de la imagen actual
        image_path = join(self.abecedario_path, self.image_files[0])

        # Configurar la imagen actual en la etiqueta estática
        self.current_image = Image.open(image_path)
        self.current_image = ImageTk.PhotoImage(self.current_image)
        self.static_image_label.configure(image=self.current_image)
        self.static_image_label.image = self.current_image

        # Redimensionar la imagen a un tamaño fijo
        resized_image = Image.open(image_path).resize((250, 250))
        self.current_image = ImageTk.PhotoImage(resized_image)
        self.static_image_label.configure(image=self.current_image)
        self.static_image_label.image = self.current_image

        # Obtener la letra actual del nombre del archivo
        letra = self.image_files[0].split(".")[0]

        # Convertir la letra a audio
        self.texto_a_audio(letra)

        # Configurar el texto de la letra en la etiqueta correspondiente
        self.letter.configure(text=letra)

    def cerrar_ventana_aprendizaje(self, window):
        window.destroy()
        if self.callback:
            self.callback()
        
    def ejecutar(self):
        self.texto_a_audio("Bienvenido a la interfaz de Aprendizaje, se mostraran el abecedario en señas, con presionar next puedes moverte a la siguiente letra")
        self.mostrar_ventana_aprendizaje()

"""
# Para ejecutar aprendizaje.py sin necesidad de usar project.py
prueba = Aprendizaje()
prueba.ejecutar()
# saca de comentarios esto en init -> # def __init__(self, callback=None):
"""