import importlib
import tkinter as tk
import cv2
import math
from mmcensor.decorate.decorator_utils import feature_selector

class decorator:

    def initialize( self, known_classes ):
        self.known_classes = known_classes
        self.classes = []
        self.color = (0,0,0)
        self.expand = 0
        return

    def decorate( self, img, boxes ):
        for box in boxes:
            if self.known_classes[box[1]] in self.classes:
                w = box[4] - box[2]
                h = box[5] - box[3]
                w_diff = math.floor(self.expand*w/100)
                h_diff = math.floor(self.expand*h/100)
                img = cv2.rectangle( img, (box[2]-w_diff,box[3]-h_diff),(box[4]+w_diff,box[5]+h_diff), tuple(reversed(self.color)), cv2.FILLED )
        return img

    def export_settings( self ):
        return( { 'classes': self.classes, 'color': self.color, 'harshness': self.expand } )

    def import_settings( self, settings ):
        self.classes = settings['classes']
        self.color = settings['color']
        self.expand = settings['harshness']

    def short_name( self ):
        return 'harsh-bar'

    def short_desc( self ):
        return '%d classes, color (%d,%d,%d)'%(len(self.classes),self.color[0], self.color[1], self.color[2] )

    def populate_config_frame( self, frame ):
        #self.feature_selector = importlib.import_module('decorator_utils').feature_selector()
        self.r = tk.IntVar()
        self.g = tk.IntVar()
        self.b = tk.IntVar()
        self.h = tk.IntVar()

        tk.Label( frame, text="Color (0-255)" ).grid(row=0,column=0,columnspan=6)
        tk.Label( frame, text="R").grid(row=1,column=0)
        self.r_entry = tk.Entry( frame, textvariable=self.r )
        self.r_entry.delete(0,tk.END)
        self.r_entry.insert(0,str(self.color[0]))
        self.r_entry.grid(row=1,column=1)
        tk.Label( frame, text="G").grid(row=1,column=2)
        self.g_entry = tk.Entry( frame, textvariable=self.g )
        self.g_entry.delete(0,tk.END)
        self.g_entry.insert(0,str(self.color[1]))
        self.g_entry.grid(row=1,column=3)
        tk.Label( frame, text="B").grid(row=1,column=4)
        self.b_entry = tk.Entry( frame, textvariable=self.b )
        self.b_entry.delete(0,tk.END)
        self.b_entry.insert(0,str(self.color[2]))
        self.b_entry.grid(row=1,column=5)
        tk.Label( frame, text="harshness").grid(row=2,column=0)
        self.h_entry = tk.Entry( frame, textvariable=self.h )
        self.h_entry.delete(0,tk.END)
        self.h_entry.insert(0,str(self.expand))
        self.h_entry.grid(row=2,column=1)

        self.feature_selector = feature_selector()

        class_frame = tk.Frame(frame)
        self.feature_selector.populate_frame(class_frame, self.known_classes, self.classes)
        class_frame.grid(row=3,column=0,columnspan=6)

    def apply_config_from_config_frame( self ):
        self.classes = self.feature_selector.get_selected_classes()
        self.color = (self.r.get(), self.g.get(), self.b.get() )
        self.expand = self.h.get()

    def destroy_config_frame( self ):
        return 0

