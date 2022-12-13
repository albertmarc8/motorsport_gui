from model import Model
from view.view import View
from matplotlib import pyplot as plt


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def import_data(self):
        self.model.import_data()

    def export_data(self):
        self.model.export_data()

    def enable_live_data(self):
        pass

    def plot_live_data(self):
        pass

    def change_view(self):
        pass

    def view_air_temperature(self, view):
        view.plot(self.model.get_seconds(), self.model.get_air_temperature(), "RPM")


    def view_gear(self, view):
        view.plot(self.model.get_seconds(), self.model.get_gear(), "Gear")

    def view_oil_pressure(self, view):
        view.plot(self.model.get_seconds(), self.model.get_oil_pressure(), "Oil Pressure")

    def view_throttle_position(self, view):
        view.plot(self.model.get_seconds(), self.model.get_relative_throttle_position(), "Throttle Position")

    def view_rpm(self, view):
        view.plot(self.model.get_seconds(), self.model.get_rpms(), "RPM")

    def view_water_temperature(self, view):
        view.plot(self.model.get_seconds(), self.model.get_water_temperature(), "Water Temperature")

    def change_color_theme(self):
        pass

if __name__ == '__main__':
    controller = Controller()
    controller.import_data()
    #controller.view_rpm()
