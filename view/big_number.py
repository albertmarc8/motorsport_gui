from tkinter import Label

class BigNumber(Label):
	def __init__(self, root):
		self.root = root
		self.counter = 0

		super().__init__(root, text="214", pady=5, font=("Arial", 300), background=self.root.style.get_primary_color(), foreground="orange")
		self.grid(column=0, row=0, columnspan=2, sticky="NSEW", pady=(0, 50))

	def set_style(self):
		self.config(background=self.root.style.get_primary_color())

	def plot(self, x, y, title):
		self.config(text = "--")

	def plot_live_data(self):
		line = self.root.controller.import_live_data() # Devuelve 1 linea con cols
		print(line)



		# rpm -> 10 ; tps -> 13
		self.config(text = int(line[13]) + self.counter)

		self.counter += 1
		self.root.after(10, self.plot_live_data)