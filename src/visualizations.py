%%writefile src/visualizations.py
import plotly.express as px

def graficar_distribucion(df, columna):
    if pd.api.types.is_numeric_dtype(df[columna]):
        return px.histogram(df, x=columna, title=f"Distribución de {columna}", marginal="box")
    else:
        conteo = df[columna].value_counts().reset_index()
        conteo.columns = [columna, 'Frecuencia']
        return px.bar(conteo, x=columna, y='Frecuencia', title=f"Frecuencias de {columna}")

def graficar_dispersion(df, x, y):
    return px.scatter(df, x=x, y=y, title=f"{y} vs {x}", opacity=0.6)
