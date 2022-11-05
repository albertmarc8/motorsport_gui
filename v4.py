import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.backends.backend_tkagg as tkagg


class V3:
	def __init__(self, root):
		self.root = root
		self.root.title("UJI Formula Student")
		self.root.geometry('1920x1080')

		control_container = LabelFrame(self.root, text="controls", padx=60, pady=30)
		
		# Import Button
		import_btn = Button(control_container, text="Import data from .txt", command = self.import_from_txt)
		import_btn.pack()


		# Plot Button
		plot_btn = Button(control_container, text="Plot data", command = self.plot_data)
		plot_btn.pack()
		

		
		# Export Button
		plot_btn = Button(control_container, text="Export data to .csv", command = self.export_to_csv)
		plot_btn.pack()
		
		control_container.place(x = 1320, y=720, width=560, height=330)
		

		chart_label_frame = LabelFrame(self.root, text="chart")#, padx=750, pady=300)
		chart_label = Label(chart_label_frame, text="TELEMETRY CHART", font=("Arial", 25)).place(relx=.5, rely=.5, anchor=CENTER)
		chart_label_frame.place(x=40, y=30, width=1840, height=660)

		table_label_frame = LabelFrame(self.root, text="table")
		table_label = Label(table_label_frame, text="TELEMETRY TABLE", font=("Arial", 25)).place(relx=.5, rely=.5, anchor=CENTER)
		table_label_frame.place(x=40, y=720, width=1200, height=330)

		self.toolbar = None
		self.plot_on_start()

	def plot_on_start(self):
		self.filename="coche_reduced.txt"
		# 1. Read the file:
		with open(self.filename, "r") as f:

			# 2. Iterate and get values from all lines
			self.data = [(int(seconds), int(rpms)) for seconds, rpms in [line[7:-8].split(", ") for line in f.readlines()]]
		self.plot_data()
		

	def import_from_txt(self):
		"""
		Asks the user to select a txt file in which each line follows
		the regex [0x001 seconds, rpms 0x001]
		stores a resulting matix with shape (n, 2) being n the number
		of non-empty lines in the file
		"""

		self.filename = filedialog.askopenfilename(filetypes=(('text files', '*.txt'),))


		# 1. Read the file:
		with open(self.filename, "r") as f:

			# 2. Iterate and get values from all lines
			self.data = [(int(seconds), int(rpms)) for seconds, rpms in [line[7:-8].split(", ") for line in f.readlines()]]


	def export_to_csv(self):
		"""
		Saves 'self.data' into a file in the same folder as the txt
		but with a csv filetype.
		WARNING: It will remove the file with csv if it already exists
		"""

		# 0. Check if a datafile has been loaded
		if self.filename is None:
			return None # Todo: mensaje de error

		# 1. Get the right path
		filename = self.filename.rstrip("txt")
		filename += "csv"

		# 2. Open the file
		with open(filename, "w") as f:
			# 3. Strore data as csv
			[f.write(line) for line in [",".join([str(d[0]),str(d[1])])+"\n" for d in self.data]]

	def plot_data(self):
		if self.data is None:
			return None

		seconds = [secs for secs,rpms in self.data]
		rpms = [rpms for secs,rpms in self.data]



		# Represent the table
		table = Treeview(self.root)
		table["columns"] = ("Second", "RPMs")

		table.heading("#0", text="", anchor=W)
		table.heading("Second", text="Second", anchor=W)
		table.heading("RPMs", text="RPMs", anchor=W)

		[table.insert(parent="", index="end", iid=i, text="", values=d) for i,d in enumerate(self.data)]

		table.place(x = 0, y = 720, height=380, width=1280)
		self.root.update()
		#table.grid(row=3, column=0, rowspan=2, columnspan=2, sticky="we")

		# Represent the plot
		"""fig = plt.figure(figsize=(5,4), dpi=100)
		fig.add_subplot(111).plot(seconds, rpms)
		fig.add_subplot(121).plot(seconds, rpms)
		fig.add_subplot(131).plot(seconds, rpms)"""
		fig, axs = plt.subplots(2, 2, figsize=(5,4))
		for ax in axs.flat:
			ax.set_title("Data plot")
			ax.plot(seconds, rpms)

		frame = Frame(root)
		frame.place(x=0, y=0, width=1920, height=720)

		canvas = FigureCanvasTkAgg(fig, master=frame)
		canvas.get_tk_widget().pack(side='top', fill='both')
		canvas._tkcanvas.pack(side='top', fill='both', expand=1)
		#canvas.get_tk_widget().place(x=0, y=0)
		#canvas._tkcanvas.place(x=0, y=0)
		
		if self.toolbar is None:
			self.toolbar = NavigationToolbar2Tk(canvas, frame)
			self.toolbar.update()
			self.toolbar.pack()
		"""
		figure = plt.figure(figsize=(20,7), dpi=100)
		figure.add_subplot(111).plot(seconds, rpms)
		chart = FigureCanvasTkAgg(figure, self.root)
		#chart.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=3, sticky="we")
		chart.get_tk_widget().place(x=0, y=0)
		"""

		



root = Tk()
root.attributes('-fullscreen', True)
program = V3(root)
program.root.mainloop()
