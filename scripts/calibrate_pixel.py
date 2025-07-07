import matplotlib.pyplot as plt
import random
from numpy import sqrt as sqrt
import os
import cv2

from tkinter import *
from tkinter import messagebox, filedialog

class AskInput:
    def __init__(self, title, prompt, typeinput):

        self.root = Tk()
        self.root.title(title)
        self.type_input = typeinput

        self.prompt = Label(self.root, text=prompt)
        self.prompt.grid(row=0, column=0)

        self.entry = Entry(self.root)
        self.entry.grid(row=1, column=0)

        self.button = Button(self.root, text='Enter', command=self.get_entry)
        self.button.grid(row=1, column=1)

        self.root.mainloop()

    def get_entry(self):
        try:
            value = self.convert(self.entry.get(), self.type_input)
            self.root.quit()
            return value
        except:
            messagebox.showwarning('Error', f'Entry is not a {self.type_input}')

    @staticmethod
    def convert(variable, type_asked):
        return type_asked(variable)



class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self.draw)
        self.keypress = line.figure.canvas.mpl_connect('key_press_event', self.key)

    def draw(self, event):
        if len(self.xs) < 2:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)

            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()
    def key(self, event):
        if event.key == 'q':
            plt.close('all')

        if event.key == 'a':
            self.line.set_data([], [])
            self.ys, self.xs = [], []
            self.line.figure.canvas.draw()



def ploter(filepath):
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    fig.canvas.manager.set_window_title('Calibration Step')

    video = cv2.VideoCapture(filepath)
    randomnb = random.randint(0, int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    video.set(1, randomnb)
    fig.suptitle('Calibration', fontsize=16)

    ret, frame = video.read()
    imgplot = plt.imshow(frame)

    line, = ax.plot([], [])
    linebuilder = LineBuilder(line)

    plt.show()
    return(linebuilder.line.get_data())


def Calibrator (video_path):

    coord = ploter(video_path)

    distance_px = sqrt((coord[0][0] - coord[1][0]) ** 2 + (coord[0][1] - coord[1][1]) ** 2)

    distance_cm = float(input('Distance in cm : '))

    pixel_size = distance_cm / distance_px

    return pixel_size


if __name__ == '__main__':
    path = str(input('Enter the file path : '))
    size = Calibrator(path)

    print("pixel size: ", size)