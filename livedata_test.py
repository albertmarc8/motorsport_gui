import tkinter as tk
from random import random, randint

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from utils.IO import *

hist_data = []
y_data = []
cond = False
counter = 0
counter_tot = 0


def plot_data():
    print("plot data")
    global cond, counter, counter_tot, y_data, hist_data

    if cond:
        line = arduino.read_from_arduino()
        counter += randint(0, 10)
        counter_tot += 1
        if counter % 50 == 0:
            counter = 0

        if len(shown_data) < 100:
            shown_data = np.append(shown_data, counter)
        else:
            shown_data[0:99] = shown_data[1:100]
            shown_data[99] = counter
        hist_data.append(line)

        lines.set_xdata(np.arange(0, len(shown_data)))
        lines.set_ydata(shown_data)
        ax.set_ylim(0, max(shown_data)*1.1)
        canvas.draw()
    if cond:
        root.after(10, plot_data)



def plot_start():
    global cond
    print("Started")
    cond = True
    plot_data()


def plot_end():
    global cond
    print("Stopped")
    cond = False


# GUI
root = tk.Tk()
root.title = ("Real time data")
root.configure(background='light blue')
root.geometry('1600x900')

fig = Figure()
ax = fig.add_subplot(111)
ax.set_title("RealTime")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_xlim(0, 100)
ax.set_ylim(0, 1000)
lines = ax.plot([], [])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=10, y=10, width=1500, height=500)
canvas.draw()

root.update()
start = tk.Button(root, text="Start", command=lambda: plot_start())
start.place(x=100, y=600)

root.update()
stop = tk.Button(root, text="Stop", command=lambda: plot_end())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=600)

# connecting to serial
arduino = ArduinoReceiver()
arduino.find_port()
arduino.connect_to_arduino()

root.after(1, plot_data)
root.mainloop()
