class StyleManager:
    def __init__(self, style_name="light"):
        if style_name == "dark":
            self.dark()
        else:
            # Init with light style
            self.style_name = "light"
            self.primary_color = "#fff"
            self.secondary_color = "lightgray"
            self.contrast_color = "#000"

    def light(self):
        self.style_name = "light"
        self.primary_color = "#fff"
        self.secondary_color = "lightgray"
        self.contrast_color = "#000"

    def dark(self):
        self.style_name = "dark"
        self.primary_color = "#242424"
        self.secondary_color = "#000"
        self.contrast_color = "#fff"

    def change_style(self):
        self.dark() if self.style_name == "light" else self.light()

    def get_style_name(self):
        return self.style_name

    def get_primary_color(self):
        return self.primary_color

    def get_secondary_color(self):
        return self.secondary_color

    def get_contrast_color(self):
        return self.contrast_color
