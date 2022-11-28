from datetime import date
import math
from model import Model
import re
import tkinter as tk
import tkinter.messagebox
from tree_view import TreeView
from view import View, LoginWindow


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.treeview = None
        self.admin = None

    def main(self):  # 1. Se declara una función main acá y en el view
        self.view.main()

    def is_number(self, sample_str):
        """Devuelve True si una string contiene un lint o un float"""
        result = True
        try:
            float(sample_str)
        except:
            result = False
        return result

    ######################################################
    ########## TAB ALTA DE GIFT CARDS - MÉTODOS ##########
    ######################################################

    # Buscar el get del alta y ver si ese número de factura está cargado.
    def check_repetidos(self):
        factura_compra = self.get_data_alta_gc()['factura_compra']
        for datos_giftcards in self.model.get_all_data_from_db():
            if factura_compra in datos_giftcards:
                return True

    def clear_data_alta_gc(self):
        """Limpia el formulario de alta de gift cards"""
        self.view.var_entry_alta_nombre_comprador.set('')
        self.view.var_entry_alta_nombre_destinatario.set('')
        self.view.var_combo_box_alta_ptos_venta.set('')
        self.view.var_entry_alta_factura_compra.set('')
        self.view.var_entry_alta_monto_compra.set('')
        self.view.var_entry_alta_local.set('')

    def get_data_alta_gc(self) -> dict:
        """Capta todos los datos del formulario de alta de gift cards. Agrega datos adicionales para la tabla SQL"""
        data_alta_gc = {
            # Datos formulario de alta
            'nombre_comprador': self.view.var_entry_alta_nombre_comprador.get().lower(),
            'nombre_destinatario': self.view.var_entry_alta_nombre_destinatario.get().lower(),
            'factura_compra': f'{self.view.var_combo_box_alta_ptos_venta.get()}-{self.view.var_entry_alta_factura_compra.get()}',
            'monto_inicial': self.view.var_entry_alta_monto_compra.get(),
            'monto_disponible': self.view.var_entry_alta_monto_compra.get(),
            'fecha_compra': self.view.var_alta_today.get(),
            'lugar_compra': self.view.var_entry_alta_local.get().lower(),
            # Datos para formulario de baja
            'fecha_uso': '-',
            'monto_utilizado': '-',
            'factura_uso': '-',
            'lugar_uso': '-',
            # Estado
            'status': 'visible',
            'tipo': 'alta'
        }
        return data_alta_gc

    def save_data_alta_db(self):
        """Guarda en la base de datos la información capturada por la función get_data_alta_gc que toma los
        datos del formulario Alta de Gift Cards"""
        if not self.view.var_entry_alta_nombre_comprador.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not bool(re.match('[a-zA-Z\s]+$', self.view.var_entry_alta_nombre_comprador.get())):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Nombre Comprador" contiene caracteres prohibidos.')
        elif not self.view.var_entry_alta_nombre_destinatario.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not bool(re.match('[a-zA-Z\s]+$', self.view.var_entry_alta_nombre_destinatario.get())):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Nombre Destinatario" contiene caracteres prohibidos.')
        elif not self.view.var_combo_box_alta_ptos_venta.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar.')
        elif not self.view.var_entry_alta_factura_compra.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar.')
        elif not self.is_number(self.view.var_entry_alta_factura_compra.get()):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Factura de Compra" contiene caracteres prohibidos.')
        elif len(self.view.var_entry_alta_factura_compra.get()) != 8:
            tkinter.messagebox.showerror(title='Error!', message='El número de la factura debe tener 8 caracteres.')
        elif not self.view.var_entry_alta_monto_compra.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not self.is_number(self.view.var_entry_alta_monto_compra.get()):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Monto de la Gift Card" contiene caracteres prohibidos.')
        elif self.check_repetidos():
            tkinter.messagebox.showerror(title='Error!',
                                         message='Esa factura ya está cargada en sistema.')
        else:
            msg_box = tkinter.messagebox.askquestion('Alta de Gift Cards', 'Confirmás la carga de datos?',
                                                     icon='warning')
            self.check_repetidos()
            if msg_box == 'yes':
                self.model.data_gift_to_db(self.get_data_alta_gc())
                self.clear_data_alta_gc()
                if self.treeview:
                    self.clear_and_show_treeview()

    def set_local_alta_gc(self, *args):
        """Establece el local de compra de la gift card según el punto de venta elegido"""
        ptos_vta_il_cheff = ['0008', '0009', '0014']
        if self.view.var_combo_box_alta_ptos_venta.get() in ptos_vta_il_cheff:
            return self.view.var_entry_alta_local.set('IL CHEFF')
        return self.view.var_entry_alta_local.set('COSAS DE CASA')

    ######################################################
    ########## TAB BAJA DE GIFT CARDS - MÉTODOS ##########
    ######################################################

    def clear_data_baja_gc(self):
        """Limpia el formulario de alta de gift cards"""
        self.view.var_entry_baja_nombre_comprador_.set('')
        self.view.var_entry_baja_nombre_destinatario_.set('')
        self.view.var_entry_baja_monto_disponible_.set('')
        self.view.var_combo_box_baja_factura_compra.set('')  # TODO ver esta mierda
        self.view.var_entry_baja_fecha_uso_today.set('')
        self.view.var_entry_baja_monto_utilizado.set('')
        self.view.var_combo_baja_pto_venta.set('')
        self.view.var_entry_baja_factura_uso.set('')
        self.view.var_entry_baja_local_uso.set('')

    def facturas_sin_usar_baja_gc(self):
        """Muestra en el combo box de la pestaña baja de gift cards las facturas de las gift cards sin utilizar"""
        self.view.combo_box_baja_factura_compra.config(values=self.model.get_facturas_sin_usar_from_db())

    def set_data_baja_gc(self, *args):
        """Trae de la DB los datos de la factura sin usar"""
        factura_compra = self.view.var_combo_box_baja_factura_compra.get()
        try:
            data = self.model.get_gift_data_baja_from_db(factura_compra)
            self.view.var_entry_baja_nombre_comprador_.set(data[1].title())
            self.view.var_entry_baja_nombre_destinatario_.set(data[2].title())
            self.view.var_entry_baja_monto_disponible_.set(f'${data[5]}')
            self.view.var_entry_baja_fecha_uso_today.set(date.today().strftime("%d/%m/%Y"))
        except Exception:
            print('No sé qué mierda hacer con esto')

    def set_local_baja_gc(self, *args):
        """Establece el local de compra de la gift card según el punto de venta elegido"""
        ptos_vta_il_cheff = ['0008', '0009', '0014']
        if self.view.var_combo_baja_pto_venta.get() in ptos_vta_il_cheff:
            return self.view.var_entry_baja_local_uso.set('IL CHEFF')
        return self.view.var_entry_baja_local_uso.set('COSAS DE CASA')

    def get_data_baja_gc(self) -> dict:
        """Capta todos los datos del formulario de baja de gift cards. Agrega datos adicionales para la tabla SQL.
        Update de gift card inicial"""
        data_baja_gc = {
            # Datos formulario de alta
            'nombre_comprador': self.view.var_entry_baja_nombre_comprador_.get().lower(),
            'nombre_destinatario': self.view.var_entry_baja_nombre_destinatario_.get().lower(),
            'factura_compra': self.view.var_combo_box_baja_factura_compra.get(),
            'monto_inicial': '-',
            'monto_disponible': float(self.view.var_entry_baja_monto_disponible_.get()[1:]) - float(
                self.view.var_entry_baja_monto_utilizado.get()),
            'fecha_compra': '-',
            'lugar_compra': '-',
            # Datos para formulario de baja
            'fecha_uso': self.view.var_entry_baja_fecha_uso_today.get(),
            'monto_utilizado': self.view.var_entry_baja_monto_utilizado.get(),
            'factura_uso': f'{self.view.var_combo_baja_pto_venta.get()}-{self.view.var_entry_baja_factura_uso.get()}',
            'lugar_uso': self.view.var_entry_baja_local_uso.get().lower(),
            # Estado
            'status': 'oculto',
            'tipo': 'baja'
        }
        # Update de Gift Card Inicial
        if self.model.utilizado_igual_disponible(nro_factura=self.view.var_combo_box_baja_factura_compra.get(),
                                                 monto_utilizado=self.view.var_entry_baja_monto_utilizado.get()):
            self.model.update_gift_inicial_db(nro_factura=self.view.var_combo_box_baja_factura_compra.get())
        else:
            resultado = float(self.view.var_entry_baja_monto_disponible_.get()[1:]) - float(
                self.view.var_entry_baja_monto_utilizado.get())
            self.model.update_gift_inicial_db(nro_factura=self.view.var_combo_box_baja_factura_compra.get(),
                                              monto_disponible=math.ceil(resultado))
        return data_baja_gc

    def save_data_baja_db(self):
        """Guarda en la base de datos la información capturada por la función get_data_alta_gc que toma los
        datos del formulario Alta de Gift Cards"""
        if not self.view.var_entry_baja_nombre_comprador_.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not self.view.var_entry_baja_monto_utilizado.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not self.is_number(self.view.var_entry_baja_monto_utilizado.get()):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Monto Utilizado" contiene caracteres prohibidos.')
        elif not self.view.var_combo_baja_pto_venta.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not self.view.var_entry_baja_factura_uso.get():
            tkinter.messagebox.showerror(title='Error!', message='Hay campos sin completar')
        elif not self.is_number(self.view.var_entry_baja_factura_uso.get()):
            tkinter.messagebox.showerror(title='Error!',
                                         message='El campo "Factura de Uso" contiene caracteres prohibidos.')
        elif len(self.view.var_entry_baja_factura_uso.get()) != 8:
            tkinter.messagebox.showerror(title='Error!', message='El número de la factura debe tener 8 caracteres.')
        else:
            msg_box = tkinter.messagebox.askquestion('Alta de Gift Cards', 'Confirmás la carga de datos?',
                                                     icon='warning')
            if msg_box == 'yes':
                self.model.data_gift_to_db(self.get_data_baja_gc())
                self.clear_data_baja_gc()
                if self.treeview:
                    self.clear_and_show_treeview()

    ######################################################
    ################# TREEVIEW - MÉTODOS #################
    ######################################################

    def create_tree_view(self):
        """crea el treeview"""
        if self.treeview is None:
            self.treeview = TreeView(self)
            self.treeview.protocol('WM_DELETE_WINDOW', self.close_treeview)
            self.show_data()

    def clear_treeview(self):
        """limpia la vista del treeview"""
        self.treeview.tree.delete(*self.treeview.tree.get_children())

    def clear_and_show_treeview(self):
        self.clear_treeview()
        self.show_data()

    def close_treeview(self):
        """cierra el tree view"""
        self.treeview.destroy()
        self.treeview = None

    def search_data(self):
        """hace la búsqueda de la información en la db y la trae al treeview"""
        search_entry = self.treeview.var_search_entry.get()
        self.clear_treeview()
        rows = self.model.search_data(factura_compra=search_entry)
        for row in rows:
            id = row[0]
            fecha_compra = row[6]
            factura_compra = row[3]
            monto_compra = row[4]
            if self.is_number(monto_compra):
                monto_compra = f'${math.ceil(float(monto_compra))}'
            fecha_uso = row[8]
            factura_uso = row[10]
            monto_utilizado = row[9]
            if self.is_number(monto_utilizado):
                monto_utilizado = f'${math.ceil(float(monto_utilizado))}'
            row = [id, fecha_compra, factura_compra, monto_compra, fecha_uso, factura_uso, monto_utilizado]
            self.treeview.tree.insert('', tk.END, values=row)

    def selected_row(self, *args) -> list:
        """devuelve la fila seleccionada"""
        if self.treeview is not None:
            current_item = self.treeview.tree.focus()
            row = self.treeview.tree.item(current_item)['values']
            return row

    def show_data(self):
        """muestra los datos de la db en el view del treeview"""
        data_db = self.model.get_all_data_from_db()
        for data in data_db:
            id = data[0]
            fecha_compra = data[6]
            factura_compra = data[3]
            monto_compra = data[4]
            if self.is_number(monto_compra):
                monto_compra = f'${math.ceil(float(monto_compra))}'
            fecha_uso = data[8]
            factura_uso = data[10]
            monto_utilizado = data[9]
            if self.is_number(monto_utilizado):
                monto_utilizado = f'${math.ceil(float(monto_utilizado))}'
            data = [id, fecha_compra, factura_compra, monto_compra, fecha_uso, factura_uso, monto_utilizado]
            self.treeview.tree.insert('', tk.END, values=data)

    def delete_data(self):
        """borra la información seleccionada y hace refresh del treeview"""
        if self.selected_row():
            msg_box = tk.messagebox.askquestion('Eliminar Datos',
                                                'Confirmás la eliminación de los datos seleccionados?',
                                                icon='warning')
            if msg_box == 'yes':
                # Si la fila "tipo" es "alta" -> borrar todas las demás apariciones del número de factura
                if self.selected_row()[-1] == '-':
                    self.model.delete_all_data(self.selected_row())
                    self.clear_and_show_treeview()
                # Si se borra una baja, se suma el "monto_utilizado" al "monto_disponible" de la alta
                elif self.selected_row()[-1] != '-':
                    # Monto disponible giftcard seleccionada
                    monto_disponible_giftcard_seleccionada = math.ceil(float(self.selected_row()[-1][1:]))
                    factura_alta = self.selected_row()[2]
                    monto_disponible_giftcard_alta = self.model.get_monto_disponible_fc_alta(nro_factura=factura_alta)
                    monto_disponible_alta_inicial = int(monto_disponible_giftcard_seleccionada) + int(
                        monto_disponible_giftcard_alta)
                    self.model.update_gift_inicial_db(nro_factura=factura_alta,
                                                      monto_disponible=monto_disponible_alta_inicial)
                    self.model.delete_row(id=self.selected_row()[0])
                    self.clear_and_show_treeview()
                else:
                    print('Que hacés Marianito')


if __name__ == '__main__':
    login = LoginWindow()
    login.mainloop()
    if login.password:
        controller = Controller()
        controller.main()
    elif login.password_admin:
        controller = Controller()
        controller.admin = True
        controller.main()
