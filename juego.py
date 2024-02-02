import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import itertools
import copy
from datetime import datetime
import requests
from ahorcado import JuegoTk
from ClaseJuego import ClaseJuego

class Juego:
    def __init__(self):
        # Inicialización de variables y configuración inicial
        self.ahorcado = JuegoTk()
        self.ObjetoJuego=ClaseJuego()
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.cap = cv2.VideoCapture(0)
        self.keypoint_classifier_labels = []
        self.letter = None
        self.EntradaTexto = None
        self.Texto1 = None
        self.Texto2 = None
        self.palabra_aleatoria_label = None
        self.resultado_label = None
        self.canvas_ahorcado = None
        self.EstamosJugando=False
        self.count = 0
    
    
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
                    print(f"hand_sign_id: {hand_sign_id}")
                    print(f"len(self.keypoint_classifier_labels): {len(self.keypoint_classifier_labels)}")
                    if 0 <= hand_sign_id < len(self.keypoint_classifier_labels):
                        cur = self.keypoint_classifier_labels[hand_sign_id]
                        if cur == self.prev:
                            self.letter.configure(text=cur)
                        elif cur:
                            self.prev = cur
                        
                        #self.comparar(cur, self.palabra_aleatoria_label.get("text"))
                    else:
                        print("Invalid hand_sign_id:", hand_sign_id)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = cv2.flip(frame, 1)
            captured_image = Image.fromarray(frame)
            my_image = ctk.CTkImage(dark_image=captured_image, size=(340, 335))
            self.video_lable.configure(image=my_image)
            self.video_lable.after(10, self.open_camera1)
    
    def change_text(self):
        self.palabra_aleatoria_label.configure(text=requests.get("https://random-word-api.herokuapp.com/word?number=1").json()[0])
        #self.palabra_aleatoria_label.configure(text="C")
    
    # def comparar(self, cur, letra):
    #     if cur == letra:
    #         self.resultado_label.configure(text="CORRECTO")
    #     elif cur:
    #         self.resultado_label.configure(text="INCORRECTO")
    #         self.count += 1
    #         self.__Dibujo()
    #         #self.dibujar_ahorcado(self.canvas_ahorcado, self.count)
    def JuegoNuevo(self):
        self.EstamosJugando=True
        self.ObjetoJuego.nuevojuego()
        self.EntradaTexto.focus_set()
        self.__ActualizarVista()

    def BotonEnviar(self):
        if self.EstamosJugando:
            self.ObjetoJuego.jugar(self.EntradaTexto.get())
            if self.ObjetoJuego.getVictoria() or not(self.ObjetoJuego.getJugadorEstaVivo()):
                self.EstamosJugando=False
            self.__ActualizarVista()
        else:
            self.JuegoNuevo()
        self.EntradaTexto.delete(0,"end")    

    def __ActualizarVista(self):
        if self.EstamosJugando:
            letrero=""
            for x in self.ObjetoJuego.getLetrero(): letrero+=x+" "
            self.Texto1.configure(letrero)
            mensaje="Tus jugadas: "
            for x in self.ObjetoJuego.getLetrasUsadas():mensaje+=x
            self.Texto2.configure(mensaje)
        else:
            if self.ObjetoJuego.getVictoria():
                self.Texto1.configure("¡Felicidades Has ganado! :) ")
                self.Texto2.configure("La palabra es "+self.ObjetoJuego.getPalabra())
            else:
                self.Texto1.configure("Lo siento, perdiste :( ")
                self.Texto2.configure("La palabra era "+self.ObjetoJuego.getPalabra())
        self.__Dibujo()        

    def __Dibujo(self):
        if self.EstamosJugando:
            oportunidades=self.ObjetoJuego.getOportunidades()
            if oportunidades==1:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
                self.canvas_ahorcado.create_line(150,120,110,180,width=5,fill="white")#brazo1
                self.canvas_ahorcado.create_line(150,120,190,180,width=5,fill="white")#brazo2
                self.canvas_ahorcado.create_line(150,190,110,250,width=5,fill="white")#pierna1
            elif oportunidades==2:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
                self.canvas_ahorcado.create_line(150,120,110,180,width=5,fill="white")#brazo1
                self.canvas_ahorcado.create_line(150,120,190,180,width=5,fill="white")#brazo2
            elif oportunidades==3:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
                self.canvas_ahorcado.create_line(150,120,110,180,width=5,fill="white")#brazo1
            elif oportunidades==4:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
            elif oportunidades==5:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
            else:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
 
        else:
            if self.ObjetoJuego.getVictoria():
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
                self.canvas_ahorcado.create_line(150,130,100,80,width=5,fill="white")#brazo1
                self.canvas_ahorcado.create_line(150,130,200,80,width=5,fill="white")#brazo2
                self.canvas_ahorcado.create_line(150,190,110,250,width=5,fill="white")#pierna1
                self.canvas_ahorcado.create_line(150,190,190,250,width=5,fill="white")#pierna2
            else:
                self.canvas_ahorcado.delete("all")
                self.canvas_ahorcado.create_line(40,280,40,30,150,30,150,70,width=5,fill="white")#horca
                self.canvas_ahorcado.create_line(20,290,20,280,280,280,280,290,width=5,fill="white")#horca
                self.canvas_ahorcado.create_oval(130,70,170,110,width=5,fill="dark green",outline="white")#cabeza
                self.canvas_ahorcado.create_line(150,110,150,190,width=5,fill="white")#torso
                self.canvas_ahorcado.create_line(150,120,110,180,width=5,fill="white")#brazo1
                self.canvas_ahorcado.create_line(150,120,190,180,width=5,fill="white")#brazo2
                self.canvas_ahorcado.create_line(150,190,110,250,width=5,fill="white")#pierna1
                self.canvas_ahorcado.create_line(150,190,190,250,width=5,fill="white")#pierna2