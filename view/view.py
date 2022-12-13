from tkinter import LabelFrame, Label

from customtkinter import CTk as Tk
import customtkinter

from view.UFSTreeview import UFSTreeview
from view.figure import CustomFigure
from view.menu import CustomMenu
from view.placeholder import CustomPlaceholder


class View(Tk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.color_theme = 'default'
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark

        self.title("UJI Motorsport Plotter")
        self.geometry('1600x900')

        self.config(menu=CustomMenu(self, self.controller))
        self.figure = CustomFigure(self)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        # Table
        self.table = UFSTreeview(self)

        # Placeholders
        self.control_container = CustomPlaceholder(self)
        #self.view_plot()
        self.figure = CustomFigure(self)




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

    def plot(self, x, y, title):
        self.figure.plot(x, y, title)
        print("Plotting")
