import importlib
import tkinter as tk
import cv2
from mmcensor.decorate.decorator_utils import feature_selector
import mmcensor.geo as geo
import math
import numpy as np

class decorator:


    def initialize( self, known_classes ):
        self.known_classes = known_classes
        self.classes = []
        self.strength=10
        self.color = (1, 1, 1)
        self.circular = False
        self.expand = 0

    def decorate( self, img, boxes ):
        boxes = geo.expand_boxes( boxes, self.expand)
        condensed = geo.condense_boxes_single( boxes )

        for feature in condensed:
            if self.known_classes[feature] in self.classes:
                for box in condensed[feature]:
                    w = box[4]-box[2]
                    h = box[5]-box[3]
                    wr = w>>1
                    hr = h>>1
                    factor = 2 * math.ceil( self.strength * min( w,h ) / 100 /2 ) + 1
                    region = img[box[3]:box[5],box[2]:box[4]]
                    blur = cv2.blur( region, (factor,factor), cv2.BORDER_DEFAULT )
                    if self.circular:
                        mask = np.zeros(region.shape, np.uint8)
                        mask = cv2.ellipse(mask, (wr, hr), (wr, hr), 
                            0, 0, 360, self.color, -1)
                        img[box[3]:box[5],box[2]:box[4]] = region + blur*mask - region*mask
                    else:
                        img[box[3]:box[5],box[2]:box[4]] = blur

        return img

    def export_settings( self ):
        return( { 'classes': self.classes, 'strength': self.strength, 'circular': self.circular, 'expand': self.expand } )

    def import_settings( self, settings ):
        self.classes = settings['classes']
        self.strength = settings['strength']
        self.circular = settings['circular']
        self.expand = settings['expand']
        

    def short_desc( self ):
        return '%d classes, strength %d'%(len(self.classes),self.strength)

    def populate_config_frame( self, frame ):
        #self.feature_selector = importlib.import_module('decorator_utils').feature_selector()
        self.strength_var = tk.IntVar()
        self.circular_var = tk.IntVar()
        self.expand_var = tk.IntVar()

        tk.Label( frame, text="Strength (1 to 50 or higher):").grid(row=0,column=0,columnspan=5)
        self.strength_entry = tk.Entry( frame, textvariable=self.strength_var, width=5 )
        self.strength_entry.delete(0,tk.END)
        self.strength_entry.insert(0,str(self.strength))
        self.strength_entry.grid(row=1,column=1)
        tk.Label( frame, text="Expand").grid(row=1,column=2)
        self.h_entry = tk.Entry( frame, textvariable=self.expand_var, width=5 )
        self.h_entry.delete(0,tk.END)
        self.h_entry.insert(0,str(self.expand))
        self.h_entry.grid(row=1,column=3)
        self.circle_entry = tk.Checkbutton( frame, text="Circular",onvalue=True, offvalue=False, variable=self.circular_var)
        if self.circular:
            self.circle_entry.select()
        self.circle_entry.grid(row=1,column=4)

        self.feature_selector = feature_selector()

        class_frame = tk.Frame(frame)
        self.feature_selector.populate_frame(class_frame, self.known_classes, self.classes)
        class_frame.grid(row=2,column=0,columnspan=4)

    def apply_config_from_config_frame( self ):
        self.classes = self.feature_selector.get_selected_classes()
        self.strength = self.strength_var.get()
        self.circular = self.circular_var.get()
        self.expand = self.expand_var.get()

    def destroy_config_frame( self ):
        return 0

