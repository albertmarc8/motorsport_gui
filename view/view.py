import os
from tkinter import LabelFrame, Label, PhotoImage

from customtkinter import CTk as Tk
import customtkinter

from view.UFSTreeview import UFSTreeview
from view.figure import CustomFigure
from view.menu import CustomMenu
from view.placeholder import CustomPlaceholder
from view.style_manager import StyleManager
from view.table_view_selector import TableViewSelector

class View(Tk):

    def __init__(self, controller):
        super().__init__()
        self.style = StyleManager(style_name="light")

        self.controller = controller

        self.iconphoto(False, PhotoImage(file=os.path.join(os.path.dirname(__file__), "uji_motorsport.png")))

        customtkinter.set_appearance_mode(self.style.get_style_name())  # Modes: system (default), light, dark
        self.title("UJI Motorsport Plotter")
        self.geometry('1600x900')
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Menu
        self.config(menu=CustomMenu(self, self.controller))

        # Table
        self.table = TableViewSelector(self, controller)

        # Placeholders
        self.control_container = CustomPlaceholder(self)

        # Figure
        self.figure = CustomFigure(self)

        self.mainloop()

    def enable_live_data(self, status, color):
        self.control_container.toggle_live_data(status, color)

    def plot_live_data(self):
        pass

    def change_view(self):
        pass

    def change_style(self):

        self.style.change_style()
        #self.control_container.reload()
        #self.table.reload()
        self.figure.set_style()
        self.control_container.set_style()
        self.table.set_style()

        customtkinter.set_appearance_mode(self.style.get_style_name())  # Modes: system (default), light, dark

    def plot(self, x, y, title):
        self.figure.plot(x, y, title)
        print("Plotting")

    def clear_plot(self):
        self.figure.clear_plots()
