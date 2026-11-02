import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_strumenti(self, e):
        # Svuoto la lista per non ripetere le righe a ogni click su Mostra
        self._view.lista_strumenti.controls.clear()

        try:
            strumenti = self._model.get_strumenti()
        except Exception as errore:
            self._view.show_alert(f"Errore durante la lettura degli strumenti: {errore}")
            self._view.update()
            return

        if strumenti is None:
            self._view.show_alert("Connessione non riuscita. Controlla MySQL e la configurazione del database.")
        elif len(strumenti) == 0:
            self._view.lista_strumenti.controls.append(ft.Text("Nessuno strumento presente nel database."))
        else:
            for strumento in strumenti:
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        self._view.update()

    def cerca_strumenti(self, e):
        tipo = self._view.input_tipo_strumento.value.strip()
        self._view.lista_strumenti_ricerca.controls.clear()

        if tipo == "":
            self._view.show_alert("Inserisci il tipo dello strumento da cercare.")
            self._view.update()
            return

        try:
            strumenti = self._model.cerca_strumenti_per_tipo(tipo)
        except Exception as errore:
            self._view.show_alert(f"Errore durante la ricerca degli strumenti: {errore}")
            self._view.update()
            return

        if strumenti is None:
            self._view.show_alert("Connessione non riuscita. Controlla MySQL e la configurazione del database.")
        elif len(strumenti) == 0:
            self._view.lista_strumenti_ricerca.controls.append(ft.Text("Nessuno strumento trovato per questo tipo."))
        else:
            # Aggiungo tutti i risultati, perché più strumenti possono avere lo stesso tipo
            for strumento in strumenti:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        self._view.update()