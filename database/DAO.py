from database.DB_connect import DBConnect
from model.artist import Artist

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT g.GenreId, g.Name FROM genre g ORDER BY g.Name"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["GenreId"], row["Name"]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNodi(genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT a.ArtistId, a.Name
                   FROM artist a, album al, track t
                   WHERE a.ArtistId = al.ArtistId
                     AND t.AlbumId = al.AlbumId
                     AND t.GenreId = %s"""
        try:
            cursor.execute(query, (genere,))
            for row in cursor:
                result.append(Artist(**row))
        except Exception as e:
            print(f"Errore in getNodi: {e}")
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAcquisti(genere):
        """ritorna righe (ArtistId, CustomerId, Quantita)"""
        """
        [
    {"ArtistId": 4,  "CustomerId": 3,  "Quantita": 1},
    {"ArtistId": 4,  "CustomerId": 14, "Quantita": 2},
    {"ArtistId": 4,  "CustomerId": 22, "Quantita": 2},
    {"ArtistId": 20, "CustomerId": 3,  "Quantita": 1}]
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT al.ArtistId, i.CustomerId, SUM(il.Quantity) AS Quantita
                    FROM invoice i, invoiceline il, track t, album al
                    WHERE i.InvoiceId = il.InvoiceId
                            AND il.TrackId = t.TrackId
                            AND t.AlbumId = al.AlbumId
                            AND t.GenreId = %s
                            GROUP BY al.ArtistId, i.CustomerId"""

        try:
            cursor.execute(query, (genere,))
            for row in cursor:
                result.append(row)
        except Exception as e:
            print(f"Errore in getAcquisti: {e}")
        finally:
            cursor.close()
            cnx.close()
        return result
