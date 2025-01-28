import importlib
import tkinter as tk
import cv2
from mmcensor.decorate.decorator_utils import feature_selector
import mmcensor.geo as geo
import math

class decorator:

    def initialize( self, known_classes ):
        self.known_classes = known_classes
        self.classes = []
        self.strength=10
        self.expand = 0

    def decorate( self, img, boxes ):
        condensed = geo.condense_boxes_single( boxes )

        for feature in condensed:
            if self.known_classes[feature] in self.classes:
                for box_or in condensed[feature]:
                    box = box_or.copy()
                    w = box[4]-box[2]
                    h = box[5]-box[3]
                    factor = self.strength * min( w,h ) / 100
                    w_diff = math.floor(self.expand*w/100)
                    h_diff = math.floor(self.expand*h/100)
                    frame_h, frame_w, c = img.shape
                    box[2] = max(0, box[2] - w_diff)
                    box[3] = max(0, box[3] - h_diff)
                    box[4] = min(frame_w, box[4] + w_diff)
                    box[5] = min(frame_h, box[5] + h_diff)
                    w = box[4]-box[2]
                    h = box[5]-box[3]
                    new_w = math.ceil( w/factor )
                    new_h = math.ceil( h/factor )
                    img[box[3]:box[5],box[2]:box[4]]=cv2.resize( cv2.resize( img[box[3]:box[5],box[2]:box[4]], (new_w,new_h), interpolation=cv2.INTER_AREA ), (w,h), interpolation = cv2.INTER_NEAREST )

        return img

    def export_settings( self ):
        return( { 'classes': self.classes, 'strength': self.strength, 'harshness': self.expand } )

    def import_settings( self, settings ):
        self.classes = settings['classes']
        self.strength = settings['strength']
        self.expand = settings['harshness']

    def short_name( self ):
        return 'pixel'

    def short_desc( self ):
        return '%d classes, strength %d'%(len(self.classes),self.strength)

    def populate_config_frame( self, frame ):
        #self.feature_selector = importlib.import_module('decorator_utils').feature_selector()
        self.strength_var = tk.IntVar()
        self.h = tk.IntVar()

        tk.Label( frame, text="Strength (1 to 50 or higher):").grid(row=1,column=0,columnspan=3)
        self.strength_entry = tk.Entry( frame, textvariable=self.strength_var )
        self.strength_entry.delete(0,tk.END)
        self.strength_entry.insert(0,str(self.strength))
        self.strength_entry.grid(row=1,column=3)
        tk.Label( frame, text="harshness").grid(row=2,column=0)
        self.h_entry = tk.Entry( frame, textvariable=self.h )
        self.h_entry.delete(0,tk.END)
        self.h_entry.insert(0,str(self.expand))
        self.h_entry.grid(row=2,column=1)

        self.feature_selector = feature_selector()

        class_frame = tk.Frame(frame)
        self.feature_selector.populate_frame(class_frame, self.known_classes, self.classes)
        class_frame.grid(row=3,column=0,columnspan=4)

    def apply_config_from_config_frame( self ):
        self.classes = self.feature_selector.get_selected_classes()
        self.strength = self.strength_var.get()
        self.expand = self.h.get()

    def destroy_config_frame( self ):
        return 0

