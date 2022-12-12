from tkinter import LabelFrame, Label

from customtkinter import CTk as Tk
import customtkinter

from view.UFSTreeview import UFSTreeview
from view.menu import CustomMenu


class View(Tk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.color_theme = 'default'
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark

        self.title("UJI Motorsport Plotter")
        self.geometry('1600x900')

        self.config(menu=CustomMenu(self, self.controller))

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        # Table
        self.table = UFSTreeview(self)

        # Placeholders
        self.control_container = LabelFrame(self, text="controls", pady=5)
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
        #self.view_plot()





        #self.configure(background='light blue')
        #self.resizable(False, False)
        #self.create_widgets()
        self.mainloop()

    def enable_live_data(self):
        pass

    def plot_live_data(self):
        pass

    def change_view(self):
        pass

    def change_color_theme(self):
        pass