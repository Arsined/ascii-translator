import os
import curses
import ctypes
import time

import numpy as np
import pyautogui
from PIL import Image
import keyboard
import win32con
import win32gui
import win32ui

class Apple:
    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.size = 7
        self.time = time.time()
        self.grad = np.array(list("       ..''``^,,<~+=:;!i|Il(1?[{tfjrxnuvczeomwqpdbkhXYUQ#MW&8B№@"))

    def get_image(self) -> None:
        self.time = time.time()
        win_name = "opera"
        for title in pyautogui.getAllTitles():
            if win_name.lower() in title.lower():
                hwnd = win32gui.FindWindow(None, title)
                break
        else:
            for title in pyautogui.getAllTitles():
                if len(title)>1:
                    hwnd = win32gui.FindWindow(None, title)
                    break
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

        ctypes.windll.shcore.SetProcessDpiAwareness(2)

        user32 = ctypes.windll.user32
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

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
        img = np.array(im)
        self.out(img)

    def out(self, img: np.array) -> None:
        if keyboard.is_pressed("esc"):
            os.system('cls')
            exit()
        kk = (256 // self.grad.size)
        k = np.array([0.2126 / kk, 0.7152 / kk, 0.0722 / kk])
        img = np.multiply(img, k)
        converted_img = np.sum(img[::self.size, ::self.size], axis=2).astype(int)
        try:
            self.stdscr.clear()
            for row in converted_img:
                self.stdscr.addstr("".join(self.grad[row]) + "\n", curses.A_BOLD)
            self.stdscr.addstr(str(1/(time.time() - self.time)))
            self.stdscr.refresh()
        except curses.error:
            self.size += 1
            print("Решаю ошибку. Ожидайте... (рекомендованно открывать код через полноэкранную консоль, а не терминал)")


def set_console_size() -> None:
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, win32con.SW_MAXIMIZE)
def main():
    set_console_size()
    a = curses.wrapper(Apple)
    while True:
        a.get_image()

if __name__ == '__main__':
    main()
