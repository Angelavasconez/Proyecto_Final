import streamlit as st
import os

st.title("Proyecto Final Integrador")

st.write("Este proyecto presenta el desarrollo de una aplicación modular en Streamlit para explorar y analizar un dataset relacionado con Watch Market Dataset")
st.write("Elaborado por: Angela Vásconez V.")

st.sidebar.image("UCG.jpeg")

st.sidebar.title("Configuración")

st.set_page_config(page_title="Watch Market Explorer", layout="wide")

st.title("⌚ Explorador de Mercado de Relojes con IA Local")

# 1. Carga de Datos
st.sidebar.header("1. Carga de Datos")
archivo_cargado = st.sidebar.file_uploader("Sube tu dataset (CSV)", type="csv")

st.sidebar.write("Modelo Ollama (Llama 3.2:3b)")
st.markdown("---")

from src.data_loader import cargar_datos

ruta_dataset = None

if archivo is not None:
    os.makedirs("data/watches(cleaned).csv", exist_ok=True)
    ruta_dataset = os.path.join("data/watches(cleaned).csv", archivo.name)
    with open(ruta_dataset, "wb") as f:
        f.write(archivo.getbuffer())
elif os.path.exists("data/watches(cleaned).csv"):
    ruta_dataset = "data/watches(cleaned).csv"
    st.sidebar.info("Utilizando dataset por defecto.")








