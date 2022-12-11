from model import Model
from view.view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def import_data(self):
        pass

    def export_data(self):
        pass

    def enable_live_data(self):
        pass

    def plot_live_data(self):
        pass

    def change_view(self):
        pass

    def view_air_temperature(self):
        pass

    def view_gear(self):
        pass

    def view_oil_pressure(self):
        pass

    def view_throttle_position(self):
        pass

    def view_rpm(self):
        pass

    def view_water_temperature(self):
        pass

    def change_color_theme(self):
        pass
