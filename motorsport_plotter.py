from random import randint, random

import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import Treeview

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from utils.IO import *
from utils.field_names_constants import Fields

hist_data = []
shown_data = []
cond = True
counter = 0
counter_tot = 0
x_axis_data = []


class MotorsportPlotter:
    # Styling parameters
    pad_cont = 5
    single_plot = True
    live_data_enabled = False

    def __init__(self):
        # GUI
        self.label_arduino = None
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
        self.init_common_GUI()

    def init_common_GUI(self):
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
        # self.my_menu.add_command(label="Single/Multiple graphs", command=self.change_view)

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

        self.figure = Figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky=NSEW, pady=(0, 50))
        self.canvas.draw()

        # Plot navigation
        self.toolbarFrame = Frame(master=self.root)
        self.toolbarFrame.grid(column=0, row=0, columnspan=2, sticky="ews")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

        # Table
        self.table = Treeview(self.root, columns=([Fields[n] for n in range(len(Fields))]))
        self.table['show'] = 'headings'  # deletes the initial column without data (that is used for indexes/ids)
        self.table['displaycolumns'] = ()
        self.table_vsb = Scrollbar(self.root, orient="vertical")
        self.table.configure(yscrollcommand=self.table_vsb.set)
        self.table_vsb.configure(command=self.table.yview)
        for n in range(len(Fields)):
            self.table.heading(n, text=Fields[n])
        self.table.grid(column=0, row=1, sticky="NSEW", padx=(0, 20))
        self.table_vsb.grid(column=0, row=1, sticky="NSE")

        # Placeholders
        self.control_container = LabelFrame(self.root, text="controls", padx=60, pady=30)
        self.control_container.columnconfigure(0, weight=1)
        self.control_container.columnconfigure(1, weight=1)
        self.control_container.rowconfigure(0, weight=1)
        self.control_container.rowconfigure(1, weight=1)
        self.control_container.rowconfigure(2, weight=1)
        self.control_container.rowconfigure(3, weight=1)
        self.control_container.grid(column=1, row=1, sticky="NSEW")

        self.label_arduino = Label(self.control_container, text="Arduino status: Not connected")
        self.label_arduino.grid(column=0, row=0)

        self.view_plot()

    def view_multi_plot(self):
        # TODO some error appears uppon using this method
        # TODO fix RAM problems, if possible
        if self.data is None:
            return None

        seconds = [vars[0] for vars in self.data]
        rpms = [vars[10] for vars in self.data]

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
        for ax in self.axs.flat:
            ax.set_title("Data plot")
            ax.plot(seconds, rpms)


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
        print("view_single_plot()")
        # if len(self.data) > 0:
        # if self.figure is not None:
        #     self.figure = None
        # if self.canvas is not None:
        #     self.canvas = None

        # Dibujando plot

        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Realtime Data")
        self.ax.set_ylabel("Y")
        self.ax.set_xlabel("Miliseconds")
        self.lines = self.ax.plot([], [])[0]



    def change_view(self):
        """
        Plot view switcher using a boolean to check which one is active.
        """
        print("change_view()")
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
        self.lines.set_xdata(self.values_x)
        self.lines.set_ydata(self.values_y[0])
        self.ax.set_xlim(0, max(self.values_x))
        self.ax.set_ylim(min(self.values_y[0]) * 0.9, max(self.values_y[0]) * 1.1)
        print(self.ax.get_autoscale_on())

        self.canvas.draw()

    def enable_live_data(self):
        if self.live_data_enabled:
            self.live_data_enabled = False
            self.label_arduino['text'] = "Arduino status: Disconnected"
            arduino.ser.close()
        else:
            self.label_arduino['text'] = "Arduino status: Connecting..."
            connected = arduino.connect_to_arduino()
            if connected:
                self.label_arduino['text'] = "Arduino status: Connected"
                self.live_data_enabled = True
            else:
                self.label_arduino['text'] = "Arduno status: Port not found"

    def plot_live_data(self):
        global cond, counter, counter_tot, shown_data, hist_data, x_axis_data

        if self.live_data_enabled:
            line = import_live_data()
            counter += 100;
            if len(shown_data) < 100:

                shown_data = np.append(shown_data, line[10]*randint(0, 5))
                # x_axis_data.append(line[self.selected_x[0]])
                x_axis_data.append(counter)
                print(f"({line[self.selected_x[0]]} , {line[self.selected_ys[0]]}")
                if line is not None:
                    self.data.append(line)
                    print(len(self.data))

            else:
                shown_data[0:99] = shown_data[1:100]
                shown_data[99] = line[self.selected_ys[0]]
                x_axis_data[0:99] = x_axis_data[1:100]
                #x_axis_data[99] = line[self.selected_x[0]]
                x_axis_data[99] = counter;

            self.lines.set_xdata(x_axis_data)
            self.lines.set_ydata(shown_data)
            self.ax.set_ylim(0, max(shown_data) * 1.1)
            self.ax.set_xlim(min(x_axis_data), max(x_axis_data))
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


program = MotorsportPlotter()
program.root.mainloop()
