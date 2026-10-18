import streamlit as st

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

try:
  from src.data_loader import cargar_datos
  from src.eda import perfil_calidad_datos
  from src.visualizations import generar_grafico_distribucion
  from src.agent import AgenteDatos
except ImportError as e:
  st.error(f" X Error en la estructura de los archivos dentro de 'src/': {e}")
  st.stop()

try:
  df = cargar_datos()
  st.sidebar.success("Dataset muy bien cargado")
except FileNotFoundError as err:
    st.error("⚠️ **Control de Entorno (Dataset Ausente):**")
    st.info(str(err))
    st.stop()




