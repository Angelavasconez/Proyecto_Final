%%writefile src/eda.py
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

def perfil_calidad_datos(df):
    """Función pura para perfilar el dataset."""
    perfil = pd.DataFrame({
        'Tipo de Dato': df.dtypes,
        'Valores Nulos': df.isnull().sum(),
        'Porcentaje Nulos (%)': round((df.isnull().sum() / len(df)) * 100, 2),
        'Valores Únicos': df.nunique()
    })
    return perfil

class AnalizadorVariable(ABC):
    def __init__(self, nombre, serie):
        self.nombre = nombre
        self.serie = serie.dropna()

    @abstractmethod
    def analizar(self):
        pass

class AnalizadorNumerico(AnalizadorVariable):
    def analizar(self):
        return {
            "Variable": self.nombre,
            "Tipo": "Numérico",
            "Media": round(self.serie.mean(), 2),
            "Desviación Estándar": round(self.serie.std(), 2),
            "Máximo": self.serie.max(),
            "Mínimo": self.serie.min()
        }

class AnalizadorCategorico(AnalizadorVariable):
    def analizar(self):
        return {
            "Variable": self.nombre,
            "Tipo": "Categórico",
            "Moda": self.serie.mode().iloc[0] if not self.serie.empty else None,
            "Frecuencia Moda": self.serie.value_counts().iloc[0] if not self.serie.empty else 0
        }
