import pandas as pd
import os

def cargar_datos(ruta_archivo="./data/watches (cleaned).csv"):
    """Carga de forma segura el archivo CSV del proyecto."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo '{ruta_archivo}' no existe. Por favor, colóquelo en la carpeta data/."
        )
    return pd.read_csv(ruta_archivo)

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
