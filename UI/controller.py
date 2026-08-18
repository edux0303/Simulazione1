import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # ------------------------------------------------------------------
    # popolamento dei dropdown
    # ------------------------------------------------------------------
    def fillDDGenre(self):
        for gid, nome in DAO.getAllGenres():
            self._view.ddGenre.options.append(
                ft.dropdown.Option(key=str(gid), text=nome)
            )

    def fillDDArtist(self):
        """Popola il dropdown degli artisti con i nodi del grafo appena creato."""
        self._view.ddArtist.options.clear()
        self._view.ddArtist.value = None
        for artista in sorted(self._model.getNodi(), key=lambda a: a.Name):
            self._view.ddArtist.options.append(
                ft.dropdown.Option(key=str(artista.ArtistId), text=artista.Name)
            )

    # ------------------------------------------------------------------
    # PUNTO 1
    # ------------------------------------------------------------------
    def handleCreaGrafo(self, e):
        self._view.clear_results()

        if self._view.ddGenre.value is None:
            self._view.create_alert("Seleziona un genere")
            self._view.update_page()
            return

        try:
            genre_id = int(self._view.ddGenre.value)
        except ValueError:
            self._view.create_alert("Genere non valido")
            self._view.update_page()
            return

        self._model.buildGraph(genre_id)

        if self._model.getNumNodi() == 0:
            self._view.print_result("Nessun artista per il genere selezionato")
            self._view.enable_cammino(False)
            self._view.update_page()
            return

        self._view.print_result("Grafo correttamente creato:")
        self._view.print_result(f"Numero di nodi:{self._model.getNumNodi()}")
        self._view.print_result(f"Numero di archi:{self._model.getNumArchi()}")

        artista, influenza = self._model.getPiuInfluente()
        if artista is not None:
            self._view.print_result(
                f"Artista più influente: {artista}, con influenza: {influenza}")

        top5 = self._model.getTop5Archi()
        if len(top5) > 0:
            self._view.print_result("Top 5 archi:")
            for u, v, peso in top5:
                self._view.print_result(f"{u} -> {v} : {peso}")

        # abilita la sezione del punto 2
        self.fillDDArtist()
        self._view.enable_cammino(True)
        self._view.update_page()

    # ------------------------------------------------------------------
    # PUNTO 2
    # ------------------------------------------------------------------
    def handleCammino(self, e):
        self._view.clear_results()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Crea prima il grafo")
            self._view.update_page()
            return

        if self._view.ddArtist.value is None:
            self._view.create_alert("Seleziona un artista")
            self._view.update_page()
            return

        try:
            artist_id = int(self._view.ddArtist.value)
        except ValueError:
            self._view.create_alert("Artista non valido")
            self._view.update_page()
            return

        partenza = self._model.getArtistById(artist_id)
        if partenza is None:
            self._view.create_alert("Artista non presente nel grafo")
            self._view.update_page()
            return

        cammino, numArchi = self._model.getCammino(partenza)

        self._view.print_result(
            f"Cammino piu lungo a pesi crescenti da {partenza}: {numArchi} archi")
        for artista in cammino:
            self._view.print_result(f"  {artista}")
        self._view.update_page()

