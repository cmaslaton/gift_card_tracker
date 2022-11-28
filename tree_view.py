import tkinter as tk
from tkinter import ttk
from tkinter import StringVar


class TreeView(tk.Toplevel):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Consultas')
        self.resizable(False, False)
        self.geometry('615x290+760+250')
        self._app_interface()
        if controller.admin:
            self.delete()

    def _app_interface(self):
        self.columns = (
            'id', 'fecha_compra', 'factura_compra', 'monto_compra', 'fecha_uso', 'factura_uso', 'monto_utilizado')
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        self.tree.column('# 1', anchor=tk.CENTER, stretch=tk.NO, width=33)
        self.tree.heading('# 1', text="id")
        self.tree.column('# 2', anchor=tk.CENTER, stretch=tk.NO, width=94)
        self.tree.heading('# 2', text="fecha_compra")
        self.tree.column('# 3', anchor=tk.CENTER, stretch=tk.NO, width=94)
        self.tree.heading('# 3', text="factura_compra")
        self.tree.column('# 4', anchor=tk.CENTER, stretch=tk.NO, width=94)
        self.tree.heading('# 4', text="monto_compra")
        self.tree.column('# 5', anchor=tk.CENTER, stretch=tk.NO, width=94)
        self.tree.heading('# 5', text="fecha_uso")
        self.tree.column('# 6', anchor=tk.CENTER, stretch=tk.NO, width=94)
        self.tree.heading('# 6', text="factura_uso")
        self.tree.column('# 7', anchor=tk.CENTER, stretch=tk.NO, width=97)
        self.tree.heading('# 7', text="monto_utilizado")
        self.tree.place(relx=0.01, rely=0.02, width=603, height=245)

        self.var_search_entry = StringVar()
        self.search_entry = ttk.Entry(self,
                                      textvariable=self.var_search_entry,
                                      width=25)
        self.search_entry.place(x=5, y=258, height=25)

        self.search_button = tk.Button(self,
                                       command=self.controller.search_data,
                                       text='Buscar',
                                       width=20)
        self.search_button.place(x=165, y=258)

        self.refresh_button = tk.Button(self,
                                        command=self.controller.clear_and_show_treeview,
                                        text='Reiniciar',
                                        width=19)
        self.refresh_button.place(x=318, y=258)

    def delete(self):
        self.delete_button = tk.Button(self,
                                       command=self.controller.delete_data,
                                       text='Eliminar',
                                       width=19)

        self.delete_button.place(x=465, y=258)

        self.tree.bind('<ButtonRelease-1>', self.controller.selected_row)  # Para que funcione el select
