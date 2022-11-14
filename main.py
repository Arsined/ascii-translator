from PIL import ImageGrab
import numpy as np
import curses
from curses import wrapper
import keyboard
import os

class Apple:
    def __init__(self, stdscr):
        self.converted_img = None
        self.img = None
        self.stdscr = stdscr
        self.size = 7
        self.grad = np.array(list("       ..''``^,,<~+=:;!i|Il(1?[{tfjrxnuvczeomwqpdbkhXYUQ#MW&8B№@"))
        #self.grad = np.array(list(" .:;xX$@"))

    def get_image(self):
        self.img = np.array(ImageGrab.grab(bbox=None))
        # self.img = self.img[:, 0:self.img[0].size//6]
        self.out()

    def out(self):
        b = np.sum(self.img[::self.size, ::self.size], axis=2)
        try:
            self.stdscr.clear()
            for i in b:
                self.stdscr.addstr("".join(self.grad[i // (768 // self.grad.size)]) + "\n", curses.A_BOLD)
            self.stdscr.refresh()
        except curses.error:
            self.size += 1
            print("Решау ошибку. Ожидайте... (рекомендованно открывать код через полноэкранную консоль, а не терминал)")


if __name__ == '__main__':
    keyboard.press('f11')
    a = wrapper(Apple)
    while True:
        a.get_image()
