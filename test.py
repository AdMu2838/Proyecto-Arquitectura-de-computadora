import customtkinter as ctk
import csv
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
from model import KeyPointClassifier
import itertools
import copy
import time
import random
from reporte import Reporte
from asistente import AsistenteVoz

import_interfaz = "interfaz"
interfaz = __import__(import_interfaz)

Interfaz = interfaz.Interfaz


class Test():
    # def __init__(self, callback=None):
    def __init__(self, callback):
        self.callback = callback
        self.voz = AsistenteVoz()
        self.testLetter = None
        self.point = 0
        self.miss = 0
        self.video_lable = None
        self.keypoint_classifier = None
        self.cap = cv2.VideoCapture(0)
        self.keypoint_classifier_labels = []
        self.letter = None
        self.reports = []
        self.begin = False

    def results(self, Sentence):
        sum = 0
        result_text = "\n\nRESULTADOS OBTENIDOS:\n"
        for report in self.reports:
            sum += report.result()
            result_text += str(report) + "\n"

        result_text += f"\nDado el test, el participante obtuvo un {sum/10}% de precisión."

        # Limpiar el contenido actual del CTkTextbox
        Sentence.delete(1.0, ctk.END)
        # Mostrar los resultados en el CTkTextbox
        Sentence.insert(ctk.END, result_text)

        # Apagar la cámara y cerrar la ventana después de mostrar los resultados
        if self.cap.isOpened():
            self.cap.release()

        if self.window:
            self.window.destroy()
            if self.callback:
                self.callback()

    def start_test(self, Sentence):
        abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        test = []

        while (len(test) < 11):
            letra = random.choice(abc)
            if letra not in test:
                test.append(letra)

        self.begin = True

        def show_next_letter():
            r = Reporte(self.point, self.miss, self.testLetter)
            self.reports.append(r)
            self.point = 0
            self.miss = 0
            nonlocal i
            i += 1
            self.letter.configure(text=test[i])
            self.testLetter = test[i]
            if i < 10:
                self.letter.after(10000, show_next_letter)
            else:
                self.results(Sentence)

        i = 0
        self.letter.configure(text=test[0])
        self.testLetter = test[0]
        self.letter.after(10000, show_next_letter)

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
        with mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=False) as hands:
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

                    
                    if (self.begin):
                        actualLetter = self.keypoint_classifier_labels[hand_sign_id]
                        if (actualLetter == self.testLetter):
                            self.point += 1
                        else:
                            self.miss += 1


            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = cv2.flip(frame, 1)
            captured_image = Image.fromarray(frame)
            my_image = ctk.CTkImage(dark_image=captured_image, size=(340, 335))
            self.video_lable.configure(image=my_image)
            self.video_lable.after(10, self.open_camera1)

    def mostrar_ventana_test(self):
        # Cargar el modelo KeyPointClassifier
        self.keypoint_classifier = KeyPointClassifier()

        # Leer etiquetas de un archivo CSV
        with open('model/keypoint_classifier/label.csv', encoding='utf-8-sig') as f:
            keypoint_classifier_labels_reader = csv.reader(f)
            self.keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels_reader]

        # Configuración de la apariencia de la interfaz gráfica
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Creación de la ventana principal
        window = ctk.CTk()
        window.geometry('1080x720')
        window.title("APRENDIZAJE")

        # Inicializar la captura de video
        width, height = 600, 500

        # Crear la etiqueta del título
        title = ctk.CTkFont(family='Consolas', weight='bold', size=25)
        Label = ctk.CTkLabel(window, text='HAND SIGNS', fg_color='steelblue', text_color='white',
                             height=40, font=title, corner_radius=8)
        Label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 4), padx=(10, 10))

        # Crear el marco principal
        main_frame = ctk.CTkFrame(master=window, height=770, corner_radius=8)
        main_frame.pack(fill=ctk.X, padx=(10, 10), pady=(5, 0))

        MyFrame1 = ctk.CTkFrame(master=main_frame, height=375, width=365)
        MyFrame1.pack(fill=ctk.BOTH, expand=ctk.TRUE, side=ctk.LEFT, padx=(10, 10), pady=(10, 10))

        # Crear el marco de video
        video_frame = ctk.CTkFrame(master=MyFrame1, height=340, width=365, corner_radius=12)
        video_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE, padx=(10, 10), pady=(10, 5))

        # Crear la etiqueta de video
        self.video_lable = ctk.CTkLabel(master=video_frame, text='', height=340, width=365, corner_radius=12)
        self.video_lable.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))

        # Crear un botón para volver a las opciones
        Button_back_to_options = ctk.CTkButton(master=MyFrame1, text='Volver a Opciones', height=40, width=250,
                                               border_width=0, corner_radius=12,
                                               command=lambda: self.cerrar_ventana_test(window))
        Button_back_to_options.pack(side=ctk.LEFT, padx=(5, 5))

        # Crear un botón para iniciar el test
        Camera_feed_start = ctk.CTkButton(master=MyFrame1, text='Iniciar un Test', height=40, width=250, border_width=0,
                                          corner_radius=12, command=lambda: self.start_test(Sentence))
        Camera_feed_start.pack(side=ctk.TOP, pady=(5, 10))
        self.open_camera1()

        MyFrame2 = ctk.CTkFrame(master=main_frame, height=375)
        MyFrame2.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Crear una fuente para mostrar letras
        myfont = ctk.CTkFont(family='Consolas', weight='bold', size=200)
        self.letter = ctk.CTkLabel(MyFrame2, font=myfont, fg_color='#2B2B2B', justify=ctk.CENTER)
        self.letter.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        self.letter.configure(text='')

        MyFrame3 = ctk.CTkFrame(master=window, height=175, corner_radius=12)
        MyFrame3.pack(fill=ctk.X, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Crear un cuadro de texto para mostrar una oración
        Sentence = ctk.CTkLabel(MyFrame3, font=("Consolas", 24))
        Sentence.pack(fill=ctk.X, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))

        # Iniciar el bucle principal de tkinter
        window.mainloop()
    
    def cerrar_ventana_test(self, window):
        window.destroy()
        if self.callback:
            self.callback()

    def ejecutar(self):
        # self.voz.texto_a_audio("El test consiste en probar tus conocimientos en el lenguaje de señas. Este consiste en que se te mostará una letra aleatoria y tú deberás hacer el gesto correspondiente. Son un total de 10 letras, cada una con evaluación de 10 segundos, al final se te mostrará tu precisión.")
        self.mostrar_ventana_test()

"""
# Para ejecutar test.py sin necesidad de usar project.py
prueba = Test()
prueba.ejecutar()
# saca de comentarios esto en init -> # def __init__(self, callback=None):
"""