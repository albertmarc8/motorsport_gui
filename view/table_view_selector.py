from tkinter import LabelFrame, Label, Button
from tkinter import ttk


class TableViewSelector(LabelFrame):
    def __init__(self, root, controller):
        super().__init__(root, text="controls", pady=5, background="white")
        self.root = root
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.grid(column=0, row=1, sticky="NSEW")
        """
        self.label_arduino_text = Label(self, text="Arduino Status:")
        self.label_arduino_text.grid(column=0, row=0, sticky="NSEW")
        
        self.label_arduino_status = Label(self, text="Not connected", fg='blue')
        self.label_arduino_status.grid(column=1, row=0, sticky="NSEW")
        
        self.label_time_text = Label(self, text="Moving seconds:")
        self.label_time_text.grid(column=0, row=1, sticky="NSEW")
        
        self.label_time_status = Label(self, text="ON", fg="green")
        self.label_time_status.grid(column=1, row=1, sticky="NSEW")
        """

        view_options = ["Airflow", "Air temperature", "Engine block temperature", "Gear",
                        "Oil pressure", "Oil temperature", "Throttle position", "Revolutions Per Minute",
                        "Water temperature", "Water temperature IN", "Water temperature OUT", "CLEAR"]

        options_functions = [None, self.view_air_temperature, None, self.view_gear, self.view_oil_pressure, None,
                             self.view_throttle_position, self.view_rpm, None, None, None, self.clear_view]

        self.active_buttons = [False, False, False, False, False, False, False, False, False, False, False, False]

        self.buttons = []
        index = 0
        for row in range(3):
            for column in range(4):
                button = Button(self, text=view_options[index], command=options_functions[index])
                print(f"Placing button at {index} ({column} , {row})")
                button.grid(column=column, row=row, sticky="NSEW")
                self.buttons.append(button)
                index += 1

        self.set_style()

    def set_style(self):
        self.config(background=self.root.style.get_primary_color(),
                    foreground=self.root.style.get_contrast_color(),
                    highlightbackground=self.root.style.get_contrast_color())

        for i in range(len(self.buttons)):
            if self.active_buttons[i]:
                self.buttons[i].configure(bg=self.root.style.get_secondary_color(),
                                          fg=self.root.style.get_contrast_color(),
                                          activebackground=self.root.style.get_secondary_color(),
                                          activeforeground=self.root.style.get_contrast_color())
            else:
                self.buttons[i].configure(bg=self.root.style.get_primary_color(),
                                          fg=self.root.style.get_contrast_color(),
                                          activebackground=self.root.style.get_secondary_color(),
                                          activeforeground=self.root.style.get_contrast_color())

        # self.label_arduino_text.config(background=self.root.style.get_primary_color(), foreground=self.root.style.get_contrast_color())

    def enable_live_data(self):
        self.controller.enable_live_data(self.root)

    def view_air_temperature(self):
        self.controller.view_air_temperature(self.root)
        self.toggle_button(1)

    def view_gear(self):
        self.controller.view_gear(self.root)
        self.toggle_button(3)

    def view_oil_pressure(self):
        self.controller.view_oil_pressure(self.root)
        self.toggle_button(4)

    def view_throttle_position(self):
        self.controller.view_throttle_position(self.root)
        self.toggle_button(6)

    def view_rpm(self):
        self.controller.view_rpm(self.root)
        self.toggle_button(7)

    def view_water_temperature(self):
        self.controller.view_water_temperature(self.root)
        self.toggle_button(8)

    def clear_view(self):
        self.controller.clear_plot(self.root)
        for i in range(len(self.active_buttons)):
            if self.active_buttons[i]:
                self.toggle_button(i)

    def toggle_button(self, index):
        if self.active_buttons[index]:
            self.active_buttons[index] = False
            self.buttons[index].configure(bg=self.root.style.get_primary_color())
        else:
            self.active_buttons[index] = True
            self.buttons[index].configure(bg=self.root.style.get_secondary_color())
