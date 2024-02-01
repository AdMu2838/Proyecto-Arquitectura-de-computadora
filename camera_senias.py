import customtkinter as ctk
import csv
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
from model import KeyPointClassifier
import itertools
import copy
from datetime import datetime
from ClaseJuego import ClaseJuego


class Camera:
    def __init__(self):
        # Inicialización de variables y configuración inicial
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.cap = cv2.VideoCapture(1)
        self.keypoint_classifier_labels = []
        self.letter = None

        self.juego = ClaseJuego()
        self.EstamosJugando = False
        self.window = ctk.CTk()
        self.EntradaTexto = None

    # Function to calculate the landmark points from an image
    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Iterate over each landmark and convert its coordinates
        for landmark in landmarks.landmark:
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    # Function to preprocess landmark data
    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(
            itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    # Function to open the camera and perform hand gesture recognition
    def open_camera1(self):
        width, height = 800, 600
        with mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,
                                      static_image_mode=False) as hands:
            _, frame = self.cap.read()
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            opencv_image = cv2.resize(opencv_image, (width, height))

            processFrames = hands.process(opencv_image)
            if processFrames.multi_hand_landmarks:
                for lm in processFrames.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(frame, lm, mp.solutions.hands.HAND_CONNECTIONS)

                    landmark_list = self.calc_landmark_list(frame, lm)

                    pre_processed_landmark_list = self.pre_process_landmark(landmark_list)

                    hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)

                    # print(f"hand_sign_id: {hand_sign_id}")
                    # print(f"len(self.keypoint_classifier_labels): {len(self.keypoint_classifier_labels)}")

                    if 0 <= hand_sign_id < len(self.keypoint_classifier_labels):
                        cur = self.keypoint_classifier_labels[hand_sign_id]
                        if cur == self.prev:
                            self.letter.configure(text=cur)
                            self.EntradaTexto.delete(0, 'end')  # Limpiar el texto anterior
                            self.EntradaTexto.insert(0, cur)  # Insertar el nuevo texto en la entrada
                            # print(cur)
                        elif cur:
                            self.prev = cur
                    else:
                        print("Invalid hand_sign_id:", hand_sign_id)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = cv2.flip(frame, 1)
            captured_image = Image.fromarray(frame)
            my_image = ctk.CTkImage(dark_image=captured_image, size=(340, 335))
            self.video_lable.configure(image=my_image)
            self.video_lable.after(10, self.open_camera1)

    def ejecutar(self):

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

        self.window.geometry('1380x800')
        self.window.title("AHORCADO DE SEÑAS")

        # Initialize the video capture

        width, height = 500, 500

        # Create the title label
        i = 0
        title = ctk.CTkFont(
            family='Consolas',
            weight='bold',
            size=25
        )
        Label = ctk.CTkLabel(
            self.window,
            text='AHORCADO DE SEÑAS',
            fg_color='steelblue',
            text_color='white',
            height=40,
            font=title,
            corner_radius=8)
        Label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 4), padx=(10, 10))

        # Create the main frame
        main_frame = ctk.CTkFrame(master=self.window,
                                  height=770,
                                  corner_radius=8
                                  )

        main_frame.pack(fill=ctk.X, padx=(10, 10), pady=(5, 0))
        MyFrame1 = ctk.CTkFrame(master=main_frame,
                                height=375,
                                width=365
                                )
        MyFrame1.pack(fill=ctk.BOTH, expand=ctk.TRUE, side=ctk.LEFT, padx=(10, 10), pady=(10, 10))

        # Create the video frame
        video_frame = ctk.CTkFrame(master=MyFrame1, height=340, width=365, corner_radius=12)
        video_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE, padx=(10, 10), pady=(10, 5))

        # Create the video label
        self.video_lable = ctk.CTkLabel(master=video_frame, text='', height=340, width=365, corner_radius=12)
        self.video_lable.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))

        # Create a button to start the camera feed
        Camera_feed_start = ctk.CTkButton(master=MyFrame1, text='START', height=40, width=250, border_width=0,
                                          corner_radius=12, command=lambda: self.open_camera1())
        Camera_feed_start.pack(side=ctk.TOP, pady=(5, 10))

        MyFrame2 = ctk.CTkFrame(master=main_frame,
                                height=375
                                )
        MyFrame2.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Create a font for displaying letters
        myfont = ctk.CTkFont(
            family='Consolas',
            weight='bold',
            size=200
        )
        self.letter = ctk.CTkLabel(MyFrame2,
                                   font=myfont, width=300, fg_color='#2B2B2B', justify=ctk.CENTER)
        self.letter.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        self.letter.configure(text='')

        ############################################
        ############################################
        ############################################
        ############################################

        # ESPACIO PARA LA PALABRA DEL AHORCADO Y EL LABEL

        self.Texto1 = ctk.StringVar()
        self.Texto1.set("BIENVENIDO AL JUEGO DE SEÑAS")

        Label = ctk.CTkLabel(
            self.window,
            textvariable=self.Texto1,
            fg_color='steelblue',
            text_color='white',
            height=40,
            font=title,
            corner_radius=8)

        Label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 4), padx=(10, 10))

        # SECCION DEL LABEL INTENTOS

        self.Texto2 = ctk.StringVar()
        self.Texto2.set("TEXTO RANDOM")  # Establecer el texto inicial

        myframeOportunidades = ctk.CTkFrame(master=self.window,
                                            height=175,
                                            corner_radius=12
                                            )
        myframeOportunidades.pack(fill=ctk.X, expand=ctk.TRUE)

        Label = ctk.CTkLabel(
            master=myframeOportunidades,
            textvariable=self.Texto2,
            fg_color='steelblue3',
            text_color='snow',
            height=35,
            font=('Helvetica', 20),
            corner_radius=5)

        Label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 4), padx=(10, 10))

        # SECCION BOTONES PARA NUEVO JUEGO Y SALIR

        MyFrame3 = ctk.CTkFrame(master=self.window,
                                height=175,
                                corner_radius=12
                                )
        MyFrame3.pack(fill=ctk.X, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        button_frame = ctk.CTkFrame(master=MyFrame3)
        button_frame.pack(fill=ctk.X, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        new_game_button = ctk.CTkButton(master=button_frame, text='Nuevo Juego', height=40, width=100, border_width=0,
                                        corner_radius=12, command=self.JuegoNuevo)
        new_game_button.pack(side=ctk.TOP, padx=(5, 10))

        exit_button = ctk.CTkButton(master=button_frame, text='Salir', height=40, width=100, border_width=0,
                                    corner_radius=12)
        exit_button.pack(side=ctk.BOTTOM, padx=(5, 10), pady=(5, 10))

        # ESPACIO PARA PONER EL AHORCADO

        self.Lienzo = tk.Canvas(master=main_frame, width=200, height=200, bg="blue")
        self.Lienzo.pack(fill=ctk.BOTH, side=ctk.RIGHT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        self.Dibujo()

        # ESPACIO PARA ENVIAR EL TEXTO EN FORMATO ENTRY

        MyFrame4 = ctk.CTkFrame(master=self.window,
                                height=300,
                                corner_radius=12
                                )
        MyFrame4.pack(fill=ctk.X, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        self.EntradaTexto = tk.Entry(master=MyFrame4, width=2, bg="Skyblue1", bd=6, font="Helvetica 17")

        self.window.bind("<Return>", lambda x: self.BotonEnviar())
        self.EntradaTexto.delete(0, 'end')
        self.EntradaTexto.insert(0, self.letter)

        self.EntradaTexto.pack(side=ctk.TOP, padx=(10, 10), pady=(10, 10), anchor=tk.CENTER, expand=ctk.TRUE)

        # Start the tkinter main loop
        self.window.mainloop()

    def JuegoNuevo(self):
        self.EstamosJugando = True
        self.juego.nuevojuego()
        self.EntradaTexto.focus_set()
        self.__ActualizarVista()

    def BotonEnviar(self):
        if self.EstamosJugando:
            self.juego.jugar(self.EntradaTexto.get())
            if self.juego.getVictoria() or not (self.juego.getJugadorEstaVivo()):
                self.EstamosJugando = False
            self.__ActualizarVista()
        else:
            self.JuegoNuevo()
        self.EntradaTexto.delete(0, "end")

    def __ActualizarVista(self):
        if self.EstamosJugando:
            letrero = ""
            for x in self.juego.getLetrero(): letrero += x + " "
            self.Texto1.set(letrero)
            mensaje = "Tus jugadas: "
            for x in self.juego.getLetrasUsadas(): mensaje += x
            self.Texto2.set(mensaje)
        else:
            if self.juego.getVictoria():
                self.Texto1.set("¡Felicidades Has ganado! :) ")
                self.Texto2.set("La palabra es " + self.ObjetoJuego.getPalabra())
            else:
                self.Texto1.set("Lo siento, perdiste :( ")
                self.Texto2.set("La palabra era " + self.ObjetoJuego.getPalabra())
        self.Dibujo()

    def Dibujo(self):
        if self.EstamosJugando:
            oportunidades = self.juego.getOportunidades()
            if oportunidades == 1:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
                self.Lienzo.create_line(150, 120, 110, 180, width=5, fill="white")  # brazo1
                self.Lienzo.create_line(150, 120, 190, 180, width=5, fill="white")  # brazo2
                self.Lienzo.create_line(150, 190, 110, 250, width=5, fill="white")  # pierna1
            elif oportunidades == 2:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
                self.Lienzo.create_line(150, 120, 110, 180, width=5, fill="white")  # brazo1
                self.Lienzo.create_line(150, 120, 190, 180, width=5, fill="white")  # brazo2
            elif oportunidades == 3:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
                self.Lienzo.create_line(150, 120, 110, 180, width=5, fill="white")  # brazo1
            elif oportunidades == 4:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
            elif oportunidades == 5:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
            else:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca

        else:
            if self.juego.getVictoria():
                self.Lienzo.delete("all")
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
                self.Lienzo.create_line(150, 130, 100, 80, width=5, fill="white")  # brazo1
                self.Lienzo.create_line(150, 130, 200, 80, width=5, fill="white")  # brazo2
                self.Lienzo.create_line(150, 190, 110, 250, width=5, fill="white")  # pierna1
                self.Lienzo.create_line(150, 190, 190, 250, width=5, fill="white")  # pierna2
            else:
                self.Lienzo.delete("all")
                self.Lienzo.create_line(40, 280, 40, 30, 150, 30, 150, 70, width=5, fill="white")  # horca
                self.Lienzo.create_line(20, 290, 20, 280, 280, 280, 280, 290, width=5, fill="white")  # horca
                self.Lienzo.create_oval(130, 70, 170, 110, width=5, fill="blue", outline="white")  # cabeza
                self.Lienzo.create_line(150, 110, 150, 190, width=5, fill="white")  # torso
                self.Lienzo.create_line(150, 120, 110, 180, width=5, fill="white")  # brazo1
                self.Lienzo.create_line(150, 120, 190, 180, width=5, fill="white")  # brazo2
                self.Lienzo.create_line(150, 190, 110, 250, width=5, fill="white")  # pierna1
                self.Lienzo.create_line(150, 190, 190, 250, width=5, fill="white")  # pierna2


if __name__ == "__main__":
    # Instanciar la clase Camera
    camera = Camera()

    # Ejecutar el método 'ejecutar()'
    camera.ejecutar()