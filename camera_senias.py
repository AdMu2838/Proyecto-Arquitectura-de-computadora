
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

class Camera:
    
    cur = 0
    window = 0

    def __init__(self):
        # Inicialización de variables y configuración inicial
        self.prev = ""
        self.video_lable = None
        self.keypoint_classifier = None
        self.cap = cv2.VideoCapture(0)
        self.keypoint_classifier_labels = []
        self.letter = None

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
        cur = 0
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
        window = ctk.CTk()
        window.geometry('1080x1080')
        window.title("HAND SIGNS")
        

        # Initialize the video capture
        
        
      
        width, height = 600, 500

        # Create the title label
        i = 0
        title = ctk.CTkFont(
            family='Consolas',
            weight='bold',
            size=25
        )
        Label = ctk.CTkLabel(
            window,
            text = 'HAND SIGNS',
            fg_color='steelblue',
            text_color= 'white',
            height= 40,
            font=title,
            corner_radius= 8)
        Label.pack(side = ctk.TOP,fill=ctk.X,pady=(10,4),padx=(10,10))

        # Create the main frame
        main_frame = ctk.CTkFrame(master=window,
                                height=770,
                                corner_radius=8
                                )

        main_frame.pack(fill = ctk.X , padx=(10,10),pady=(5,0))
        MyFrame1=ctk.CTkFrame(master=main_frame,
                            height = 375,
                            width=365
                            )
        MyFrame1.pack(fill = ctk.BOTH,expand=ctk.TRUE,side = ctk.LEFT,padx = (10,10),pady=(10,10))

        # Create the video frame
        video_frame = ctk.CTkFrame(master=MyFrame1,height=50,width=50,corner_radius=12)
        video_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand = ctk.TRUE ,padx=(10,10),pady=(10,5))

        # Create the video label
        self.video_lable = ctk.CTkLabel(master=video_frame, text='', height=340, width=365, corner_radius=12)
        self.video_lable.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))


        # Create a button to start the camera feed
        Camera_feed_start = ctk.CTkButton(master=MyFrame1, text='START', height=40, width=250, border_width=0, corner_radius=12, command=lambda: self.open_camera1())
        Camera_feed_start.pack(side=ctk.TOP, pady=(5, 10))

        MyFrame2=ctk.CTkFrame(master=main_frame,
                            height=375
                            ) 
        MyFrame2.pack(fill = ctk.BOTH,side=ctk.LEFT,expand = ctk.TRUE,padx = (10,10),pady=(10,10))

        # Create a font for displaying letters
        myfont = ctk.CTkFont(
            family='Consolas',
            weight='bold',
            size=200
        )
        self.letter = ctk.CTkLabel(MyFrame2,
                                font=myfont,fg_color='#2B2B2B',justify=ctk.CENTER)
        self.letter.pack(fill = ctk.BOTH,side=ctk.LEFT,expand = ctk.TRUE,padx = (10,10),pady=(10,10))
        self.letter.configure(text='')

        MyFrame3=ctk.CTkFrame(master=window,
                            height=175,
                            corner_radius=12
                            )
        MyFrame3.pack(fill = ctk.X,expand = ctk.TRUE,padx = (10,10),pady=(10,10))

        # Start the tkinter main loop
        window.mainloop()
        
