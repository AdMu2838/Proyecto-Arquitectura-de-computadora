import customtkinter as ctk
import csv
import cv2
from model import KeyPointClassifier
import requests
from juego import Juego

class Interface:

    def ejecutar(self):
        mi_juego = Juego()
        # Load the KeyPointClassifier model
        mi_juego.keypoint_classifier = KeyPointClassifier()

        # Read labels from a CSV file
        with open('model/keypoint_classifier/label.csv', encoding='utf-8-sig') as f:
            keypoint_classifier_labels_reader = csv.reader(f)
            mi_juego.keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels_reader]
        # Set the appearance mode and color theme for the custom tkinter library
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Create the main window
        initial_width, initial_height = 1400, 700
        window = ctk.CTk()
        window.geometry(f'{initial_width}x{initial_height}')
        window.title("HAND SIGNS")
        
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
        video_frame = ctk.CTkFrame(master=MyFrame1,height=340,width=365,corner_radius=12)
        video_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand = ctk.TRUE ,padx=(10,10),pady=(10,5))

        # Create the video label
        mi_juego.video_lable = ctk.CTkLabel(master=video_frame, text='', height=340, width=365, corner_radius=12)
        mi_juego.video_lable.pack(fill=ctk.BOTH, padx=(0, 0), pady=(0, 0))


        # Create a button to start the camera feed
        Camera_feed_start = ctk.CTkButton(master=MyFrame1, text='START', height=40, width=250, border_width=0, corner_radius=12, command=lambda: mi_juego.open_camera1())
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
        mi_juego.letter = ctk.CTkLabel(MyFrame2,
                                font=myfont,fg_color='#2B2B2B',justify=ctk.CENTER)
        mi_juego.letter.pack(fill = ctk.BOTH,side=ctk.LEFT,expand = ctk.TRUE,padx = (10,10),pady=(10,10))
        mi_juego.letter.configure(text='')

        MyFrame3=ctk.CTkFrame(master=window,
                            height=175,
                            corner_radius=12
                            )
        MyFrame3.pack(fill = ctk.X,expand = ctk.TRUE,padx = (10,10),pady=(10,10))

        # Create a textbox for displaying a sentence
        # Sentence = ctk.CTkTextbox(MyFrame3,
        #                         font=("Consolas",24))
        # Sentence.pack(fill = ctk.X,side=ctk.LEFT,expand = ctk.TRUE,padx = (10,10),pady=(10,10))

        cambio_palabra = ctk.CTkButton(master=MyFrame3, text="cambiar", height=40, width=250, border_width=0, corner_radius=12, command=lambda: mi_juego.change_text())
        cambio_palabra.pack(side=ctk.TOP, pady=(5, 10))

        mi_juego.palabra_aleatoria_label = ctk.CTkLabel(MyFrame3, font=("Consolas", 24))
        mi_juego.palabra_aleatoria_label.pack(fill=ctk.X, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        mi_juego.change_text()
        
        mi_juego.resultado_label = ctk.CTkLabel(MyFrame3, font=("Consolas", 24))
        mi_juego.resultado_label.pack(fill=ctk.X, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        mi_juego.resultado_label.configure(text= "RESULTADO")

        MyFrame4 = ctk.CTkFrame(master=main_frame, height=375)
        MyFrame4.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10)) 

        mi_juego.canvas_ahorcado = ctk.CTkCanvas(MyFrame4, height=200, width=200, bg="dark green")
        mi_juego.canvas_ahorcado.pack(fill=ctk.BOTH, side=ctk.LEFT, expand=ctk.TRUE, padx=(10, 10), pady=(10, 10))
        # Start the tkinter main loop
        window.mainloop()

mi_interfaz = Interface()
mi_interfaz.ejecutar()