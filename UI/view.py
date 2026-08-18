import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP-Simulazione esame Chinook"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (inizializzato nel main, dopo la creazione del controller)
        self._controller = None
        # elementi grafici
        self._title = None
        self._ddGenre = None
        self._btnCreaGrafo = None
        self._ddArtist = None
        self._btnCammino = None
        self.txt_result = None

    def load_interface(self):
        # titolo
        self._title = ft.Text("TdP-Simulazione esame Chinook", color="blue", size=24)
        self._page.controls.append(self._title)

        # riga 1: scelta del genere e costruzione del grafo
        self._ddGenre = ft.Dropdown(label="Genere", width=250)
        self._controller.fillDDGenre()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                              on_click=self._controller.handleCreaGrafo,
                                              width=250)
        row1 = ft.Row([self._ddGenre, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # riga 2: scelta dell'artista e ricerca del cammino
        # il dropdown parte disabilitato: si popola solo dopo aver creato il grafo
        self._ddArtist = ft.Dropdown(label="Artist", width=250, disabled=True)
        self._btnCammino = ft.ElevatedButton(text="Trova Cammino",
                                            on_click=self._controller.handleCammino,
                                            width=250, disabled=True)
        row2 = ft.Row([self._ddArtist, self._btnCammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # ListView dove viene stampato il risultato
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    # ------------------------------------------------------------------
    # accesso ai controlli
    # ------------------------------------------------------------------
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    @property
    def ddGenre(self):
        return self._ddGenre

    @property
    def ddArtist(self):
        return self._ddArtist

    @property
    def btnCammino(self):
        return self._btnCammino

    # ------------------------------------------------------------------
    # utilita'
    # ------------------------------------------------------------------
    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def clear_results(self):
        """Svuota la ListView dei risultati (da chiamare a ogni nuovo grafo)."""
        self.txt_result.controls.clear()

    def print_result(self, message):
        """Aggiunge una riga di testo alla ListView dei risultati."""
        self.txt_result.controls.append(ft.Text(message))

    def enable_cammino(self, enabled=True):
        """Abilita/disabilita la sezione del punto 2."""
        self._ddArtist.disabled = not enabled
        self._btnCammino.disabled = not enabled

    def update_page(self):
        self._page.update()