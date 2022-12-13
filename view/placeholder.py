from tkinter import LabelFrame, Label

class CustomPlaceholder(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="controls", pady=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.grid(column=1, row=1, sticky="NSEW")

        self.label_arduino_text = Label(self, text="Arduino Status:")
        self.label_arduino_text.grid(column=0, row=0, sticky="NSEW")
        self.label_arduino_status = Label(self, text="Not connected", fg='blue')
        self.label_arduino_status.grid(column=1, row=0, sticky="NSEW")
        self.label_time_text = Label(self, text="Moving seconds:")
        self.label_time_text.grid(column=0, row=1, sticky="NSEW")
        self.label_time_status = Label(self, text="ON", fg="green")
        self.label_time_status.grid(column=1, row=1, sticky="NSEW")
