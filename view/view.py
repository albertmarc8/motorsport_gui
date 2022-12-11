from customtkinter import CTk as Tk
from customtkinter import CTkFrame as Frame
import customtkinter

from menu import CustomMenu


class View(Tk):

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.color_theme = 'default'
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark

        self.title("UJI Motorsport Plotter")
        self.geometry('1600x900')

        self.menu = CustomMenu(self, self.controller)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

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