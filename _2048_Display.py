from PIL import Image, ImageTk, ImageDraw, ImageFont
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
        self.canvas_proportion = 1000,1400
        self.board_size = 695
        self.setup_window()
    def load_images(self):
        self.game_bg = Image.open('resources/game-bg.png')
        #
        self.tile_images = {}
        self.tile_scale = .8
        self.tile_size = int(19 / 20 * (self.game_bg.size[0] * self.tile_scale / 4))
        _size = (self.tile_size,self.tile_size)
        self.tile_images[0] = Image.open('resources/0.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[2] = Image.open('resources/2.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[4] = Image.open('resources/4.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[8] = Image.open('resources/8.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[16] = Image.open('resources/16.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[32] = Image.open('resources/32.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[64] = Image.open('resources/64.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[128] = Image.open('resources/128.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[256] = Image.open('resources/256.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[512] = Image.open('resources/512.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[1024] = Image.open('resources/1024.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[2048] = Image.open('resources/2048.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[4096] = Image.open('resources/4096.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[8192] = Image.open('resources/8192.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[16384] = Image.open('resources/16384.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[32768] = Image.open('resources/32768.png').resize(_size, Image.ANTIALIAS)
        self.tile_images[65536] = Image.open('resources/65536.png').resize(_size, Image.ANTIALIAS)
    def setup_window(self):
        # # initial setup
        self.primary_window = Tk()
        self.primary_window.wm_title("2048~")
        # self.primary_window.geometry('695x970+1189+10')
        self.primary_window.geometry('695x970+2264+30')
        self.window_size = 695,970
        self.load_images()
        # self.primary_window.geometry('1274x960+3281+1112')
        # self.primary_window.minsize(width=100, height=30)
        # self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # # canvas
        # self.canvas_frame = ttk.Frame(self.primary_window)
        # self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canv_size = self.get_size( self.window_size, self.canvas_proportion )
        self.the_canvas = Canvas(self.primary_window,
                                width=self.canv_size[0],
                                height=self.canv_size[1],
                                background='#FFFFFF')
        self.the_canvas.grid(row=0,column=0)
        self.game_photo = ImageTk.PhotoImage(self.game_bg.resize(self.canv_size, Image.ANTIALIAS))
        self.image_item = self.the_canvas.create_image(0, 0, image=self.game_photo, anchor='nw')
        # self.the_canvas.pack()
        
        # self.primary_window.bind("<Left>",lambda event: self.parent.game.move("left"))
        # self.primary_window.bind("<Up>",lambda event: self.parent.game.move("up"))
        # self.primary_window.bind("<Down>",lambda event: self.parent.game.move("down"))
        # self.primary_window.bind("<Right>",lambda event: self.parent.game.move("right"))
        # self.primary_window.bind(";",lambda event: self.parent.game.undo())
        # self.primary_window.bind("z",lambda event: self.parent.game.new_game())
        
        self.primary_window.bind("<Left>",lambda event: self.parent.move("left"))
        self.primary_window.bind("<Up>",lambda event: self.parent.move("up"))
        self.primary_window.bind("<Down>",lambda event: self.parent.move("down"))
        self.primary_window.bind("<Right>",lambda event: self.parent.move("right"))
        self.primary_window.bind(";",lambda event: self.parent.move("undo"))
        self.primary_window.bind("z",lambda event: self.parent.move("new_game"))
        
        self.update_display(self.parent.game.board,self.parent.game.score)
    def update_display(self,board,score):
        assert(isinstance(board,np.ndarray))
        assert(board.shape == (4,4))
        start_x = int(self.game_bg.size[0] / 20)
        start_y = int(self.game_bg.size[1] * 4 / 14 + start_x)
        start_point = start_x, start_y
        padding_between_tiles = 19 / 20 * self.game_bg.size[0] * (1 - self.tile_scale) / 5
        curr_image = self.game_bg.copy()
        
        # paste the tile images
        for row in range(4):
            for col in range(4):
                x_loc = start_x + int(col * (padding_between_tiles + self.tile_size) + .4*padding_between_tiles)
                y_loc = start_y + int(row * (padding_between_tiles + self.tile_size) + .4*padding_between_tiles)
                val = board[row,col]
                curr_image.paste(self.tile_images[val],(x_loc,y_loc))
        
        # paste the score
        font = ImageFont.truetype("resources/ClearSans-Bold.ttf", 135)
        draw = ImageDraw.Draw(curr_image)
        draw.text((.7765 * self.game_bg.size[0],.155 * self.game_bg.size[0]),str(score),(255,255,255),font=font,anchor="mm")
        
        # update the canvas image
        self.game_photo = ImageTk.PhotoImage(curr_image.resize(self.canv_size, Image.ANTIALIAS))
        self.the_canvas.itemconfig(self.image_item, image = self.game_photo)
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