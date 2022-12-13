class StyleManager:
    def __init__(self, style_name="default"):
        self.style_name = style_name

        if style_name == "dark":
            self.dark()
        else:
            # Init with default style
            self.primary_color = "#fff"
            self.secondary_color = "lightgray"
            self.contrast_color = "#000"

    def default(self):
        self.primary_color = "#fff"
        self.secondary_color = "lightgray"
        self.contrast_color = "#000"

    def dark(self):
        self.primary_color = "#242424"
        self.secondary_color = "#000"
        self.contrast_color = "#fff"

    def get_primary_color(self):
        return self.primary_color

    def get_secondary_color(self):
        return self.secondary_color

    def get_contrast_color(self):
        return self.contrast_color
