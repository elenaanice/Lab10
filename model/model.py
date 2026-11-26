from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutte le Filiali (i nodi) presenti e filtrando i Collegamenti con
        importo medio per bonifico >= threshold (euro)
        """
        self.G.clear()
        #1: Carico i nodi (tutte le filiali) e costruisco la mappa id->filiale
        self._nodes = DAO.get_all_filiali()
        if self._nodes is None:
            return

        self._id_map = {f.id: f for f in self._nodes}
        self.G.add_nodes_from(self._nodes)

        #2: Carico gli archi filtrati per soglia e li aggiungo con il rispettivo peso
        collegamenti = DAO.get_collegamenti_filtrati(threshold)
        if collegamenti is None:
            return

        self._edges = []
        for id_f1, id_f2, peso in collegamenti:
            if id_f1 in self._id_map and id_f2 in self._id_map:
                f1=self._id_map[id_f1]
                f2 = self._id_map[id_f2]
                self._edges.append((f1, f2, peso))
        self.G.add_weighted_edges_from(self._edges)


    def get_num_edges(self):
        """
        Restituisce il numero di Collegamenti (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Filiali (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutti i Collegamenti (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return list(self.G.edges(data=True))
