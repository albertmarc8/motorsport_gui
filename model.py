from tkinter import filedialog
from utils.IO import *

import pandas as plt
class Model:
    def __init__(self):
        self.live_data_enabled = False
        try:
            self.df = plt.read_csv("../6508.txt", header=None)
            print("Succes reading default file.")
        except:
            print("No default file detected.")

    def import_data(self):
        filename = filedialog.askopenfilename(defaultextension="txt")
        self.df = plt.read_csv(filename, header=None)

    def export_data(self):
        pass

    def enable_live_data(self):

        """
        if self.live_data_enabled:
            self.label_arduino_status['text'] = "Disconnected"
            self.label_arduino_status['fg'] = "blue"
            arduino.close()
            self.live_data_enabled = False
        else:
            self.label_arduino_status['text'] = "Connecting..."
            self.label_arduino_status['fg'] = "blue"
            connected = arduino.connect_to_arduino()
            if connected:
                self.label_arduino_status['text'] = "Connected"
                self.label_arduino_status['fg'] = "green"
                self.live_data_enabled = True
            else:
                self.label_arduino_status['text'] = "Port not found"
                self.label_arduino_status['fg'] = "red"
        """

        if self.live_data_enabled:
            arduino.close()
            self.live_data_enabled = False
            return "Disconnected", "blue"
        else:
            connected, selected_port = arduino.connect_to_arduino()
            if connected:
                self.live_data_enabled = True
                return "Connected to " + selected_port, "green"
            else:
                return "Port not found", "red"



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

    def is_live_data_enabled(self):
        return self.live_data_enabled


if __name__ == '__main__':
    model = Model()
    model.import_data()
