from tkinter import Scrollbar
from tkinter.ttk import Treeview, Style

from utils.field_names_constants import Fields


class UFSTreeview(Treeview):

    def __init__(self, root):
        style = Style()
        # Modify the font of the body
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        # Modify the font of the headings
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        # Remove the borders
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        super().__init__(root, columns=([Fields[n] for n in range(len(Fields))]), style="mystyle.Treeview")

        self.tag_configure('odd', background='#E8E8E8')
        self.tag_configure('even', background='#DFDFDF')

        self['show'] = 'headings'  # deletes the initial column without data (that is used for indexes/ids)
        self['displaycolumns'] = ()
        self.table_vsb = Scrollbar(root, orient="vertical")
        self.configure(yscrollcommand=self.table_vsb.set)
        self.table_vsb.configure(command=self.yview)
        for n in range(len(Fields)):
            self.heading(n, text=Fields[n])
        self.grid(column=0, row=1, sticky="NSEW", padx=(0, 20))