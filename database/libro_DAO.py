from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_generi(self):
        conn = DBConnect.get_connection()
        if conn is None:
            raise ConnectionError("Impossibile collegarsi al database.")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT genere "
                "FROM libro "
                "WHERE genere IS NOT NULL "
                "ORDER BY genere"
            )
            return [riga[0] for riga in cursor.fetchall()]
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def get_libri_filtrati(self, biblioteca_id=None, genere=None):
        conn = DBConnect.get_connection()
        if conn is None:
            raise ConnectionError("Impossibile collegarsi al database.")

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id, titolo, autore, genere,
                       anno_pubblicazione, id_biblioteca
                FROM libro
                WHERE (%s IS NULL OR id_biblioteca = %s)
                  AND (%s IS NULL OR genere = %s)
                ORDER BY titolo, autore
            """
            cursor.execute(
                query,
                (biblioteca_id, biblioteca_id, genere, genere),
            )
            righe = cursor.fetchall()

            return [
                Libro(
                    id=riga["id"],
                    titolo=riga["titolo"],
                    autore=riga["autore"],
                    genere=riga["genere"],
                    anno_pubblicazione=riga["anno_pubblicazione"],
                    id_biblioteca=riga["id_biblioteca"],
                )
                for riga in righe
            ]
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
