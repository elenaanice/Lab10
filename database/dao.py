from database.DB_connect import DBConnect
from model.filiale import Filiale

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """

    @staticmethod
    def get_all_filiali():
        #Restituisce tutte le filiali presenti nel database
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database (get_all_filiali).")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM filiale """

        try:
            cursor.execute(query)
            for row in cursor:
                filiale = Filiale(
                    id = row['id'],
                    codice=row['codice'],
                    nome = row['nome'],
                    citta=row['citta'],
                    provincia=row['provincia'],
                    latitudine=float(row['latitudine']),
                    longitudine=float(row['longitudine'])
                )
                result.append(filiale)
        except Exception as e:
            print(f"Errore durante la query get_all_filiali: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_collegamenti_filtrati(threshold: float):
        #restituisce le coppie di filiali (id_f1, id_f2, importo_medio) con importo medio >= threshold,
        #aggregando i bonifici in entrambe le direzioni.
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database (get_collegamenti_filtrati).")
            return None

        cursor = cnx. cursor(dictionary=True)
        query = """ 
                SELECT LEAST(id_filiale_origine, id_filiale_destinazione) AS f1,
                        GREATEST(id_filiale_origine, id_filiale_destinazione) AS f2,
                        AVG(importo) AS peso
                FROM bonifico
                GROUP BY LEAST(id_filiale_origine, id_filiale_destinazione),
                        GREATEST(id_filiale_origine, id_filiale_destinazione)
                HAVING AVG(importo) >= %s
                """
        try:
            cursor.execute(query, (threshold,))
            for row in cursor:
                result.append((row["f1"], row["f2"], float(row["peso"])))
        except Exception as e:
            print(f'Errore durante la query get_collegamenti_filtrati: {e}')
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result




