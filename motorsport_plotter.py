import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class MotorsportPlotter:
    # Styling parameters
    pad_containers = 5
    single_plot = False

    def __init__(self, root):
        self.figure = None
        self.chart = None
        self.previous_subplot_2 = None
        self.previous_subplot = None
        self.filename = None
        self.table = None
        self.data = None
        self.root = root
        self.root.title("UJI Motorsport Plotter")
        self.root.geometry('1600x900')

        # Window menu
        my_menu = Menu(self.root)
        self.root.config(menu=my_menu)
        my_menu.add_command(label="Import", command=self.import_data)
        my_menu.add_command(label="View", command=self.view_plot)  # TODO add command=method to parameters
        my_menu.add_command(label="Export", command=self.export_data)  # TODO add command=method to parameters
        my_menu.add_command(label="Single/Multiple graphs", command=self.change_view)
        tables_menu = Menu(my_menu)
        my_menu.add_cascade(menu=tables_menu, label="View tables") # TODO fix a line that appears and duplicates the dropdown
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
        import_btn = Button(control_container, text="Import data from .txt", command=self.import_from_txt)
        # import_btn.pack()

        # Plot Button
        plot_btn = Button(control_container, text="Plot data", command=self.view_multi_plot)
        # plot_btn.pack()

        # Export Button
        plot_btn = Button(control_container, text="Export data to .csv", command=self.export_to_csv)
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

    def plot_on_start(self):
        self.filename = "datos_task/coche_reduced.txt"
        # 1. Read the file:
        with open(self.filename, "r") as f:
            # 2. Iterate and get values from all lines
            self.data = [(int(seconds), int(rpms)) for seconds, rpms in
                         [line[7:-8].split(", ") for line in f.readlines()]]
        self.plot_data()

    def import_from_txt(self):
        """
        Asks the user to select a txt file in which each line follows
        the regex [0x001 seconds, rpms 0x001]
        stores a resulting matix with shape (n, 2) being n the number
        of non-empty lines in the file
        """

        self.filename = filedialog.askopenfilename(filetypes=(('text files', '*.txt'),))

        # 1. Read the file:
        with open(self.filename, "r") as f:
            # 2. Iterate and get values from all lines
            self.data = [(int(seconds), int(rpms)) for seconds, rpms in
                         [line[7:-8].split(", ") for line in f.readlines()]]

    def export_to_csv(self):
        """
        Saves 'self.data' into a file in the same folder as the txt
        but with a csv filetype.
        WARNING: It will remove the file with csv if it already exists
        """

        # 0. Check if a datafile has been loaded
        if self.filename is None:
            return None  # Todo: mensaje de error

        # 1. Get the right path
        filename = self.filename.rstrip("txt")
        filename += "csv"

        # 2. Open the file
        with open(filename, "w") as f:
            # 3. Strore data as csv
            [f.write(line) for line in [",".join([str(d[0]), str(d[1])]) + "\n" for d in self.data]]

    def import_data(self):
        def read_data(file):
            """
            Opens a dialog and asks the user to select a file from which It can read the data from.

            :param file: Reads the specified file line by line.
            :return: Returns a 2d array with int/float/string variables from the file.
            """
            def line_convert(info):
                """
                Converts a line from the files to an array with correct data types.

                :param info: The line that will be converted into an array.
                :return: The properly formatted array containing ints, floats and strings.
                """
                variables = info.rstrip().split(",")

                # Conversion: strings -> int
                for num_i in {0, 2, 3, 8, 9, 11, 18, 19}:
                    variables[num_i] = int(variables[num_i])

                # Conversion: strings -> float
                for num_f in {4, 5, 6, 7, 10, 12, 13, 14, 15, 16, 17}:
                    variables[num_f] = float(variables[num_f])

                # Taking into consideration the 2 kind of files, one with 20 fields and another with 22 (starting to count from 0)
                if len(variables) == 21:
                    for num_i in {20, 21}:
                        variables[num_i] = int(variables[num_i])
                return variables

            data = []
            for line in open(file).readlines():
                data.append(line_convert(line))

            return data

        filename = filedialog.askopenfilename(defaultextension="txt")
        self.data = read_data(filename)

    def export_data(self):
        """
            Exports the data to a CSV using the ; as a separator (European standards).
            File can be saved with any name and no file format is needed to be specified at the end.

        :return: Method does not return anything.
        """
        if len(self.data) > 0:
            filename = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
            sep = ";"  # delimitador CSV
            intervalo = 1 #intervalo = int(espaciado_entry.get()) if espaciado_entry.get().isnumeric() else 1

            for i in range(0, len(self.data), intervalo):
                str2print = ""
                for j in range(0, len(self.data[i])-1, intervalo):
                    str2print += str(self.data[i][j]) + ";"
                str2print += str(self.data[i][j]) + ";\n"
                filename.write(str2print)
            filename.close()

    def view_multi_plot(self):
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

        #self.table.place(x=0, y=720, height=380, width=1280)
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

        #frame = Frame(self.root)
        #frame.grid(column=0, row=0, columnspan=2, sticky=NSEW, padx=self.pad_containers, pady=self.pad_containers)

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
