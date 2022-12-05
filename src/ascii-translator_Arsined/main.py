import os
import curses
import ctypes
import time

import numpy as np
import pyautogui
from PIL import Image
import keyboard
import win32gui
import win32ui
from screeninfo import get_monitors


class Apple:
    def __init__(self, stdscr: curses.window, win: tuple):
        self.stdscr = stdscr
        self.size = 7
        self.time = time.time()
        self.grad = np.array(list("       ..''``,,^<~+=:;!i|Il(1?[{tfjrxnuvczeomwqpdbkhXYUQ#MW&8B№@"))
        self.hwnd, self.saveBitMap, self.saveDC = win

    def get_image(self) -> None:
        self.time = time.time()
        ctypes.windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 0x00000002)
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        img = np.asarray(im)[::self.size, ::self.size]
        self.convert_image(img)

    def convert_image(self, img: np.array) -> None:
        if keyboard.is_pressed("esc"):
            os.system('cls')
            exit()
        kk = (256 // self.grad.size)
        k = np.array([0.2126 / kk, 0.7152 / kk, 0.0722 / kk])
        img = np.multiply(img, k)
        converted_img = np.sum(img, axis=2).astype(int)
        self.out(converted_img)

    def out(self, converted_img) -> None:
        try:
            self.stdscr.clear()
            for row in converted_img:
                self.stdscr.addstr("".join(self.grad[row]) + "\n", curses.A_BOLD)
            self.stdscr.addstr(str(1/(time.time() - self.time)))
            self.stdscr.refresh()
        except curses.error:
            self.size += 1


def set_console_size() -> None:
    user32 = ctypes.windll.user32
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    user32.ShowWindow(hwnd, 3)
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    user32.ShowWindow(hwnd, 1)
    user32.SetWindowPos(hwnd, 0, x, y, w, h-2, 0)


def window_size(hwnd: int) -> tuple[int, int]:
    dpi = ctypes.windll.user32.GetDpiForSystem()
    dpi = dpi / ctypes.windll.user32.GetDpiForWindow(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    a = []
    monitors = get_monitors()
    for m in monitors:
        a.append([abs(m.width - w + m.height - h)])
    indx = a.index(min(a))
    w = int(monitors[indx].width / dpi)
    h = int(monitors[indx].height / dpi)
    return w, h


def get_window(win_name: str) -> tuple[int, 'PyCBitmap', 'PyCDC']:
    hwnd = 0
    user32 = ctypes.windll.user32
    for title in pyautogui.getAllTitles():
        if win_name.lower() in title.lower():
            hwnd = win32gui.FindWindow(None, title)
            break
    else:
        print("Window not find")
        exit()

    w, h = window_size(hwnd)

    hwndDC = user32.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    return hwnd, saveBitMap, saveDC


def main():
    set_console_size()
    a = curses.wrapper(Apple, get_window("opera"))
    while True:
        a.get_image()


if __name__ == '__main__':
    main()
