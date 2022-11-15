import os

import pywintypes
import win32con
from PIL import ImageGrab, Image
import numpy as np
import curses
from curses import wrapper
import keyboard
import ctypes
import win32gui
from ctypes import windll
import win32ui

class Apple:
    def __init__(self, stdscr):
        self.converted_img = None
        self.img = None
        self.stdscr = stdscr
        self.size = 7
        self.grad = np.array(list("       ..''``^,,<~+=:;!i|Il(1?[{tfjrxnuvczeomwqpdbkhXYUQ#MW&8B№@"))
        #self.grad = np.array(list(" .:;xX$@"))

    def get_image(self):
        try:
            hwnd = win32gui.FindWindow(None, 'Друзья - Discord')
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            try:  # Windows 8.1 and later
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except:
                try:  # Before Windows 8.1
                    ctypes.windll.user32.SetProcessDPIAware()
                except:  # Windows 8 or before
                    pass # fuck you

            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

            saveDC.SelectObject(saveBitMap)

            windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2) #2

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            self.img = np.array(im)
            self.out()
        except pywintypes.error:
            self.img = np.array(ImageGrab.grab(bbox=None))
            self.out()

    def out(self):
        if keyboard.is_pressed("esc"):
            os.system('cls')
            exit()
        b = np.sum(self.img[::self.size, ::self.size], axis=2)
        try:
            self.stdscr.clear()
            for i in b:
                self.stdscr.addstr("".join(self.grad[i // (768 // self.grad.size)]) + "\n", curses.A_BOLD)
            self.stdscr.refresh()
        except curses.error:
            self.size += 1
            print("Решаю ошибку. Ожидайте... (рекомендованно открывать код через полноэкранную консоль, а не терминал)")


def set_console_size():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)


if __name__ == '__main__':
    set_console_size()
    a = wrapper(Apple)
    while True:
        a.get_image()
