from _tkinter import TclError

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
        self.plotting_data = []


        # Plot navigation
        self.toolbarFrame = Frame(master=root)
        self.toolbarFrame.grid(column=0, row=0, columnspan=2, sticky="ews")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

        self.set_style()
        self.canvas.draw()

    def set_style(self):
        # Set default colors
        self.ax.set_facecolor(self.root.style.get_primary_color())
        self.set_facecolor(self.root.style.get_primary_color())
        self.ax.spines['bottom'].set_color(self.root.style.get_contrast_color())
        self.ax.spines['top'].set_color(self.root.style.get_contrast_color())
        self.ax.spines['right'].set_color(self.root.style.get_contrast_color())
        self.ax.spines['left'].set_color(self.root.style.get_contrast_color())
        self.ax.tick_params(axis='x', colors=self.root.style.get_contrast_color())
        self.ax.tick_params(axis='y', colors=self.root.style.get_contrast_color())
        self.canvas.draw()

        self.toolbar.config(background=self.root.style.get_secondary_color())
        for widget in self.toolbar.winfo_children():
            widget.config(background=self.root.style.get_primary_color(),
                          highlightbackground=self.root.style.get_secondary_color())
            try:
                widget.config(foreground=self.root.style.get_contrast_color())
            except TclError:
                pass

        self.toolbar.pack_slaves()[0].config(background=self.root.style.get_primary_color(),
                                             highlightbackground=self.root.style.get_primary_color(),
                                             foreground=self.root.style.get_primary_color(),
                                             activebackground=self.root.style.get_primary_color(),
                                             activeforeground=self.root.style.get_primary_color())

    def plot(self, x, y, title):
        actual_titles = [title for x, y, title in self.plotting_data]
        if title in actual_titles:

            title_index_in_plotting_data = actual_titles.index(title)
            self.plotting_data.pop(title_index_in_plotting_data)
            self.ax.clear()
            for i, (x, y, title) in enumerate(self.plotting_data):
                self.ax.plot(x, y)
        else:
            self.plotting_data.append((x, y, title))
            self.ax.plot(x, y)

        #self.ax.plot(x, y)
        #self.ax.set_title(title, color=self.root.style.get_contrast_color())
        self.ax.ticklabel_format(useOffset=False, style='plain')
        self.canvas.draw()

    def clear_plots(self):
        self.ax.clear()
        self.canvas.draw()
        self.plotting_data = []

    def find_title_index_in_plotting_data(self, title):
        for i, (x, y, title) in enumerate(self.plotting_data):
            if title == title:
                return i
        return None
