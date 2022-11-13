import tkinter
from tkinter import filedialog as fd, ttk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar
from matplotlib.figure import Figure


def read_data(file):
    data = []
    for line in open(file).readlines():
        left, right = line.rstrip().split(",")
        left1, left2 = left.split(" ")
        _, right1, right2 = right.split(" ")  # alternativa: right1, right2 = right.lstrip().split(" ")
        left1 = left1.replace("[", "")
        right2 = right2.replace("]", "")
        data.append([left1, int(left2), int(right1), right2])
    return data


def read_data2(file):

    def line_convert(info):
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





def show_plot():
    pass


def show_window_grid():
    # Caracteristicas principales ventana
    my_data = []
    window = Tk()
    window.title("UJI Formula Student Data Reader")
    window.geometry("1024x768")

    # Menu
    my_menu = Menu(window)
    window.config(menu=my_menu)

    # Grid
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=14)
    window.rowconfigure(2, weight=5)

    # Dispersion de datos
    espaciado_frame = Frame(window)
    espaciado_label = Label(espaciado_frame, text="Introduce intervalo entre datos:")
    espaciado_entry = Entry(espaciado_frame)
    espaciado_frame.grid(column=1, row=2, columnspan=2)
    espaciado_label.grid(column=0, row=0)
    espaciado_entry.grid(column=1, row=0)

    # Tabla y vertical scrollbar
    tabla = ttk.Treeview(window, columns=('Seconds', 'Throttle position', "Rel. throttle position"))
    tabla['show'] = 'headings'  # para eliminar una columna inicial sin datos (usada para indices/identificadores)
    tabla_vsb = ttk.Scrollbar(window, orient="vertical")
    tabla.configure(yscrollcommand=tabla_vsb.set)
    tabla_vsb.configure(command=tabla.yview)
    tabla.heading(0, text="Seconds")
    tabla.heading(1, text="Throttle position")
    tabla.heading(2, text="Rel. throttle position")
    tabla.grid(column=0, row=2, sticky=tkinter.NSEW, padx=(0, 20))
    tabla_vsb.grid(column=0, row=2, sticky='ens')

    # Gráfica
    figure = Figure(figsize=(5, 4), dpi=100)




    previous_subplot = None
    previous_subplot_2 = None
    chart = None
    # Metodos botones menu
    def import_data():
        filename = fd.askopenfilename(defaultextension="txt")
        nonlocal my_data
        my_data = read_data2(filename)

    def view_data():
        if len(my_data) > 0:
            # Borrando y añadiendo nuevos datos a tabla
            tabla.delete(*tabla.get_children())
            x = []
            y = []
            z = []
            respuesta = espaciado_entry.get()
            intervalo = 1
            if len(respuesta) > 0 and respuesta.isnumeric():
                intervalo = int(respuesta)

            for i in range(0, len(my_data), intervalo):
                tabla.insert('', 'end', values=(my_data[i][0], my_data[i][13], my_data[i][14]))
                x.append(my_data[i][0])
                y.append(my_data[i][13])
                z.append(my_data[i][14])

            # Dibujando plot
            nonlocal previous_subplot
            if previous_subplot is not None:
                previous_subplot.clear()

            nonlocal previous_subplot_2
            if previous_subplot_2 is not None:
                previous_subplot_2.clear()

            nonlocal chart
            if chart is not None:
                chart = None

            # else:
            #   canvas.draw()
            #  canvas.get_tk_widget().grid(column=0, row=1, sticky=NSEW)
            # previous_subplot = figure.add_subplot().plot(x, y)
            # TODO x and y axis get bugged uppon displaying it several times

            show_plot()
            #canvas.get_tk_widget().pack_forget()
            #chart = figure.add_subplot()
            #chart.set_ylabel("Throttle Positions")
            #chart.set_xlabel("Seconds")

            fig, axs = plt.subplots(2, 2, figsize=(5, 4))
            for ax in axs.flat:
                 ax.set_title("Data plot")
                 ax.plot(x, y)

            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.get_tk_widget().grid(column=0, row=1, columnspan=2, sticky=NSEW)

            # Navegación grafica
            toolbar_grafica = Frame(master=window)
            toolbar_grafica.grid(column=0, row=1, columnspan=2, sticky="ewn")
            navigation_toolbar = NavigationToolbar(canvas, toolbar_grafica)

            
            #previous_subplot = chart.plot(x, y)
            #previous_subplot_2 = chart.plot(x, z)
            canvas.draw()

    def export_data():
        if len(my_data) > 0:
            filename = fd.asksaveasfile(mode="w", defaultextension=".csv")
            sep = ";"  # delimitador CSV
            intervalo = int(espaciado_entry.get()) if espaciado_entry.get().isnumeric() else 1
            for i in range(0, len(my_data), intervalo):
                filename.write(
                    f"{my_data[i][0]}{sep}{my_data[i][1]}{sep}{my_data[i][2]}{sep}{my_data[i][3]}\n")
            filename.close()


    # Acciones botones menu
    my_menu.add_command(label="Import", command=import_data)
    my_menu.add_command(label="View", command=view_data)
    my_menu.add_command(label="Export", command=export_data)
    tables_menu = Menu(my_menu)
    my_menu.add_cascade(menu=tables_menu, label="View tables")
    tables_menu.add_command(label="View airflow")
    tables_menu.add_command(label="View engine block temperature")
    tables_menu.add_command(label="View oil pressure")
    tables_menu.add_command(label="View oil temperature")
    tables_menu.add_command(label="View water temperature IN")
    tables_menu.add_command(label="View water temperature OUT")

    # Ejecuta la ventana
    window.mainloop()


def show_window():
    # Caracteristicas principales ventana
    my_car_data = []
    window = Tk()
    window.title("UJI Formula Student Data Reader")
    window.geometry("1024x768")

    # Menu
    my_menu = Menu(window)
    window.config(menu=my_menu)

    # Tabla y vertical scroll bar (vsb)
    tv = ttk.Treeview(window, columns=(0, 1, 2, 3))
    vsb = ttk.Scrollbar(window, orient="vertical")
    vsb.pack(side=tkinter.RIGHT, fill='y', expand=True)
    tv.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    tv.configure(yscrollcommand=vsb.set)
    vsb.configure(command=tv.yview)
    tv.heading(0, text="Data #1")
    tv.heading(1, text="Index")
    tv.heading(2, text="Value")
    tv.heading(3, text="Data #4")

    # Gráfica
    grafica = tkinter.Label(window)
    grafica['text'] = "Gráfica"
    grafica.pack()
    figure = Figure(figsize=(5, 4), dpi=100)

    # Metodos botones menu
    def import_data():
        filename = fd.askopenfilename(defaultextension="txt")
        nonlocal my_car_data
        my_car_data = read_data(filename)

    def view_data():
        if len(my_car_data) > 0:
            tv.delete(*tv.get_children())
            x = []
            y = []
            yy = []

            # for i in range(100):
            for i in range(len(my_car_data)):
                tv.insert('', 'end',
                          values=(my_car_data[i][0], my_car_data[i][1], my_car_data[i][2], my_car_data[i][3]))
                # if (i % 20) == 0:
                x.append(my_car_data[i][1])
                y.append(my_car_data[i][2])

            # n = len(my_car_data)
            # b = [1.0 / n] * n
            # a = 1
            # yy = lfilter(b, a, y)
            # TODO se duplica el subplot, ver como actualizar, o borrar anterior y poner uno nuevo
            figure.add_subplot(111).plot(x, y)
            chart = FigureCanvasTkAgg(figure, master=window)
            chart.draw()
            chart.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.NSEW, expand=1)

            plt.grid()
            axes = plt.axes()
            axes.set_xlim([0, 10])
            axes.set_ylim([[0, 10]])

    def export_data():
        if len(my_car_data) > 0:
            filename = fd.asksaveasfile(mode="w", defaultextension=".csv")
            sep = ";"  # delimitador CSV
            for i in range(len(my_car_data)):
                filename.write(
                    f"{my_car_data[i][0]}{sep}{my_car_data[i][1]}{sep}{my_car_data[i][2]}{sep}{my_car_data[i][3]}\n")
            filename.close()

    # Acciones botones menu
    my_menu.add_command(label="Import", command=import_data)
    my_menu.add_command(label="View", command=view_data)
    my_menu.add_command(label="Export", command=export_data)

    # Ejecuta la ventana
    window.mainloop()


if __name__ == '__main__':
    show_window_grid()
