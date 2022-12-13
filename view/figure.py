from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from customtkinter import CTkFrame as Frame
from customtkinter import CTk as Tk


class CustomFigure(Figure):
    def __init__(self, root):
        super().__init__()
        self.ax = self.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self, master=root)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky="NSEW", pady=(0, 50))
        self.canvas.draw()

        # Plot navigation
        self.toolbarFrame = Frame(master=root)
        self.toolbarFrame.grid(column=0, row=0, columnspan=2, sticky="ews")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def plot(self, x, y, title):
        self.ax.clear()

        self.ax.plot(x, y)
        self.ax.set_title(title)
        self.ax.ticklabel_format(useOffset=False, style='plain')
        self.canvas.draw()
