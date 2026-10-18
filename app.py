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
from src.eda import perfil_calidad_datos, AnalizadorNumerico, AnalizadorCategorico
from src.visualizations import graficar_distribucion, graficar_dispersion
from src.patterns import FlujoRegresionFacade
from src.agent import AgenteDatos






