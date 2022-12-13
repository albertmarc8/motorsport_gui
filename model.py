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

    def get_air_temperature(self):
        return self.df[6]

    def get_gear(self):
        return self.df[20]

    def get_oil_pressure(self):
        return self.df[21]

    def get_relative_throttle_position(self):
        return self.df[13]

    def get_rpms(self):
        return self.df[10]

    def get_water_temperature(self):
        return self.df[5]


if __name__ == '__main__':
    model = Model()
    model.import_data()
