from tkinter import filedialog

import pandas as plt
class Model:
    def __init__(self):
        pass

    def import_data(self):
        filename = filedialog.askopenfilename(defaultextension="txt")
        self.df = plt.read_csv(filename, header=None)

    def export_data(self):
        pass

    def enable_live_data(self):
        pass

    def get_seconds(self):
        return self.df[0]

    def get_rpms(self):
        return self.df[10]


if __name__ == '__main__':
    model = Model()
    model.import_data()
