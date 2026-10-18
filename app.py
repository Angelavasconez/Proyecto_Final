import streamlit as st
import pandas as pd

# Importar desde el paquete src
from src import data
from src import analytics
from src import visualizations
from src import agent

# Configuración inicial de la página
st.set_page_config(
    page_title="Analítica de Relojes con IA Local",
    page_icon="⌚",
    layout="wide"
)

st.title("⌚ Explorador del Mercado de Relojes con IA")
st.markdown("Plataforma interactiva para análisis exploratorio, modelado predictivo e interpretación asistida por Inteligencia Artificial.")

st.write("Elaborado por: Angela Vásconez V.")
st.sidebar.image("UCG.jpeg")

# -----------------------------------------------------------------------------
# 1. CARGA DE DATOS
# -----------------------------------------------------------------------------
st.sidebar.header("📁 Carga de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu dataset (CSV)", type="csv")

@st.cache_data
def load_data(file):
    if file is not None:
        return data.load_uploaded_data(file)
    else:
        try:
            return data.load_default_data()
        except FileNotFoundError:
            st.sidebar.warning("No se encontró el archivo por defecto. Por favor, sube un CSV.")
            return None

df = load_data(uploaded_file)

if df is None:
    st.stop()

# -----------------------------------------------------------------------------
# ESTRUCTURA EN PESTAÑAS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Exploración (EDA)", 
    "📈 Visualizaciones", 
    "🤖 Modelo Predictivo", 
    "🧠 Asistente IA (Ollama)"
])

# Variables numéricas disponibles para análisis
numeric_cols = df.select_dtypes(include="number").columns.tolist()

# -----------------------------------------------------------------------------
# PESTAÑA 1: EXPLORACIÓN (EDA)
# -----------------------------------------------------------------------------
with tab1:
    st.header("Análisis Exploratorio de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reporte de Valores Nulos")
        df_missing = analytics.missing_report(df)
        st.dataframe(df_missing[df_missing['nulos'] > 0], use_container_width=True)
        
    with col2:
        st.subheader("Resumen Estadístico Numérico")
        df_summary = analytics.numeric_summary(df)
        st.dataframe(df_summary, use_container_width=True)
        
    st.subheader("Vista Previa del Dataset")
    st.dataframe(df.head(10), use_container_width=True)

# -----------------------------------------------------------------------------
# PESTAÑA 2: VISUALIZACIONES
# -----------------------------------------------------------------------------
with tab2:
    st.header("Visualización de Datos")
    
    if len(numeric_cols) > 0:
        col_vis1, col_vis2 = st.columns(2)
        
        with col_vis1:
            st.subheader("Distribución de Variables")
            var_hist = st.selectbox("Selecciona la variable para el Histograma:", numeric_cols)
            fig_hist = visualizations.histogram(df, var_hist)
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col_vis2:
            st.subheader("Relación entre Variables")
            var_x = st.selectbox("Eje X:", numeric_cols, index=0)
            var_y = st.selectbox("Eje Y:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            fig_scatter = visualizations.scatter(df, var_x, var_y)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.subheader("Matriz de Correlación")
        fig_corr = visualizations.correlation_heatmap(df)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("No hay suficientes variables numéricas para generar visualizaciones.")

# -----------------------------------------------------------------------------
# PESTAÑA 3: MODELO PREDICTIVO (Regresión Lineal)
# -----------------------------------------------------------------------------
with tab3:
    st.header("Entrenamiento de Modelo Predictivo Demo")
    
    if len(numeric_cols) > 1:
        target_col = st.selectbox("Selecciona la Variable Objetivo (Y):", numeric_cols, index=len(numeric_cols)-1)
        
        if st.button("Entrenar Modelo (Regresión Lineal)"):
            with st.spinner("Entrenando modelo..."):
                try:
                    # Entrenamiento
                    model_results = analytics.train_regression_demo(df, target_col)
                    
                    # Guardar resultados en sesión para usarlos en el Agente de IA
                    st.session_state['model_results'] = model_results
                    st.session_state['target_col'] = target_col
                    
                    st.success("Modelo entrenado exitosamente.")
                    
                    # Métricas
                    col_m1, col_m2, col_m3 = st.columns(3)
                    col_m1.metric("R² (R-Cuadrado)", f"{model_results['metrics']['r2']:.4f}")
                    col_m2.metric("MAE (Error Absoluto Medio)", f"{model_results['metrics']['mae']:.4f}")
                    col_m3.metric("RMSE (Raíz Error Cuadrático Medio)", f"{model_results['metrics']['rmse']:.4f}")
                    
                    # Gráfica
                    st.subheader("Rendimiento del Modelo: Reales vs. Predichos")
                    fig_pred = visualizations.predicted_vs_real(model_results['predictions'])
                    st.plotly_chart(fig_pred, use_container_width=True)
                    
                    # Coeficientes
                    st.subheader("Importancia de Variables (Coeficientes)")
                    st.dataframe(model_results['coefficients'], use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error al entrenar el modelo: {e}")
    else:
        st.warning("Se requieren al menos 2 variables numéricas para entrenar un modelo.")

# -----------------------------------------------------------------------------
# PESTAÑA 4: ASISTENTE IA (OLLAMA)
# -----------------------------------------------------------------------------
with tab4:
    st.header("Asistente Académico con IA Local (Ollama)")
    st.markdown("Realiza preguntas sobre las estadísticas y resultados del dataset. El agente utiliza un modelo de lenguaje local para interpretar el contexto calculado en Python.")
    
    # Inicializar Agente
    ai_agent = agent.LocalDataAgent(model="llama3.2:3b")
    is_online, models, status_msg = ai_agent.status()
    
    if is_online:
        st.success(f"🟢 Ollama conectado. Modelos disponibles: {', '.join(models)}")
    else:
        st.error(f"🔴 No se pudo conectar con Ollama en {ai_agent.base_url}. Error: {status_msg}")
        st.info("Asegúrate de tener Ollama ejecutándose localmente e intenta nuevamente.")
    
    # Preparar el contexto analítico
    target = st.session_state.get('target_col', numeric_cols[0] if numeric_cols else "")
    mod_res = st.session_state.get('model_results', None)
    
    context = analytics.build_agent_context(df, target, mod_res)
    
    with st.expander("Ver Contexto Estadístico Enviado a la IA"):
        st.json(context)
        st.info(agent.offline_summary(context))

    # Interfaz de Chat
    if is_online:
        user_question = st.text_input("Haz una pregunta sobre el análisis de este dataset:")
        
        if st.button("Consultar a la IA") and user_question:
            with st.spinner(f"Consultando a {ai_agent.model}..."):
                try:
                    respuesta = ai_agent.ask(user_question, context)
                    st.markdown("### 🤖 Respuesta del Asistente")
                    st.info(respuesta)
                except Exception as e:
                    st.error(f"Error en la comunicación con Ollama: {str(e)}")











