from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        connessione = get_connection()
        if connessione is None:
            return None

        cursore = None
        try:
            cursore = connessione.cursor()
            cursore.execute("SELECT * FROM strumento ORDER BY marca, codice")

            strumenti = []
            for riga in cursore.fetchall():
                strumento = Strumento(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5])
                strumenti.append(strumento)

            return strumenti
        finally:
            # Chiudo la connessione anche se la lettura dei dati non va a buon fine
            if cursore is not None:
                cursore.close()
            connessione.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        connessione = get_connection()
        if connessione is None:
            return None

        cursore = None
        try:
            cursore = connessione.cursor()
            # Passo il tipo separatamente dalla query, senza unirlo al testo SQL
            query = "SELECT * FROM strumento WHERE tipo = %s ORDER BY marca, codice"
            cursore.execute(query, (tipo,))

            strumenti = []
            for riga in cursore.fetchall():
                strumento = Strumento(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5])
                strumenti.append(strumento)

            return strumenti
        finally:
            if cursore is not None:
                cursore.close()
            connessione.close()