from tkinter import Scrollbar
from tkinter.ttk import Treeview, Style

from utils.field_names_constants import Fields


class UFSTreeview(Treeview):

    def __init__(self, root):
        super().__init__()

        style = Style()
        # Modify the font of the body
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        # Modify the font of the headings
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        # Remove the borders
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.table = Treeview(root, columns=([Fields[n] for n in range(len(Fields))]), style="mystyle.Treeview")
        self.table.tag_configure('odd', background='#E8E8E8')
        self.table.tag_configure('even', background='#DFDFDF')

        self.table['show'] = 'headings'  # deletes the initial column without data (that is used for indexes/ids)
        self.table['displaycolumns'] = ()
        self.table_vsb = Scrollbar(root, orient="vertical")
        self.table.configure(yscrollcommand=self.table_vsb.set)
        self.table_vsb.configure(command=self.table.yview)
        for n in range(len(Fields)):
            self.table.heading(n, text=Fields[n])
        self.table.grid(column=0, row=1, sticky="NSEW", padx=(0, 20))
