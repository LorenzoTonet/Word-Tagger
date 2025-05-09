import tkinter as tk
from tkinter import filedialog

class examplesHandler:

    def __init__(self):
        self.examples = []

    # serve per ripulire le stringhe da decorazioni di formattazione inutili
    def clean_string(self, stringa):
        stringa = stringa.strip()
        stringa_senza_parentesi = stringa.replace("(", "")
        stringa_senza_parentesi2 = stringa_senza_parentesi.replace(")", "")
        stringa_senza_spazi = stringa_senza_parentesi2.replace(" ", "")
        stringa_pulita = stringa_senza_spazi.replace(",", "")
        stringa_pulita = stringa_pulita.replace("-", " ")
        return stringa_pulita

    # funziona solo con file formattati dalla classe highlight app
    def handler(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                for line in file:
                    elements = line.split("#")
                    if len(elements)>1:
                        ents = elements[1].split(",")
                        for i in range (len(ents)):
                            ents[i] = self.clean_string(ents[i])
                        entities = {"entities":[(int(el.split(";")[0]), int(el.split(";")[1]), str(el.split(";")[2])) if len(el.split(";")) == 3 else () for el in ents]}
                        self.examples.append((elements[0], entities))
        return self.examples
    
p = examplesHandler()
print(p.handler())