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
                self.ax.plot(x, y, label=title)
        else:
            self.plotting_data.append((x, y, title))
            self.ax.plot(x, y, label=title)

        # self.ax.plot(x, y)
        # self.ax.set_title(title, color=self.root.style.get_contrast_color())
        self.ax.legend(loc="upper left", facecolor=self.root.style.get_primary_color(),
                       labelcolor=self.root.style.get_contrast_color())
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


    def plot_live_data(self, title):
        counter = 0
        y_data = []
        x_data = []

        self.ax.clear()
        self.canvas.draw()
        """
        line = import_live_data()



        if len(y_data[0]) < 100:
            # Si hay menos de 100 datos para una magnitud
            for sub_y in range(len(self.selected_ys)):
                # y_data guarda los valores que se van a mostrar en pantalla
                y_data[sub_y].append(line[self.selected_ys[sub_y]])







        
        if self.live_data_enabled:

            line = import_live_data()
            counter += 100

            if len(y_data[0]) < 100:
                # Si hay menos de 100 datos para una magnitud
                for sub_y in range(len(self.selected_ys)):
                    # y_data guarda los valores que se van a mostrar en pantalla
                    y_data[sub_y].append(line[self.selected_ys[sub_y]])


                x_data.append(line[self.selected_x[0]])
                if line is not None:
                    self.data.append(line)

            else:
                # Si ya hay 100 datos
                for sub_y in range(len(self.selected_ys)):
                    y_data[sub_y][0:99] = y_data[sub_y][1:100]
                    y_data[sub_y][99] = line[self.selected_ys[sub_y]]

                x_data[0:99] = x_data[1:100]
                x_data[99] = line[self.selected_x[0]]
                #x_data[99] = counter

            for sub_y in range(len(self.selected_ys)):
                self.lines[sub_y].set_xdata(x_data)
                self.lines[sub_y].set_ydata(y_data[sub_y])

            self.ax.set_ylim(0, max(y_data[0]) * 1.1)
            self.ax.set_xlim(min(x_data), max(x_data))
            self.canvas.draw()

        if self.live_data_enabled:
            self.root.after(10, self.plot_live_data)
        """