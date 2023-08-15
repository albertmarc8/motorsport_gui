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
from view.big_number import BigNumber

class View(Tk):

    def __init__(self, controller):
        super().__init__()
        self.style = StyleManager(style_name="dark")

        self.controller = controller

        self.iconphoto(False, PhotoImage(file=os.path.join(os.path.dirname(__file__), "uji_motorsport.png")))

        customtkinter.set_appearance_mode(self.style.get_style_name())  # Modes: system (default), light, dark
        self.title("UJI Motorsport Plotter")
        self.geometry('1600x900')
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        # Menu
        self.config(menu=CustomMenu(self, self.controller))

        # Table
        self.table = TableViewSelector(self, controller)

        # Placeholders
        self.control_container = CustomPlaceholder(self)

        # Figure
        self.custom_figure = CustomFigure(self)
        #self.big_number = BigNumber(self)

        self.figure = self.custom_figure
        self.figure_selected = "custom_figure"

        self.mainloop()

    def enable_live_data(self, status, color):
        self.control_container.toggle_live_data(status, color)

        if status != "Disconnected":

            self.figure.plot_live_data()

        else:

            if self.figure_selected == "custom_figure":
                self.figure = CustomFigure(self)  
                
            else:
                self.figure = BigNumber(self)

    def plot_live_data(self):
        pass

    def change_view(self):
        if self.figure_selected == "custom_figure":
            self.figure_selected = "big_number"
            self.figure = BigNumber(self)
        else:
            self.figure_selected = "custom_figure"
            self.figure = CustomFigure(self)        

    def change_style(self):

        self.style.change_style()
        #self.control_container.reload()
        #self.table.reload()
        self.figure.set_style()
        self.control_container.set_style()
        self.table.set_style()

        customtkinter.set_appearance_mode(self.style.get_style_name())  # Modes: system (default), light, dark

    def plot(self, x, y, title):
        if self.controller.is_live_data_enabled():
            self.figure.plot_live_data(title)
        else:
            self.figure.plot(x, y, title)
        print("Plotting")

    def clear_plot(self):
        self.figure.clear_plots()
