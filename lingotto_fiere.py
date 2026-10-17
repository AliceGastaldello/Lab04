class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        return self.codice == other.codice

    def __str__(self):
        if self.stand is None:
            return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand"
        return f"{self.codice}: {self.nome} {self.cognome} - {self.stand}"

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = int(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def prezzo_finale(self):
        return self.prezzo_base

    def __eq__(self,other):
        return self.codice == other.codice

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.prezzo_finale()} - {stato}"

class StandPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, n_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.n_prese = int(n_prese)

    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 *self.n_prese)

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.prezzo_finale()} - Prese aggiuntive: {self.n_prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, testo):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.testo = str(testo)

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = "Non disponibile"

        return f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.prezzo_finale()} - Posizione: {self.testo} - {stato}"




class LingottoFiere:
    def __init__(self,nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.stand={}
        self.espositori={}

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nuovo_nome):
        self.__nome = nuovo_nome


    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""

        try:
            f = open(file_path, "r")
            for line in f:
                line = line.strip()
                campo = line.split(",")

                if campo[0].startswith("E"):
                    espositore = Espositore(campo[0], campo[1], campo[2])
                    self.espositori[campo[0]] = espositore

                elif campo[0].startswith("S"):
                    if len(campo) ==4 :
                        stand = Stand(campo[0], campo[1], campo[2], campo[3])
                    elif campo[4].isdigit():
                        stand = StandPrese(campo[0], campo[1], campo[2], campo[3], campo[4])
                    elif campo[4].isalpha():
                        stand = StandPremium(campo[0], campo[1], campo[2], campo[3], campo[4])

                self.stand[campo[0]] = stand

            f.close()

        except FileNotFoundError:
            print("File non caricato corettamente")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""

        if codice_stand not in self.stand:
            raise ValueError("Stand non trovato")

        if codice_espositore not in self.espositori:
            raise ValueError("Espositore non trovato")

        stand = self.stand[codice_stand]
        espositore = self.espositori[codice_espositore]

        if not stand.disponibile:
            raise ValueError("Stand non disponibile")

        if espositore.stand is not None:
            raise ValueError("L'espositore ha già uno stand")

        stand.disponibile = False
        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori.values():
            print(espositore)


    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand.values())