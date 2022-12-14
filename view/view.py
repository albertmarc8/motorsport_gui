import os
from tkinter import LabelFrame, Label, PhotoImage

from customtkinter import CTk as Tk
import customtkinter

from view.UFSTreeview import UFSTreeview
from view.figure import CustomFigure
from view.menu import CustomMenu
from view.placeholder import CustomPlaceholder
from view.style_manager import StyleManager

class View(Tk):

    def __init__(self, controller):
        super().__init__()
        self.style = StyleManager(style_name="dark")

        self.controller = controller

        self.iconphoto(False, PhotoImage(file=os.path.join(os.path.dirname(__file__), "uji_motorsport.png")))

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

    def change_style(self):

        self.style.change_style()
        #self.control_container.reload()
        #self.table.reload()
        self.figure.set_style()
        self.control_container.set_style()

        customtkinter.set_appearance_mode(self.style.get_style_name())  # Modes: system (default), light, dark



    def plot(self, x, y, title):
        self.figure.plot(x, y, title)
        print("Plotting")
