from camera_senias import Camera    
import time

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

class Test:

    def __init__(self):
        print("zzz")

    def ejecutar(self):
        cam = Camera()

        cam.ejecutar()

        start = time.time()
        
        run = True

        while (run):
            print(cam.cur)
            end = time.time()
            if ((end - start) > 3):
                print("logrado")
                cam.window.quit()
                run = False
            if (cam.cur != 'C'):
                start = time.time()

t = Test()
t.ejecutar()
