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
