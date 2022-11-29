from tkinter import filedialog

from utils.arduinoreceiver import ArduinoReceiver

arduino = ArduinoReceiver()
connected_to_arduino = False


def export_data(data):
    """
        Exports the data to a CSV using the ; as a separator (European standards).
        File can be saved with any name and no file format is needed to be specified at the end.

    :return: Method does not return anything.
    """
    if len(data) > 0:
        filename = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
        sep = ";"  # delimitador CSV
        intervalo = 1  # intervalo = int(espaciado_entry.get()) if espaciado_entry.get().isnumeric() else 1

        for i in range(0, len(data), intervalo):
            str2print = ""
            for j in range(0, len(data[i]) - 1, intervalo):
                str2print += str(data[i][j]) + ";"
            str2print += str(data[i][j]) + ";\n"
            filename.write(str2print)
        filename.close()


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


def import_data(data, table):
    # TODO added table to method parameters but it is a bit slower for some reason
    def read_data(file, table):
        """
            Opens a dialog and asks the user to select a file from which It can read the data from.

        :param file: Reads the specified file line by line.
        :return: Returns a 2d array with int/float/string variables from the file.
        """
        # data = []
        for line in open(file).readlines():
            converted_line = line_convert(line)
            data.append(converted_line)
            table.insert('', 'end', values=converted_line)

        return data

    filename = filedialog.askopenfilename(defaultextension="txt")
    return read_data(filename, table)


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


def import_live_data():
    return line_convert(arduino.read_from_arduino())


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
    if len(variables) == 22:
        for num_i in {20, 21}:
            variables[num_i] = int(variables[num_i])
    return variables


def plot_on_start(self):
    self.filename = "datos_task/coche_reduced.txt"
    # 1. Read the file:
    with open(self.filename, "r") as f:
        # 2. Iterate and get values from all lines
        self.data = [(int(seconds), int(rpms)) for seconds, rpms in
                     [line[7:-8].split(", ") for line in f.readlines()]]
    self.view_multi_plot()
