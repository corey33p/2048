from _2048_Display import Display
from _2048_Game import Game
from _2048_AI import _2048_AI
from tkinter import mainloop
import os
import win32gui
import win32con
import threading
from queue import Queue
import time
import numpy as np

class Parent:
    def __init__(self):
        self.main_queue = Queue()
        self.resize_CLI_window()
        # self.board = np.array([[2,0,2,0],
                          # [0,0,0,0],
                          # [0,0,0,0],
                          # [0,0,0,0]])
        self.board = np.array([[32,16,4,4],
                               [0,0,0,2],
                               [0,0,0,0],
                               [0,0,0,0]])
        self.game = Game(np.array(self.board))
        self.ai = _2048_AI(self)
        self.display  = Display(self)
        self.pause = False
        self.auto = False
        
        self.queue = Queue()
        self.main_queue_thread = threading.Thread(target=self.queue_func)
        self.main_queue_thread.daemon = True
        self.main_queue_thread.start()
        self.queue.put(self._AI)
        mainloop()
    def _AI(self):
        while True:
            if self.auto: time.sleep(.5)
            move = self.ai.find_move(self.game)
            if self.auto: print("move: " + str(move))
            else: input("move: " + str(move))
            self.queue.put(self.move(move))
    def move(self,what):
        if what == "left":
            self.game.move("left")
        elif what == "up":
            self.game.move("up")
        elif what == "down":
            self.game.move("down")
        elif what == "right":
            self.game.move("right")
        elif what == "undo":
            self.game.undo()
        elif what == "new game":
            self.game = Game(np.array(self.board))
        self.display.update_display(self.game.board,self.game.score)
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                if '~2048' in title and 'Notepad++' not in title:
                    param.append(hwnd)
            wind = []
            win32gui.EnumWindows(check, wind)
            return wind
        self.cli_handles = get_windows()
        for window in self.cli_handles:
            win32gui.MoveWindow(window,26,21,1473,812,True)
    def queue_func(self):
        while True: # handle objects in the queue until game_lost
            time.sleep(.25)
            if not self.queue.empty():
                next_action = self.queue.get(False)
                next_action()
        self.queue.clear()
        self.close()
    def close(self):
        for handle in self.cli_handles:
            win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)

if __name__ == '__main__':
    main_object = Parent()
    