import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_collegamenti(self, e):
        """
        Funzione che controlla prima se il valore dell'importo inserito sia valido (es. non deve essere una stringa) e
        poi popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Filiali presenti
        * Numero di Collegamenti
        * Lista di Collegamenti che superano l'importo indicato come soglia
        """
        valore_str = self._view.importo_medio_minimo.value

        #1. Validazione dell'input
        if not valore_str or valore_str.strip() == "":
            self._view.show_alert("Inserire un valore numerico per la soglia.")
            return
        try:
            soglia = float(valore_str.strip().replace(",", "."))
            if soglia < 0:
                self._view.show_alert("Inserire un importo medio minimo non negativo.")
                return
        except ValueError:
            self._view.show_alert("Inserire un valore numerico valido.")
            return

        #2: Cstruzione grafo
        self._model.costruisci_grafo(soglia)

        #3: Pulizia e popolamento della ListView
        self._view.lista_visualizzazione.controls.clear()

        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()

        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Filiali: {num_nodi}")
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Collegamenti: {num_archi}")
        )

        for u, v, data in self._model.get_all_edges():
            peso = data["weight"]
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{u} -- {v} | Importo medio: {peso:.2f} €")
            )

        self._view.update()
