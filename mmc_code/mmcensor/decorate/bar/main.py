import importlib
import tkinter as tk
import cv2
import math
from mmcensor.decorate.decorator_utils import feature_selector
import mmcensor.geo as geo

class decorator:

    def initialize( self, known_classes ):
        self.known_classes = known_classes
        self.classes = []
        self.color = (0,0,0)
        self.expand = 0
        return

    def decorate( self, img, boxes ):
        boxes = geo.expand_boxes( boxes, self.expand)
        for box in boxes:
            if self.known_classes[box[1]] in self.classes:
                img = cv2.rectangle( img, (box[2],box[3]),(box[4],box[5]), tuple(reversed(self.color)), cv2.FILLED )
        return img

    def export_settings( self ):
        return( { 'classes': self.classes, 'color': self.color, 'expand': self.expand } )

    def import_settings( self, settings ):
        self.classes = settings['classes']
        self.color = settings['color']
        self.expand = settings['expand']

    def short_name( self ):
        return 'bar'

    def short_desc( self ):
        return '%d classes, color (%d,%d,%d)'%(len(self.classes),self.color[0], self.color[1], self.color[2] )

    def populate_config_frame( self, frame ):
        #self.feature_selector = importlib.import_module('decorator_utils').feature_selector()
        self.r = tk.IntVar()
        self.g = tk.IntVar()
        self.b = tk.IntVar()
        self.expand_var = tk.IntVar()

        tk.Label( frame, text="Color (0-255)" ).grid(row=0,column=0,columnspan=6)
        tk.Label( frame, text="R").grid(row=1,column=0)
        self.r_entry = tk.Entry( frame, textvariable=self.r, width=4 )
        self.r_entry.delete(0,tk.END)
        self.r_entry.insert(0,str(self.color[0]))
        self.r_entry.grid(row=1,column=1)
        tk.Label( frame, text="G").grid(row=1,column=2)
        self.g_entry = tk.Entry( frame, textvariable=self.g, width=4 )
        self.g_entry.delete(0,tk.END)
        self.g_entry.insert(0,str(self.color[1]))
        self.g_entry.grid(row=1,column=3)
        tk.Label( frame, text="B").grid(row=1,column=4)
        self.b_entry = tk.Entry( frame, textvariable=self.b, width=4 )
        self.b_entry.delete(0,tk.END)
        self.b_entry.insert(0,str(self.color[2]))
        self.b_entry.grid(row=1,column=5)
        tk.Label( frame, text="Expand").grid(row=2,column=0)
        self.h_entry = tk.Entry( frame, textvariable=self.expand_var, width=4 )
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
        self.expand = self.expand_var.get()

    def destroy_config_frame( self ):
        return 0

