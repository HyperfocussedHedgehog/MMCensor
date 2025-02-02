import importlib
import tkinter as tk
import cv2
import math
import random
import numpy as np
import os
from PIL import ImageFont, ImageDraw, Image 
from mmcensor.decorate.decorator_utils import feature_selector

class decorator:

    def initialize( self, known_classes ):
        self.known_classes = known_classes
        self.classes = []
        self.color = (0,0,0)
        self.last_class = None
        self.available_captions = ["FEMME_BREAST_EXPOSED", "VULVA_EXPOSED"]
        # font
        self.font = ImageFont.truetype("mmcensor/fonts/ShadeBlue-2OozX.ttf", 80)
        self.fonts = ["AvinedBrush.otf", "Blink.ttf", "Bounce.ttf", "ShadeBlue-2OozX.ttf", "ConeriaScript.ttf", "Cools.ttf", "WinterSaturday.otf"]

        # org
        self.org = (0, 0)

        # fontSize
        self.fontSize = 80
        
        # Red color in BGR
        self.color = (200, 0, 255)
        self.color2 = (0, 0, 0)
        self.randomize = True
        self.rcolor = (0, 0, 0)

        # Line thickness of 2 px
        self.thickness = 2

        self.text = "Not for BETA boys like you!"

        dirname = os.path.dirname(__file__)
        self.captionsP = open("mmcensor/decorate/caption/Captions/CaptionP.txt", "r").read().splitlines()
        self.captionsB = open("mmcensor/decorate/caption/Captions/CaptionB.txt", "r").read().splitlines()
        self.captionsGeneral = open("mmcensor/decorate/caption/Captions/CaptionGeneral.txt", "r").read().splitlines()
        return

    def decorate( self, img, boxes ):
        #Check if the same features are shown and if so, show the same cation. Else randomize
        same = False
        if len(boxes) == 0:
            self.last_class = -1
            return img
        for box in boxes:
            if box[1] == self.last_class:
                same = True
                break
        if not same:
            found = False
            for box in boxes:
                if self.known_classes[box[1]] in self.available_captions:
                    self.last_class = box[1]
                    self.randomizeCaption()
                    found = True
                    break
            if not found:
                self.last_class = -1
                return img
        
        img = self.draw(img)
        return img
    
    def randomizeCaption( self ):
        if self.last_class == 3:
            self.text = random.choice(self.captionsB)
        if self.last_class == 4:
            self.text = random.choice(self.captionsP)
        if random.randrange(2) == 1:
            self.text = random.choice(self.captionsGeneral) 
        self.font = ImageFont.truetype("mmcensor/fonts/" + random.choice(self.fonts), self.fontSize)
        if self.randomize:
            self.rcolor = (random.randrange(256), random.randrange(256), random.randrange(256))


    def draw( self, img ):
        #Use the PIL library to draw in any font of your choice
        pil_im = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  
        draw = ImageDraw.Draw(pil_im)
        if self.randomize:
            r, g, b = self.rcolor
        else:
            r, g, b = self.color
        _, _, w, h = draw.textbbox((0, 0), self.text, font=self.font)
        H, W, _ = img.shape
        draw.text(((W-w)/2, (H/10)), self.text, font=self.font, fill=(r, g, b, 255), stroke_width=3, stroke_fill=self.color2,) 
        img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        return img

    def export_settings( self ):
        return( { 'classes': self.classes, 'color': self.color , 'random': self.randomize} )

    def import_settings( self, settings ):
        self.classes = settings['classes']
        self.color = settings['color']
        self.randomize = settings['random']

    def short_name( self ):
        return 'caption'

    def short_desc( self ):
        return '%d classes, color (%d,%d,%d)'%(len(self.classes),self.color[0], self.color[1], self.color[2] )

    def populate_config_frame( self, frame ):
        #self.feature_selector = importlib.import_module('decorator_utils').feature_selector()
        self.r = tk.IntVar()
        self.g = tk.IntVar()
        self.b = tk.IntVar()
        self.rd = tk.IntVar()

        tk.Label( frame, text="Text Color (0-255)" ).grid(row=0,column=0,columnspan=7)
        tk.Label( frame, text="R").grid(row=1,column=0)
        self.r_entry = tk.Entry( frame, textvariable=self.r, width=4)
        self.r_entry.delete(0,tk.END)
        self.r_entry.insert(0,str(self.color[0]))
        self.r_entry.grid(row=1,column=1)
        tk.Label( frame, text="G").grid(row=1,column=2)
        self.g_entry = tk.Entry( frame, textvariable=self.g, width=4)
        self.g_entry.delete(0,tk.END)
        self.g_entry.insert(0,str(self.color[1]))
        self.g_entry.grid(row=1,column=3)
        tk.Label( frame, text="B").grid(row=1,column=4)
        self.b_entry = tk.Entry( frame, textvariable=self.b, width=4)
        self.b_entry.delete(0,tk.END)
        self.b_entry.insert(0,str(self.color[2]))
        self.b_entry.grid(row=1,column=5)
        self.random_entry = tk.Checkbutton( frame, text="Randomize",onvalue=True, offvalue=False, variable=self.rd)
        if self.randomize:
            self.random_entry.select()
        self.random_entry.grid(row=1,column=6)

        self.feature_selector = feature_selector()

        class_frame = tk.Frame(frame)
        self.feature_selector.populate_frame(class_frame, self.known_classes, self.classes)
        class_frame.grid(row=2,column=0,columnspan=6)

    def apply_config_from_config_frame( self ):
        self.classes = self.feature_selector.get_selected_classes()
        self.color = (self.r.get(), self.g.get(), self.b.get() )
        self.randomize = self.rd.get()

    def destroy_config_frame( self ):
        return 0

