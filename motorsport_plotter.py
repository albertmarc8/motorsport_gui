from random import randint, random

import customtkinter
import matplotlib.pyplot as plt
from tkinter import Label, Menu, LabelFrame, Scrollbar
from tkinter.ttk import Treeview, Style
from customtkinter import CTkFrame as Frame
from customtkinter import CTk as Tk


import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from utils.IO import *
from utils.field_names_constants import Fields
from view.UFSTreeview import UFSTreeview

y_data = [[] for n in range(len(Fields))]
counter = 0
x_data = []

# TODO cambiar a segundos
# TODO opcion de tener el eje X fijo
# TODO cambiar a custom tkinter
# TODO cambiar tabla por columnas a mostrar en gráfica (on/off)
# TODO leyenda

class MotorsportPlotter:
    # Styling parameters
    pad_cont = 5
    single_plot = True
    live_data_enabled = False

    def __init__(self):
        self.color_theme = 'default'
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # GUI
        self.label_time_status = None
        self.label_time_text = None
        self.label_arduino_text = None
        self.label_arduino_status = None
        self.control_container = None
        self.axs = None
        self.toolbarFrame = None
        self.chart_label_frame = None
        self.table_label_frame = None
        self.root = Tk()
        self.my_menu = None
        self.table = None
        self.table_vsb = None  # VSB = Vertical Scroll Bar
        self.canvas = None
        self.figure = None

        self.lines = []
        self.ax = None
        self.toolbar = None

        # Data
        self.filename = None
        self.previous_subplots = []
        self.data = []  # String/int/floats from the file
        self.selected_x = [0]
        self.selected_ys = [10]
        self.values_x = None
        self.values_y = []

        self.canvas_counter = 0
        self.live_counter = 0
        self.init_common_gui()

    def init_common_gui(self):
        # Window settings
        self.root.title("UJI Motorsport Plotter")
        self.root.geometry('1600x900')

        # Grid system declaration
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        # Window menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.my_menu.add_command(label="Import", command=lambda: import_data(self.data, self.table))
        self.my_menu.add_command(label="Export", command=lambda: export_data(self.data))
        self.my_menu.add_command(label="Enable/Disable realtime", command=self.enable_live_data)
        self.my_menu.add_command(label="Plot realtime", command=self.plot_live_data)
        self.my_menu.add_command(label="Single/Multiple graphs", command=self.change_view)

        # View tables dropdown
        tables_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(menu=tables_menu, label="View tables")
        tables_menu.add_command(label="** View airflow")  # TODO add command=method to parameters
        tables_menu.add_command(label="View air temperature", command=lambda: self.plot_change_xy([0], [6]))
        tables_menu.add_command(label="** View engine block temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View gear", command=lambda: self.plot_change_xy([0], [20]))
        tables_menu.add_command(label="View oil pressure", command=lambda: self.plot_change_xy([0], [21]))
        tables_menu.add_command(label="** View oil temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View throttle position and relative throttle position",
                                command=lambda: self.plot_change_xy([0], [13, 14]))
        tables_menu.add_command(label="View RPM", command=lambda: self.plot_change_xy([0], [10]))
        tables_menu.add_command(label="View water temperature", command=lambda: self.plot_change_xy([0], [5]))
        tables_menu.add_command(label="** View water temperature IN")  # TODO add command=method to parameters
        tables_menu.add_command(label="** View water temperature OUT")  # TODO add command=method to parameters

        self.my_menu.add_command(label="Change color theme", command=lambda: self.change_color_theme())

        self.figure = Figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky="NSEW", pady=(0, 50))
        self.canvas.draw()

        # Plot navigation
        self.toolbarFrame = Frame(master=self.root)
        self.toolbarFrame.grid(column=0, row=0, columnspan=2, sticky="ews")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

        # Table
        self.table = UFSTreeview(self.root)

        # Placeholders
        self.control_container = LabelFrame(self.root, text="controls", pady=5)
        self.control_container.columnconfigure(0, weight=1)
        self.control_container.columnconfigure(1, weight=1)
        self.control_container.rowconfigure(0, weight=1)
        self.control_container.rowconfigure(1, weight=1)
        self.control_container.rowconfigure(2, weight=1)
        self.control_container.rowconfigure(3, weight=1)
        self.control_container.grid(column=1, row=1, sticky="NSEW")

        self.label_arduino_text = Label(self.control_container, text="Arduino Status:")
        self.label_arduino_text.grid(column=0, row=0, sticky="NSEW")
        self.label_arduino_status = Label(self.control_container, text="Not connected", fg='blue')
        self.label_arduino_status.grid(column=1, row=0, sticky="NSEW")
        self.label_time_text = Label(self.control_container, text="Moving seconds:")
        self.label_time_text.grid(column=0, row=1, sticky="NSEW")
        self.label_time_status = Label(self.control_container, text="ON", fg="green")
        self.label_time_status.grid(column=1, row=1, sticky="NSEW")
        self.view_plot()

    def view_multi_plot(self):
        # TODO some error appears uppon using this method
        # TODO fix RAM problems, if possible
        if self.data is None:
            return None

        seconds = [vars[0] for vars in self.data]
        rpms = [vars[10] for vars in self.data]
        water_temperature = [vars[5] for vars in self.data]
        air_temperature = [vars[6] for vars in self.data]
        throttle_position = [vars[13] for vars in self.data]
        variables = [rpms, water_temperature, air_temperature, throttle_position]

        # Represent the table
        # self.table = Treeview(self.root)
        # self.table["columns"] = ("Second", "RPMs")
        #
        # self.table.heading("#0", text="", anchor=W)
        # self.table.heading("Second", text="Second", anchor=W)
        # self.table.heading("RPMs", text="RPMs", anchor=W)
        #
        # [self.table.insert(parent="", index="end", iid=i, text="", values=d) for i, d in enumerate(self.data)]
        #
        # # self.table.place(x=0, y=720, height=380, width=1280)
        # self.table.grid(column=0, row=1, sticky=NSEW, padx=self.pad_cont, pady=self.pad_cont)
        # self.root.update()

        # Represent the plot
        """fig = plt.figure(figsize=(5,4), dpi=100)
        fig.add_subplot(111).plot(seconds, rpms)
        fig.add_subplot(121).plot(seconds, rpms)
        fig.add_subplot(131).plot(seconds, rpms)"""
        self.figure, self.axs = plt.subplots(2, 2, figsize=(5, 4))


        self.table['displaycolumns'] = [0] + [5, 6, 10, 13]
        plot_names = ["RPMs", "Water temperature", "Air temperature", "Throttle position"]

        for i, ax in enumerate(self.axs.flat):
            ax.set_title(plot_names)
            ax.plot(seconds, variables[i])


        """
        figure = plt.figure(figsize=(20,7), dpi=100)
        figure.add_subplot(111).plot(seconds, rpms)
        chart = FigureCanvasTkAgg(figure, self.root)
        #chart.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=3, sticky="we")
        chart.get_tk_widget().place(x=0, y=0)
        """

    def view_single_plot(self):
        """
        Displays a single plot on the main view.

        :return: Method does not return anything.
        """
        self.ax = self.figure.add_subplot(111)
        if self.color_theme == 'dark':
            self.ax.set_title("Realtime Data", color="white")
            self.ax.set_facecolor('#242424')
            self.figure.set_facecolor('#242424')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.set_ylabel(Fields[self.selected_ys[0]], color="white")
            self.ax.set_xlabel(Fields[self.selected_x[0]], color="white")
        else:
            # Set default colors
            self.ax.set_title("Realtime Data", color="black")
            self.ax.set_facecolor('white')
            self.figure.set_facecolor('white')
            self.ax.spines['bottom'].set_color('black')
            self.ax.spines['top'].set_color('black')
            self.ax.spines['right'].set_color('black')
            self.ax.spines['left'].set_color('black')
            self.ax.tick_params(axis='x', colors='black')
            self.ax.tick_params(axis='y', colors='black')
            self.ax.set_ylabel(Fields[self.selected_ys[0]], color="black")
            self.ax.set_xlabel(Fields[self.selected_x[0]], color="black")



        self.lines = [[] for n in range(len(Fields))]
        self.lines[0] = self.ax.plot([], [])[0]
        self.lines[1] = self.ax.plot([], [])[0]

    def change_view(self):
        """
        Plot view switcher using a boolean to check which one is active.
        """
        # TODO plots need to be removed or hidden before display one or another, currently they are getting overlapped
        #  and it is visible
        if len(self.data) > 0:
            self.single_plot = not self.single_plot
            self.view_plot()

    def plot_data(self):
        print("plot_data()")
        self.values_x = []
        self.values_y = [[] for _ in range(len(self.selected_ys))]
        intervalo = 1
        for i in range(0, len(self.data), intervalo):
            for j, value in enumerate(self.selected_ys):
                self.values_y[j].append(self.data[i][value])
            self.values_x.append(self.data[i][self.selected_x[0]])

        for sub_y in range(len(self.selected_ys)):
            self.lines[sub_y].set_xdata(self.values_x)
            self.lines[sub_y].set_ydata(self.values_y[0])
        self.ax.set_xlim(0, max(self.values_x))
        self.ax.set_ylim(min(self.values_y[0]) * 0.9, max(self.values_y[0]) * 1.1)

        self.ax.set_xlabel(Fields[self.selected_x[0]])
        self.ax.set_ylabel(Fields[self.selected_ys[0]])

        self.canvas.draw()

    def enable_live_data(self):
        if self.live_data_enabled:
            self.label_arduino_status['text'] = "Disconnected"
            self.label_arduino_status['fg'] = "blue"
            arduino.close()
            self.live_data_enabled = False
        else:
            self.label_arduino_status['text'] = "Connecting..."
            self.label_arduino_status['fg'] = "blue"
            connected = arduino.connect_to_arduino()
            if connected:
                self.label_arduino_status['text'] = "Connected"
                self.label_arduino_status['fg'] = "green"
                self.live_data_enabled = True
            else:
                self.label_arduino_status['text'] = "Port not found"
                self.label_arduino_status['fg'] = "red"

    def plot_live_data(self):
        global counter, y_data, x_data
        # optimize
        if self.live_data_enabled:

            line = import_live_data()
            counter += 100
            if len(y_data[0]) < 100:
                for sub_y in range(len(self.selected_ys)):
                    y_data[sub_y].append(line[self.selected_ys[sub_y]] * randint(0, 20))
                # x_axis_data.append(line[self.selected_x[0]])
                x_data.append(counter)
                if line is not None:
                    self.data.append(line)
            else:
                for sub_y in range(len(self.selected_ys)):
                    y_data[sub_y][0:99] = y_data[sub_y][1:100]
                    y_data[sub_y][99] = line[self.selected_ys[sub_y]]

                x_data[0:99] = x_data[1:100]
                #x_data[99] = line[self.selected_x[0]]
                x_data[99] = counter

            for sub_y in range(len(self.selected_ys)):
                self.lines[sub_y].set_xdata(x_data)
                self.lines[sub_y].set_ydata(y_data[sub_y])

            self.ax.set_ylim(0, max(y_data[0]) * 1.1)
            self.ax.set_xlim(min(x_data), max(x_data))
            self.canvas.draw()

        if self.live_data_enabled:
            self.root.after(10, self.plot_live_data)

    def plot_change_xy(self, x, y):
        print("plot_change_xy()")
        self.selected_x = x
        self.selected_ys = y
        print(Fields)
        self.table['displaycolumns'] = self.selected_x + self.selected_ys
        self.plot_data()  # anterior: self.view_plot()

    def view_plot(self):
        print("view_plot()")
        """
        Display the plot, single or multi, depending which one is activated.
        """
        self.view_single_plot() if self.single_plot else self.view_multi_plot()

    def change_color_theme(self):
        self.color_theme = "dark" if self.color_theme == "default" else "default"
        self.init_common_gui()


program = MotorsportPlotter()
program.root.mainloop()
