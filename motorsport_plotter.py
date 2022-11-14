import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from utils.IO import *


class MotorsportPlotter:
    # Styling parameters
    pad_containers = 5
    single_plot = False

    def __init__(self, r):
        self.figure = None
        self.chart = None
        self.previous_subplot_2 = None
        self.previous_subplot = None
        self.filename = None
        self.table = None
        self.data = []
        self.root = r
        self.root.title("UJI Motorsport Plotter")
        self.root.geometry('1600x900')

        # Window menu
        my_menu = Menu(self.root)
        self.root.config(menu=my_menu)
        my_menu.add_command(label="Import", command=lambda: import_data(self.data))
        my_menu.add_command(label="View", command=self.view_plot)  # TODO add command=method to parameters
        my_menu.add_command(label="Export", command=lambda: export_data(self.data))  # TODO add command=method to parameters
        my_menu.add_command(label="Single/Multiple graphs", command=self.change_view)
        tables_menu = Menu(my_menu)
        my_menu.add_cascade(menu=tables_menu,
                            label="View tables")  # TODO fix a line that appears and duplicates the dropdown
        tables_menu.add_command(label="View airflow")  # TODO add command=method to parameters
        tables_menu.add_command(label="View engine block temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View oil pressure")  # TODO add command=method to parameters
        tables_menu.add_command(label="View oil temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View water temperature IN")  # TODO add command=method to parameters
        tables_menu.add_command(label="View water temperature OUT")  # TODO add command=method to parameters

        # Grid system declaration
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)

        control_container = LabelFrame(self.root, text="controls", padx=60, pady=30)
        # Import Button
        import_btn = Button(control_container, text="Import data from .txt", command=import_from_txt)
        # import_btn.pack()

        # Plot Button
        plot_btn = Button(control_container, text="Plot data", command=self.view_multi_plot)
        # plot_btn.pack()

        # Export Button
        plot_btn = Button(control_container, text="Export data to .csv", command=export_to_csv)
        # plot_btn.pack()
        control_container.grid(column=1, row=1, sticky=NSEW, padx=self.pad_containers, pady=self.pad_containers)

        self.chart_label_frame = LabelFrame(self.root, text="chart")  # , padx=750, pady=300)
        Label(self.chart_label_frame, text="TELEMETRY CHART", font=("Arial", 25)).place(relx=.5, rely=.5,
                                                                                        anchor=CENTER)
        self.chart_label_frame.grid(column=0, row=0, columnspan=2, sticky=NSEW, padx=self.pad_containers,
                                    pady=self.pad_containers)

        self.table_label_frame = LabelFrame(self.root, text="table")
        Label(self.table_label_frame, text="TELEMETRY TABLE", font=("Arial", 25)).place(relx=.5, rely=.5,
                                                                                        anchor=CENTER)
        self.table_label_frame.grid(column=0, row=1, sticky=NSEW, padx=self.pad_containers, pady=self.pad_containers)
        # table_label_frame.place(x=40, y=720, width=1200, height=330)

        self.toolbar = None
        # self.plot_on_start()


    def view_multi_plot(self):
        # TODO some error appears uppon using this method
        # TODO fix RAM problems, if possible
        if self.data is None:
            return None

        seconds = [vars[0] for vars in self.data]
        rpms = [vars[10] for vars in self.data]

        # Represent the table
        self.table = Treeview(self.root)
        self.table["columns"] = ("Second", "RPMs")

        self.table.heading("#0", text="", anchor=W)
        self.table.heading("Second", text="Second", anchor=W)
        self.table.heading("RPMs", text="RPMs", anchor=W)

        [self.table.insert(parent="", index="end", iid=i, text="", values=d) for i, d in enumerate(self.data)]

        # self.table.place(x=0, y=720, height=380, width=1280)
        self.table.grid(column=0, row=1, sticky=NSEW, padx=self.pad_containers, pady=self.pad_containers)
        self.root.update()

        # Represent the plot
        """fig = plt.figure(figsize=(5,4), dpi=100)
        fig.add_subplot(111).plot(seconds, rpms)
        fig.add_subplot(121).plot(seconds, rpms)
        fig.add_subplot(131).plot(seconds, rpms)"""
        fig, axs = plt.subplots(2, 2, figsize=(5, 4))
        for ax in axs.flat:
            ax.set_title("Data plot")
            ax.plot(seconds, rpms)

        # frame = Frame(self.root)
        # frame.grid(column=0, row=0, columnspan=2, sticky=NSEW, padx=self.pad_containers, pady=self.pad_containers)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky=NSEW)

        if self.toolbar is None:
            self.toolbar = NavigationToolbar2Tk(canvas, self.root)
            self.toolbar.grid(column=0, row=0, columnspan=2, sticky="ews")
        """
        figure = plt.figure(figsize=(20,7), dpi=100)
        figure.add_subplot(111).plot(seconds, rpms)
        chart = FigureCanvasTkAgg(figure, self.root)
        #chart.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=3, sticky="we")
        chart.get_tk_widget().place(x=0, y=0)
        """

    def view_single_plot(self):
        """
        Displays a single plot on the main view.

        :return: Method does not return anything.
        """
        # TODO fix RAM problems, if possible
        if self.table is None:
            self.chart_label_frame.destroy()
            self.table_label_frame.destroy()
            self.table = Treeview(self.root, columns=('Seconds', 'Throttle position', 'Rel. throttle position'))
            self.table[
                'show'] = 'headings'  # para eliminar una columna inicial sin datos (usada para indices/identificadores)
            tabla_vsb = Scrollbar(self.root, orient="vertical")
            self.table.configure(yscrollcommand=tabla_vsb.set)
            tabla_vsb.configure(command=self.table.yview)
            self.table.heading(0, text="Seconds")
            self.table.heading(1, text="Throttle position")
            self.table.heading(2, text="Rel. throttle position")
            self.table.grid(column=0, row=1, sticky="NSEW", padx=(0, 20))
            tabla_vsb.grid(column=0, row=1, sticky="NSE")

        if len(self.data) > 0:
            # Borrando y añadiendo nuevos datos a tabla
            self.table.delete(*self.table.get_children())
            x = []
            y = []
            z = []
            # respuesta = espaciado_entry.get()
            intervalo = 1
            # if len(respuesta) > 0 and respuesta.isnumeric():
            #    intervalo = int(respuesta)

            for i in range(0, len(self.data), intervalo):
                self.table.insert('', 'end', values=(self.data[i][0], self.data[i][13], self.data[i][14]))
                x.append(self.data[i][0])
                y.append(self.data[i][13])
                z.append(self.data[i][14])

            # Dibujando plot
            if self.previous_subplot is not None:
                self.previous_subplot = None

            if self.previous_subplot_2 is not None:
                self.previous_subplot_2 = None

            if self.chart is not None:
                self.chart = None

            # previous_subplot = figure.add_subplot().plot(x, y)
            # TODO x and y axis get bugged uppon displaying it several times
            if self.figure is not None:
                self.figure = None
            self.figure = Figure(figsize=(5, 4), dpi=100)
            canvas = FigureCanvasTkAgg(self.figure, master=self.root)

            chart = self.figure.add_subplot()
            chart.set_ylabel("Throttle Positions")
            chart.set_xlabel("Seconds")
            canvas = FigureCanvasTkAgg(self.figure, master=self.root)
            canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, sticky=NSEW, pady=(0, 50))

            # Navegación grafica
            toolbar_grafica = Frame(master=self.root)
            toolbar_grafica.grid(column=0, row=0, columnspan=2, sticky="ews")
            navigation_toolbar = NavigationToolbar2Tk(canvas, toolbar_grafica)

            self.previous_subplot = chart.plot(x, y)
            self.previous_subplot_2 = chart.plot(x, z)
            canvas.draw()

    def change_view(self):
        """
        Plot view switcher using a boolean to check which one is active.
        """
        if self.single_plot:
            self.view_multi_plot()
            self.single_plot = False
        else:
            self.view_single_plot()
            self.single_plot = True

    def view_plot(self):
        """
        Display the plot, single or multi, depending which one is activated.
        """
        if self.single_plot:
            self.view_single_plot()
        else:
            self.view_multi_plot()


root = Tk()
program = MotorsportPlotter(root)
program.root.mainloop()
