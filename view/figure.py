from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from customtkinter import CTkFrame as Frame
from customtkinter import CTk as Tk


class CustomFigure(Figure):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.ax = self.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self, master=root)
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky="NSEW", pady=(0, 50))

        # Set default colors
        """
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
        """
        self.ax.set_facecolor(root.style.get_primary_color())
        self.set_facecolor(root.style.get_primary_color())
        self.ax.spines['bottom'].set_color(root.style.get_contrast_color())
        self.ax.spines['top'].set_color(root.style.get_contrast_color())
        self.ax.spines['right'].set_color(root.style.get_contrast_color())
        self.ax.spines['left'].set_color(root.style.get_contrast_color())
        self.ax.tick_params(axis='x', colors=root.style.get_contrast_color())
        self.ax.tick_params(axis='y', colors=root.style.get_contrast_color())


        self.canvas.draw()

        # Plot navigation
        self.toolbarFrame = Frame(master=root)
        self.toolbarFrame.grid(column=0, row=0, columnspan=2, sticky="ews")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def plot(self, x, y, title):
        self.ax.clear()

        self.ax.plot(x, y)
        self.ax.set_title(title, color=self.root.style.get_contrast_color())
        self.ax.ticklabel_format(useOffset=False, style='plain')
        self.canvas.draw()
