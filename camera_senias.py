from asistente import AsistenteVoz

import customtkinter as ctk
import cv2
import mediapipe as mp
import itertools
import copy

class Camera (AsistenteVoz):
    def __init__(self):
        # Llama al constructor de la clase base (AsistenteVoz)
        super().__init__()
        # Inicialización de variables y configuración inicial
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.cap = cv2.VideoCapture(0)
        self.keypoint_classifier_labels = []
        self.letter = None
        self.palabra_aleatoria_label = None
        self.resultado_label = None
        self.canvas_ahorcado = None
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
                        self.comparar(cur, self.palabra_aleatoria_label.cget("text"))
                    else:
                        print("Invalid hand_sign_id:", hand_sign_id)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = cv2.flip(frame, 1)
            captured_image = Image.fromarray(frame)
            my_image = ctk.CTkImage(dark_image=captured_image, size=(340, 335))
            self.video_lable.configure(image=my_image)
            self.video_lable.after(10, self.open_camera1)
    
    def change_text(self):
        #self.palabra_aleatoria_label.configure(text=requests.get("https://random-word-api.herokuapp.com/word?number=1").json()[0])
        self.palabra_aleatoria_label.configure(text="C")

    def comparar(self, cur, letra):
        if cur == letra:
            self.resultado_label.configure(text="CORRECTO")
        elif cur:
            self.resultado_label.configure(text="INCORRECTO")
            self.count += 1
            self.dibujar_ahorcado(self.canvas_ahorcado, self.count)

    def dibujar_ahorcado(self, canvas, intentos):
        # Dibujar la cabeza
        if intentos == 1:
            canvas.create_oval(50, 50, 100, 100, outline='black', width=4)

        # Dibujar el cuerpo
        if intentos == 2:
            canvas.create_line(100, 100, 100, 150, fill='black', width=4)

        if intentos == 3:
            # Dibujar el brazo izquierdo
            canvas.create_line(100, 110, 80, 130, fill='black', width=4)

        if intentos == 4:
            # Dibujar el brazo derecho
            canvas.create_line(100, 110, 120, 130, fill='black', width=2)

        if intentos == 5:
            # Dibujar la pierna izquierda
            canvas.create_line(100, 150, 80, 170, fill='black', width=2)

        if intentos == 6:
            # Dibujar la pierna derecha
            canvas.create_line(100, 150, 120, 170, fill='black', width=2)

    # Llama a esta función para dibujar la figura del ahorcado

#Probando zzz
prueba = Camera()
prueba.ejecutar()
