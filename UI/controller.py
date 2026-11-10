import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    def popola_dropdown(self):
        try:
            biblioteche = self._model.get_biblioteche()
            generi = self._model.get_generi()

            for biblioteca in biblioteche:
                self._view.dd_biblioteca.options.append(
                    self._view.opzione(str(biblioteca.id), biblioteca.nome)
                )

            for genere in generi:
                self._view.dd_genere.options.append(
                    self._view.opzione(genere, genere)
                )

            self._view.update()
        except Exception as errore:
            self._view.show_alert(
                f"Errore nel caricamento dei dati dal database:\n{errore}"
            )

    def seleziona_biblioteca(self, e):
        valore = e.control.value
        if valore == "nessun_filtro":
            self.biblioteca_selezionata = None
        else:
            self.biblioteca_selezionata = int(valore)

    def seleziona_genere(self, e):
        valore = e.control.value
        if valore == "nessun_filtro":
            self.genere_selezionato = None
        else:
            self.genere_selezionato = valore

    def mostra_libri(self, e):
        try:
            libri = self._model.get_libri_filtrati(
                self.biblioteca_selezionata,
                self.genere_selezionato,
            )

            if not libri:
                self._view.svuota_lista()
                self._view.show_alert(
                    "Nessun libro corrisponde ai filtri selezionati."
                )
                return

            self._view.mostra_libri(libri)
        except Exception as errore:
            self._view.show_alert(
                f"Errore durante la ricerca dei libri:\n{errore}"
            )