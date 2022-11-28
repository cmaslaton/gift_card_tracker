import sqlite3


class Model:
    def __init__(self):
        self._crea_db()

    def _crea_db(self):
        """Si no existe, crea la db"""
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE giftcards (
                id INTEGER PRIMARY KEY,
                nombre_comprador TEXT,
                nombre_destinatario TEXT,
                factura_compra TEXT,
                monto_inicial TEXT,
                monto_disponible TEXT,
                fecha_compra TEXT,
                lugar_compra TEXT,
                fecha_uso TEXT,
                monto_utilizado TEXT,
                factura_uso TEXT,
                lugar_uso TEXT,
                status TEXT,
                tipo TEXT                
                            )""")
            print('DB Creada')
        except sqlite3.Error:
            print('La DB ya está creada')
        finally:
            conn.commit()
            conn.close()

    ######################################################
    ########## TAB ALTA DE GIFT CARDS - MÉTODOS ##########
    ######################################################

    def data_gift_to_db(self, data_dict):
        """Guarda la información de la pestaña de alta de gift cards en la db"""
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"""INSERT INTO giftcards VALUES (
                                    NULL,
                                    '{data_dict['nombre_comprador']}',
                                    '{data_dict['nombre_destinatario']}',
                                    '{data_dict['factura_compra']}',
                                    '{data_dict['monto_inicial']}',
                                    '{data_dict['monto_disponible']}',
                                    '{data_dict['fecha_compra']}',
                                    '{data_dict['lugar_compra']}',
                                    '{data_dict['fecha_uso']}',
                                    '{data_dict['monto_utilizado']}',
                                    '{data_dict['factura_uso']}',
                                    '{data_dict['lugar_uso']}',
                                    '{data_dict['status']}',
                                    '{data_dict['tipo']}'
                                    )
                                """)
            print('Datos Guardados!')
        except sqlite3.Error:
            print('Error en la carga de datos')
        finally:
            conn.commit()
            conn.close()

    ######################################################
    ########## TAB BAJA DE GIFT CARDS - MÉTODOS ##########
    ######################################################

    def get_facturas_sin_usar_from_db(self) -> list:
        """Conecta a la DB y trae las facturas de gift cards no están usadas"""
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM giftcards WHERE status = 'visible'")
            gift_cards_sin_uso = cursor.fetchall()
            gift_cards_sin_uso = [gift_card[3] for gift_card in gift_cards_sin_uso]
            conn.commit()
            conn.close()
            return gift_cards_sin_uso
        except sqlite3.Error:
            print('Error cargando gift cards en sistema')

    def get_gift_data_baja_from_db(self, nro_factura):
        """Trae todos los datos de la factura que se ingresa como argumento"""
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT * FROM giftcards WHERE factura_compra = '{nro_factura}' AND status = 'visible'")
            datos_factura = cursor.fetchall()[0]
            return datos_factura
        except sqlite3.Error:
            print('Error obteniendo los datos ')
        finally:
            conn.commit()
            conn.close()

    def utilizado_igual_disponible(self, nro_factura, monto_utilizado):
        """Compara si el monto inicial es igual al monto disponible"""
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT monto_disponible FROM giftcards WHERE factura_compra = '{nro_factura}' AND status = 'visible'")
            monto_disponible = float(cursor.fetchall()[0][0])
            if monto_disponible == float(monto_utilizado):
                return True
            return False
        except sqlite3.Error:
            print('Error al compara monto_inicial con monto_disponible')
        finally:
            conn.commit()
            conn.close()

    def update_gift_inicial_db(self, nro_factura, monto_disponible=0):
        conn = sqlite3.connect('giftcards.db')
        c = conn.cursor()
        if monto_disponible <= 0:
            c.execute(f"""UPDATE giftcards SET status='oculto', monto_disponible='0' 
                        WHERE factura_compra = '{nro_factura}' AND status='visible'  
                    """)
        else:
            c.execute(f"""UPDATE giftcards SET monto_disponible='{monto_disponible}' 
                        WHERE factura_compra = '{nro_factura}' AND status='visible'
                    """)
        conn.commit()
        conn.close()

    ######################################################
    ################# TREEVIEW - MÉTODOS #################
    ######################################################

    def delete_all_data(self, row):
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"""DELETE FROM giftcards WHERE factura_compra = '{row[2]}'""")
        except sqlite3.Error:
            print('Error borrando los datos ')
        finally:
            conn.commit()
            conn.close()

    def delete_row(self, id):
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"""DELETE FROM giftcards WHERE id = '{id}'""")
        except sqlite3.Error:
            print('Error borrando los datos ')
        finally:
            conn.commit()
            conn.close()

    def get_monto_disponible_fc_alta(self, nro_factura):
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"""SELECT monto_disponible FROM giftcards WHERE factura_compra = '{nro_factura}' 
                AND tipo = 'alta'""")
            monto_disponible = cursor.fetchall()
            return monto_disponible[0][0]
        except sqlite3.Error:
            print('Error borrando los datos ')
        finally:
            conn.commit()
            conn.close()

    def get_all_data_from_db(self):
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM giftcards")
            data = cursor.fetchall()
            return data
        except sqlite3.Error:
            print('Error obteniendo los datos ')
        finally:
            conn.commit()
            conn.close()

    def search_data(self, factura_compra):
        conn = sqlite3.connect('giftcards.db')
        cursor = conn.cursor()
        try:
            cursor = cursor.execute(f"""SELECT * FROM giftcards WHERE factura_compra LIKE '%{factura_compra}%'""")
            giftcards = cursor.fetchall()
            return giftcards
        except:
            pass
        finally:
            conn.commit()
            conn.close()
