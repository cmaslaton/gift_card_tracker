from datetime import date
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox


class View(tk.Tk):
    BACKGROUND_COLOR = '#432C7A'
    PUNTOS_DE_VENTA = ['0008', '0009', '0010', '0011', '0014']

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.geometry('350x290+400+250')
        self.resizable(False, False)
        self.title('Polla - Gift Card Tracker')
        self._app_interface()

    def main(self):
        self.mainloop()  # 1. Para que ande y ande. Hasta este punto está armado lo básico.

    def _app_interface(self):
        ########## CREACIÓN DE TABS ##########
        # Crea el Tab Control
        self.tab_control = ttk.Notebook(self)
        # Se crean las Tabs
        self.tab_alta_gift = ttk.Frame(self.tab_control)
        self.tab_baja_gift = ttk.Frame(self.tab_control)
        # Se agregan las tabs
        self.tab_control.add(self.tab_alta_gift, text='Alta de Gift Cards')
        self.tab_control.add(self.tab_baja_gift, text='Baja de Gift Cards')
        # Se hacen visibles las tabs
        self.tab_control.pack(expand=1, fill="both")

        ######################################################
        ########## TAB ALTA DE GIFT CARDS - WIDGETS ##########
        ######################################################

        ##### ALTA DE GIFT CARDS - Nombre Comprador #####
        self.label_alta_nombre_comprador = tk.Label(self.tab_alta_gift,
                                                    text='Nombre Comprador:')
        self.label_alta_nombre_comprador.place(x=5, y=5)
        self.var_entry_alta_nombre_comprador = StringVar()
        self.entry_alta_nombre_comprador = ttk.Entry(self.tab_alta_gift,
                                                     textvariable=self.var_entry_alta_nombre_comprador,
                                                     width=34)
        self.entry_alta_nombre_comprador.place(x=130, y=5)

        ##### ALTA DE GIFT CARDS - Nombre Destinatario #####
        self.label_alta_nombre_destinatario = tk.Label(self.tab_alta_gift,
                                                       text='Nombre Destinatario:')
        self.label_alta_nombre_destinatario.place(x=5, y=30)
        self.var_entry_alta_nombre_destinatario = StringVar()
        self.entry_alta_nombre_destinatario = ttk.Entry(self.tab_alta_gift,
                                                        textvariable=self.var_entry_alta_nombre_destinatario,
                                                        width=34)
        self.entry_alta_nombre_destinatario.place(x=130, y=30)

        ##### ALTA DE GIFT CARDS - Factura de Compra #####
        self.label_alta_factura_compra = tk.Label(self.tab_alta_gift,
                                                  text='Factura de Compra:')
        self.label_alta_factura_compra.place(x=5, y=55)

        ### Combo Box - Factura de Compra ###
        self.var_combo_box_alta_ptos_venta = StringVar()
        self.combo_box_alta_ptos_venta = ttk.Combobox(self.tab_alta_gift,
                                                      textvariable=self.var_combo_box_alta_ptos_venta,
                                                      values=self.PUNTOS_DE_VENTA,
                                                      width=4)
        self.combo_box_alta_ptos_venta['state'] = 'readonly'
        self.combo_box_alta_ptos_venta.place(x=130, y=55)
        self.var_combo_box_alta_ptos_venta.trace('w', self.controller.set_local_alta_gc)

        ### Guion + Entry - Factura de Compra ###
        self.label_alta_guion_factura_compra = tk.Label(self.tab_alta_gift,
                                                        text='-')
        self.label_alta_guion_factura_compra.place(x=179, y=55)
        self.var_entry_alta_factura_compra = StringVar()
        self.entry_alta_factura_compra = ttk.Entry(self.tab_alta_gift,
                                                   textvariable=self.var_entry_alta_factura_compra,
                                                   width=24)
        self.entry_alta_factura_compra.place(x=191, y=55)

        ##### ALTA DE GIFT CARDS - Monto de Compra #####
        self.label_alta_monto_compra = tk.Label(self.tab_alta_gift,
                                                text='Monto de la Gift Card:')
        self.label_alta_monto_compra.place(x=5, y=80)
        self.var_entry_alta_monto_compra = StringVar()
        self.entry_alta_monto_compra = ttk.Entry(self.tab_alta_gift,
                                                 textvariable=self.var_entry_alta_monto_compra,
                                                 width=34)
        self.entry_alta_monto_compra.place(x=130, y=80)

        ##### ALTA DE GIFT CARDS - Fecha de Compra #####
        self.label_alta_fecha_compra = tk.Label(self.tab_alta_gift,
                                                text='Fecha de Compra:')
        self.label_alta_fecha_compra.place(x=5, y=105)

        self.var_alta_today = tk.StringVar()
        self.var_alta_today.set(date.today().strftime("%d/%m/%Y"))
        self.entry_alta_fecha_compra = ttk.Entry(self.tab_alta_gift,
                                                 state='disabled',
                                                 textvariable=self.var_alta_today,
                                                 width=34)
        self.entry_alta_fecha_compra.place(x=130, y=105)

        ##### ALTA DE GIFT CARDS - Lugar de Compra #####
        self.label_alta_lugar_compra = tk.Label(self.tab_alta_gift,
                                                text='Lugar de Compra:')
        self.label_alta_lugar_compra.place(x=5, y=130)
        self.var_entry_alta_local = StringVar()
        self.entry_alta_local = ttk.Entry(self.tab_alta_gift,
                                          state='disabled',
                                          textvariable=self.var_entry_alta_local,
                                          width=34, )
        self.entry_alta_local.place(x=130, y=130)

        ##### ALTA DE GIFT CARDS - Botón de Guardado #####
        self.button_alta_compra = tk.Button(self.tab_alta_gift,
                                            command=self.controller.save_data_alta_db,
                                            height=2,
                                            text='Alta de Gift Card',
                                            width=47)
        self.button_alta_compra.place(x=5, y=157)

        ##### ALTA DE GIFT CARDS - Botón de Consultas #####
        self.button_alta_consultas = tk.Button(self.tab_alta_gift,
                                               command=self.controller.create_tree_view,
                                               height=3,
                                               text='Consultas',
                                               width=47)
        self.button_alta_consultas.place(x=5, y=205)

        ######################################################
        ########## TAB BAJA DE GIFT CARDS - WIDGETS ##########
        ######################################################

        ##### BAJA DE GIFT CARDS - Nombre Comprador #####
        self.label_baja_nombre_comprador = tk.Label(self.tab_baja_gift,
                                                    text='Nombre Comprador:')
        self.label_baja_nombre_comprador.place(x=5, y=5)
        self.var_entry_baja_nombre_comprador_ = StringVar()
        self.entry_baja_nombre_comprador_ = ttk.Entry(self.tab_baja_gift,
                                                      state='disabled',
                                                      textvariable=self.var_entry_baja_nombre_comprador_,
                                                      width=34)
        self.entry_baja_nombre_comprador_.place(x=130, y=5)

        ##### BAJA DE GIFT CARDS - Nombre Destinatario #####
        self.label_baja_nombre_destinatario = tk.Label(self.tab_baja_gift,
                                                       text='Nombre Destinatario:')
        self.label_baja_nombre_destinatario.place(x=5, y=30)
        self.var_entry_baja_nombre_destinatario_ = StringVar()
        self.entry_baja_nombre_destinatario_ = ttk.Entry(self.tab_baja_gift,
                                                         state='disabled',
                                                         textvariable=self.var_entry_baja_nombre_destinatario_,
                                                         width=34)
        self.entry_baja_nombre_destinatario_.place(x=130, y=30)

        ##### BAJA DE GIFT CARDS - Factura de Compra #####
        self.label_baja_factura_compra = tk.Label(self.tab_baja_gift,
                                                  text='Factura de Compra:')
        self.label_baja_factura_compra.place(x=5, y=55)

        ### Combo Box - Factura de Compra ###
        self.var_combo_box_baja_factura_compra = StringVar()
        self.combo_box_baja_factura_compra = ttk.Combobox(self.tab_baja_gift,
                                                          textvariable=self.var_combo_box_baja_factura_compra,
                                                          postcommand=self.controller.facturas_sin_usar_baja_gc,
                                                          width=31)
        self.combo_box_baja_factura_compra['state'] = 'readonly'
        self.combo_box_baja_factura_compra.place(x=130, y=55)
        self.var_combo_box_baja_factura_compra.trace('w', self.controller.set_data_baja_gc)

        ##### BAJA DE GIFT CARDS - Monto de Compra #####
        self.label_baja_monto_compra = tk.Label(self.tab_baja_gift,
                                                text='Monto Disponible:')
        self.label_baja_monto_compra.place(x=5, y=80)
        self.var_entry_baja_monto_disponible_ = StringVar()
        self.entry_baja_monto_compra_ = ttk.Entry(self.tab_baja_gift,
                                                  state='disabled',
                                                  textvariable=self.var_entry_baja_monto_disponible_,
                                                  width=34)
        self.entry_baja_monto_compra_.place(x=130, y=80)

        ##### BAJA DE GIFT CARDS - Fecha de Uso #####
        self.label_baja_fecha_uso = tk.Label(self.tab_baja_gift,
                                             text='Fecha de Uso:')
        self.label_baja_fecha_uso.place(x=5, y=105)
        self.var_entry_baja_fecha_uso_today = StringVar()
        self.entry_baja_fecha_compra_today = ttk.Entry(self.tab_baja_gift,
                                                       state='disabled',
                                                       textvariable=self.var_entry_baja_fecha_uso_today,
                                                       width=34)
        self.entry_baja_fecha_compra_today.place(x=130, y=105)

        ##### BAJA DE GIFT CARDS - Monto Utilizado #####
        self.label_baja_monto_utilizado = tk.Label(self.tab_baja_gift,
                                                   text='Monto Utilizado:')
        self.label_baja_monto_utilizado.place(x=5, y=130)
        self.var_entry_baja_monto_utilizado = StringVar()
        self.entry_baja_monto_utilizado = ttk.Entry(self.tab_baja_gift,
                                                    textvariable=self.var_entry_baja_monto_utilizado,
                                                    width=34)
        self.entry_baja_monto_utilizado.place(x=130, y=130)

        ##### BAJA DE GIFT CARDS - Factura de Uso #####
        self.label_baja_factura_uso = tk.Label(self.tab_baja_gift,
                                               text='Factura de Uso:')
        self.label_baja_factura_uso.place(x=5, y=155)

        ### Combo Box - Factura de Uso ###
        self.var_combo_baja_pto_venta = StringVar()
        self.combo_box_baja_ptos_venta = ttk.Combobox(self.tab_baja_gift,
                                                      values=self.PUNTOS_DE_VENTA,
                                                      textvariable=self.var_combo_baja_pto_venta,
                                                      width=4)
        self.combo_box_baja_ptos_venta['state'] = 'readonly'
        self.combo_box_baja_ptos_venta.place(x=130, y=155)
        self.var_combo_baja_pto_venta.trace('w', self.controller.set_local_baja_gc)

        ### Guion + Entry - Factura de Uso ###
        self.label_baja_guion_factura_uso = tk.Label(self.tab_baja_gift,
                                                     text='-')
        self.label_baja_guion_factura_uso.place(x=179, y=155)
        self.var_entry_baja_factura_uso = StringVar()
        self.entry_baja_factura_uso = ttk.Entry(self.tab_baja_gift,
                                                textvariable=self.var_entry_baja_factura_uso,
                                                width=24)
        self.entry_baja_factura_uso.place(x=191, y=155)

        ##### BAJA DE GIFT CARDS - Lugar de Uso #####
        self.label_baja_lugar_compra = tk.Label(self.tab_baja_gift,
                                                text='Lugar de Uso:')
        self.label_baja_lugar_compra.place(x=5, y=180)
        self.var_entry_baja_local_uso = StringVar()
        self.entry_baja_local = ttk.Entry(self.tab_baja_gift,
                                          state='disabled',
                                          textvariable=self.var_entry_baja_local_uso,
                                          width=34, )
        self.entry_baja_local.place(x=130, y=180)

        ##### BAJA DE GIFT CARDS - Botón de Guardado #####
        self.button_baja_utilizar_gift_card = tk.Button(self.tab_baja_gift,
                                                        command=self.controller.save_data_baja_db,
                                                        height=3,
                                                        text='Utilizar Gift Card',
                                                        width=47)
        self.button_baja_utilizar_gift_card.place(x=5, y=205)


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Ingresar Clave Maestra')
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        self.geometry('305x73+650+350')
        self.password = False
        self.password_admin = False

        self.clave_label = tk.Label(self,
                                    text='Clave:')
        self.clave_label.place(x=10, y=10)

        self.var_clave_entry = StringVar()
        self.clave_entry = ttk.Entry(self,
                                     show='*',
                                     textvariable=self.var_clave_entry,
                                     width=35)
        self.clave_entry.place(x=75, y=10)

        self.modify_button = tk.Button(self,
                                       command=self.clave_maestra,
                                       text='Ingresar',
                                       width=39)
        self.modify_button.place(x=10, y=40)

    def clave_maestra(self):
        claves = {'usuarios_terrenales': 'maestra', 'usuarios_dioses': 'admines'}
        if self.var_clave_entry.get().lower() == claves['usuarios_terrenales']:
            self.password = True
            self.destroy()
        elif self.var_clave_entry.get().lower() == claves['usuarios_dioses']:
            self.password_admin = True
            self.destroy()
        elif not self.var_clave_entry.get() or (self.var_clave_entry.get().lower() not in claves.values()):
            tkinter.messagebox.showerror(title='Error!', message='Meté una contraseña válida k-po')
