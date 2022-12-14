from tkinter import Menu

class CustomMenu(Menu):
    def __init__(self, root, controller):
        super().__init__(root)
        self.controller = controller
        self.root = root
        self.config(bg=self.root.style.get_primary_color())


        self.add_command(label="Import", command=lambda: self.controller.import_data())
        self.add_command(label="Export", command=lambda: self.controller.export_data())
        self.add_command(label="Enable/Disable realtime", command=self.controller.enable_live_data())
        self.add_command(label="Plot realtime", command=self.controller.plot_live_data())
        self.add_command(label="Single/Multiple graphs", command=self.controller.change_view())

        # Cascade menu for different plots
        tables_menu = Menu(self, tearoff=False)
        self.add_cascade(menu=tables_menu, label="View tables")
        tables_menu.add_command(label="** View airflow")  # TODO add command=method to parameters
        tables_menu.add_command(label="View air temperature", command=self.view_air_temperature)
        tables_menu.add_command(label="** View engine block temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View gear", command=self.view_gear)
        tables_menu.add_command(label="View oil pressure", command=self.view_oil_pressure)
        tables_menu.add_command(label="** View oil temperature")  # TODO add command=method to parameters
        tables_menu.add_command(label="View throttle position and relative throttle position",
                                command=self.view_throttle_position)
        tables_menu.add_command(label="View RPM", command=self.view_rpm)
        tables_menu.add_command(label="View water temperature", command=self.view_water_temperature)
        tables_menu.add_command(label="** View water temperature IN")  # TODO add command=method to parameters
        tables_menu.add_command(label="** View water temperature OUT")  # TODO add command=method to parameters

        tables_menu.add_command(label="** View water temperature OUT")  # TODO add command=method to parameters

        self.add_command(label="Change color theme", command=self.change_color_theme)

    def view_air_temperature(self):
        self.controller.view_air_temperature(self.root)

    def view_gear(self):
        self.controller.view_gear(self.root)

    def view_oil_pressure(self):
        self.controller.view_oil_pressure(self.root)

    def view_throttle_position(self):
        self.controller.view_throttle_position(self.root)

    def view_rpm(self):
        self.controller.view_rpm(self.root)

    def view_water_temperature(self):
        self.controller.view_water_temperature(self.root)

    def change_color_theme(self):
        self.root.change_style()