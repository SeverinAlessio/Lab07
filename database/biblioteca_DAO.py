from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_biblioteche(self):
        conn = DBConnect.get_connection()
        if conn is None:
            raise ConnectionError("Impossibile collegarsi al database.")

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nome, indirizzo "
                "FROM biblioteca "
                "ORDER BY nome"
            )
            righe = cursor.fetchall()

            return [
                Biblioteca(
                    id=riga["id"],
                    nome=riga["nome"],
                    indirizzo=riga["indirizzo"],
                )
                for riga in righe
            ]
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
