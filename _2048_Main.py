from _2048_Display import Display
from _2048_Game import Game
from tkinter import mainloop
import os
import win32gui
import win32con
import threading
from queue import Queue
import time
import time
import numpy as np

class Parent:
    def __init__(self):
        # self.main_queue = Queue()
        self.resize_CLI_window()
        self.display  = Display(self)
        board = np.array([[0,4,0,0],
                          [0,0,0,0],
                          [0,2,0,0],
                          [0,0,0,0]])
        self.game = Game(board)
        # self.pause = False
        # main_queue_thread = threading.Thread(target=lambda: self. main_queue_thread())
        # main_queue_thread.daemon = True
        # main_queue_thread.start()
        mainloop()
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
    # def main_queue_thread(self):
        # while True: # handle objects in the queue until game_lost
            # time.sleep(.25)
            # try:
                # next_action = self.main_queue.get(False)
                # next_action()
            # except Exception as e: 
                # if str(e) != "": print(e)
        # self.main_queue.queue.clear()
        # self.close()
    def close(self):
        for handle in self.cli_handles:
            win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)

if __name__ == '__main__':
    main_object = Parent()
    