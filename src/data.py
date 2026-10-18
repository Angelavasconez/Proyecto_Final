%%writefile src/data_loader.py
import pandas as pd
import os

class GestorDataset:
    def __init__(self, ruta):
        self.ruta = ruta
        self.data = None

    def cargar_datos(self):
        if not os.path.exists(self.ruta):
            raise FileNotFoundError(f"El archivo {self.ruta} no existe. Por favor, súbelo a la carpeta 'data'.")
        self.data = pd.read_csv(self.ruta)
        return self.data

    def obtener_datos(self):
        if self.data is None:
            raise ValueError("El dataset no ha sido cargado.")
        return self.data.copy()
