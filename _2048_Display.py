from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import Canvas,Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,IntVar,Checkbutton,Radiobutton
import os
import numpy as np
from tkinter import filedialog
import math
import random
import time

class Display:
    def __init__(self, parent):
        self.parent = parent
        self.main_font = ("resources/ClearSans-Regular.ttf", 22, "bold")
        self.board_size = 695
        self.setup_window()
    def load_images(self):
        self.tile_size = self.win_size * .7 / 4
        _size = (self.tile_size,self.tile_size)
        pil_img = Image.open('resources/2.gif').resize(_size, Image.ANTIALIAS)
        self._2_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/4.gif').resize(_size, Image.ANTIALIAS)
        self._4_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/8.gif').resize(_size, Image.ANTIALIAS)
        self._8_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/16.gif').resize(_size, Image.ANTIALIAS)
        self._16_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/32.gif').resize(_size, Image.ANTIALIAS)
        self._32_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/64.gif').resize(_size, Image.ANTIALIAS)
        self._64_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/128.gif').resize(_size, Image.ANTIALIAS)
        self._128_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/256.gif').resize(_size, Image.ANTIALIAS)
        self._256_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/512.gif').resize(_size, Image.ANTIALIAS)
        self._512_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/1024.gif').resize(_size, Image.ANTIALIAS)
        self._1024_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/2048.gif').resize(_size, Image.ANTIALIAS)
        self._2048_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/4096.gif').resize(_size, Image.ANTIALIAS)
        self._4096_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/8192.gif').resize(_size, Image.ANTIALIAS)
        self._8192_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/16384.gif').resize(_size, Image.ANTIALIAS)
        self._16384_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/32768.gif').resize(_size, Image.ANTIALIAS)
        self._32768_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('resources/65536.gif').resize(_size, Image.ANTIALIAS)
        self._65536_photo=ImageTk.PhotoImage(pil_img)
        #
        
    def setup_window(self):
        # # initial setup
        self.primary_window = Tk()
        # self.load_images()
        self.primary_window.wm_title("2048~")
        self.primary_window.geometry('695x970+1189+10')
        # self.primary_window.geometry('1274x960+3281+1112')
        # self.primary_window.minsize(width=100, height=30)
        # self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # # canvas
        self.canvas_frame = ttk.Frame(self.primary_window)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        # self.the_canvas = Canvas(self.canvas_frame,
                                # width=self.win_size[0],
                                # height=self.win_size[1],
                                # background='#111111')
        
        self.primary_window.bind("<Left>",lambda event: self.parent.game.move("left"))
        self.primary_window.bind("<Up>",lambda event: self.parent.game.move("up"))
        self.primary_window.bind("<Down>",lambda event: self.parent.game.move("down"))
        self.primary_window.bind("<Right>",lambda event: self.parent.game.move("right"))
        self.primary_window.bind(";",lambda event: self.parent.game.undo())
        self.primary_window.bind("z",lambda event: self.parent.game.new_game())
    def get_size(self, max_size, input_size, circumscribe = False):
        # fits dimensions to a target size while maintaining aspect ratio
        if (input_size[0] != max_size[0]) or (input_size[1] != max_size[1]):
            if not circumscribe:
                if (input_size[0] > max_size[0]) or (input_size[1] > max_size[1]):
                    if input_size[0]/input_size[1] > max_size[0]/max_size[1]:
                        resized_size=(int(max_size[0]),int(max_size[0]*input_size[1]/input_size[0]))
                    else:
                        resized_size=(int(max_size[1]*input_size[0]/input_size[1]),int(max_size[1]))
                else:
                    if input_size[0]/input_size[1] < max_size[0]/max_size[1]:
                        resized_size=(int(max_size[1]*input_size[0]/input_size[1]),int(max_size[1]))
                    else:
                        resized_size=(int(max_size[0]),int(max_size[0]*input_size[1]/input_size[0]))
            else:
                if (input_size[0] > max_size[0]) or (input_size[1] > max_size[1]):
                    if not (input_size[0]/input_size[1] > max_size[0]/max_size[1]):
                        resized_size=(int(max_size[0]),int(max_size[0]*input_size[1]/input_size[0]))
                    else:
                        resized_size=(int(max_size[1]*input_size[0]/input_size[1]),int(max_size[1]))
                else:
                    if not (input_size[0]/input_size[1] < max_size[0]/max_size[1]):
                        resized_size=(int(max_size[1]*input_size[0]/input_size[1]),int(max_size[1]))
                    else:
                        resized_size=(int(max_size[0]),int(max_size[0]*input_size[1]/input_size[0]))
        else: resized_size = input_size
        return resized_size