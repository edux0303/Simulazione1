import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodi = []
        self._idMap = {}      # ArtistId -> oggetto Artist
        self._pop = {}        # ArtistId -> popolarita (brani venduti del genere)

        # risultati della ricorsione del punto 2
        self._camminoOttimo = []
        self._pesoUltimoArco = 0

    # ------------------------------------------------------------------
    # PUNTO 1 - costruzione del grafo
    # ------------------------------------------------------------------
    def buildGraph(self, genere):
        """Costruisce il grafo orientato e pesato degli artisti del genere."""
        self._grafo.clear()
        self._pop = {}

        self._nodi = DAO.getNodi(genere)
        self._idMap = {a.ArtistId: a for a in self._nodi}

        # i nodi vanno aggiunti PRIMA degli archi: gli artisti mai acquistati
        # non compaiono in nessun arco ma restano vertici isolati del grafo
        self._grafo.add_nodes_from(self._nodi)

        # clienti: ArtistId -> insieme dei CustomerId che l'hanno acquistato
        clienti = {}
        for row in DAO.getAcquisti(genere):
            clienti.setdefault(row["ArtistId"], set()).add(row["CustomerId"])
            self._pop[row["ArtistId"]] = (self._pop.get(row["ArtistId"], 0)
                                          + row["Quantita"])

        for a, b in itertools.combinations(self._nodi, 2):
            # arco solo se almeno un cliente ha acquistato brani di entrambi
            if clienti.get(a.ArtistId, set()) & clienti.get(b.ArtistId, set()):
                pa = self._pop.get(a.ArtistId, 0)
                pb = self._pop.get(b.ArtistId, 0)
                peso = pa + pb
                if pa > pb:
                    self._grafo.add_edge(a, b, weight=peso)
                elif pb > pa:
                    self._grafo.add_edge(b, a, weight=peso)
                else:
                    # popolarita uguale: due archi, uno per ogni verso
                    self._grafo.add_edge(a, b, weight=peso)
                    self._grafo.add_edge(b, a, weight=peso)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getNodi(self):
        return self._nodi

    def getArtistById(self, artist_id):
        return self._idMap.get(artist_id)

    def getPopolarita(self, artista):
        return self._pop.get(artista.ArtistId, 0)

    def getPiuInfluente(self):
        """Artista con massima (somma pesi uscenti - somma pesi entranti)."""
        migliore = None
        maxInf = None
        for n in self._grafo.nodes:
            inf = (self._grafo.out_degree(n, weight="weight")
                   - self._grafo.in_degree(n, weight="weight"))
            if maxInf is None or inf > maxInf:
                maxInf = inf
                migliore = n
        return migliore, maxInf

    def getTop5Archi(self):
        """I 5 archi di peso maggiore, in ordine decrescente."""
        archi = [(u, v, d["weight"])
                 for u, v, d in self._grafo.edges(data=True)]
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

        """
    # [(Miles Davis, Gene Krupa, {"weight": 34}), 
    (Spyro Gyra, Incognito, {"weight": 29}), 
    ...]              
        """
    """
    Cosa chiede la traccia. Scegli un artista di partenza. 
    Da lì segui le frecce del grafo, senza mai ripassare da un artista già toccato,
    e ogni freccia che percorri deve pesare più della precedente. 
    Tra tutti i percorsi possibili, vuoi il più lungo.   
    """
    """
    L'idea di fondo. Non esiste una formula per trovarlo: devi provare tutte le strade. 
    Ma "provare tutte le strade" non significa generarle tutte in memoria — costruisci un cammino 
    un passo alla volta, e quando non puoi più andare avanti torni indietro di un passo e provi un'alternativa.
     È il backtracking: esplori un albero di possibilità tenendo in mano un solo cammino, che allunghi e accorci.
    
    """
    """
    parziale è il cammino che stai costruendo in questo istante. Cresce con append quando avanzi, si accorcia con pop quando torni indietro. È uno solo per tutta l'esecuzione, riusato continuamente.

self._camminoOttimo è il record: la copia del miglior cammino visto finora. Serve perché parziale viene distrutto dai passi successivi, quindi quando trovi qualcosa di buono devi fotografarlo.

pesoPrec è il peso dell'arco con cui sei arrivato al nodo corrente. Va passato di livello in livello perché il vincolo della traccia confronta ogni arco con quello immediatamente precedente, non con un valore fisso.
    
    """
    def getCammino(self, partenza):
        if partenza is None or partenza not in self._grafo:
            return [], 0
        self._camminoOttimo = [partenza]
        self._ricorsione([partenza], -1)
        return self._camminoOttimo, len(self._camminoOttimo) - 1

    def _ricorsione(self, parziale, pesoPrec):
        if len(parziale) > len(self._camminoOttimo):
            self._camminoOttimo = list(parziale)
        ultimo = parziale[-1]
        for vicino in self._grafo.successors(ultimo):
            if vicino in parziale:
                continue
            peso = self._grafo[ultimo][vicino]["weight"]
            if peso <= pesoPrec:
                continue
            parziale.append(vicino)
            self._ricorsione(parziale, peso)
            parziale.pop()


    """
    Trovare un cammino semplice di lunghezza massima tale che ogni arco successivo 
    abbia peso strettamente
    crescente.
    """

