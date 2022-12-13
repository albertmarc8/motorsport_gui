from tkinter import Menu

class CustomMenu(Menu):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.root = root

        self.add_command(label="Import", command=lambda: self.controller.import_data())
        self.add_command(label="Export", command=lambda: self.controller.export_data())
        self.add_command(label="Enable/Disable realtime", command=self.controller.enable_live_data())
        self.add_command(label="Plot realtime", command=self.controller.plot_live_data())
        self.add_command(label="Single/Multiple graphs", command=self.controller.change_view())

        # Cascade menu for different plots
        tables_menu = Menu(self, tearoff=False)
        self.add_cascade(menu=tables_menu, label="View tables")
        tables_menu.add_command(label="** View airflow")  # TODO add command=method to parameters
        tables_menu.add_command(label="View air temperature", command=lambda: self.controller.view_air_temperature())
        tables_menu.add_command(label="** View engine block temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View gear", command=lambda: self.controller.view_gear())
        tables_menu.add_command(label="View oil pressure", command=lambda: self.controller.view_oil_pressure())
        tables_menu.add_command(label="** View oil temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View throttle position and relative throttle position",
                                command=lambda: self.controller.view_throttle_position())
        tables_menu.add_command(label="View RPM", command=self.view_rpm)
        tables_menu.add_command(label="View water temperature", command=lambda: self.controller.view_water_temperature())
        tables_menu.add_command(label="** View water temperature IN")  # TODO add command=method to parameters
        tables_menu.add_command(label="** View water temperature OUT")  # TODO add command=method to parameters

        tables_menu.add_command(label="** View water temperature OUT")  # TODO add command=method to parameters

        self.add_command(label="Change color theme", command=lambda: self.controller.change_color_theme())

    def view_rpm(self):
        self.controller.view_rpm(self.root)