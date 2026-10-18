import streamlit as st

st.title("Proyecto Final Integrador")

st.write("Este proyecto presenta el desarrollo de una aplicación modular en Streamlit para explorar y analizar un dataset relacionado con Watch Market Dataset")
st.write("Elaborado por: Angela Vásconez")

st.sidebar.image("UCG.jpeg")

st.sidebar.title("Configuración")

st.set_page_config(page_title="Watch Market Explorer", layout="wide")

st.title("⌚ Explorador de Mercado de Relojes con IA Local")

# 1. Carga de Datos
st.sidebar.header("1. Carga de Datos")
archivo_cargado = st.sidebar.file_uploader("Sube tu dataset (CSV)", type="csv")

if archivo_cargado is not None:
    # Guardar temporalmente
    with open("data/temp_dataset.csv", "wb") as f:
        f.write(archivo_cargado.getbuffer())
    
    gestor = GestorDataset("data/temp_dataset.csv")
    df = gestor.cargar_datos()
    st.success(f"Dataset cargado: {df.shape[0]} filas y {df.shape[1]} columnas.")

    # Creación de Pestañas
    tab_eda, tab_vis, tab_ml, tab_ia = st.tabs(["Exploración", "Visualizaciones", "Regresión Predictiva", "Asistente IA"])

    with tab_eda:
        st.subheader("Perfil de Calidad de Datos")
        st.dataframe(perfil_calidad_datos(df))
        
        st.subheader("Analizador Orientado a Objetos")
        col_selec = st.selectbox("Selecciona una variable a analizar:", df.columns)
        serie = df[col_selec]
        if pd.api.types.is_numeric_dtype(serie):
            analizador = AnalizadorNumerico(col_selec, serie)
        else:
            analizador = AnalizadorCategorico(col_selec, serie)
        st.json(analizador.analizar())

    with tab_vis:
        st.subheader("Gráficos Interactivos")
        col_graf = st.selectbox("Selecciona variable para distribución:", df.columns, key="v1")
        st.plotly_chart(graficar_distribucion(df, col_graf), use_container_width=True)

        if 'Price' in df.columns:
            st.subheader("Dispersión vs Precio")
            col_x = st.selectbox("Eje X:", df.select_dtypes(include='number').columns, key="v2")
            st.plotly_chart(graficar_dispersion(df, col_x, 'Price'), use_container_width=True)

    with tab_ml:
        st.subheader("Modelo Predictivo (Patrón Facade)")
        cols_num = df.select_dtypes(include=['number']).columns.tolist()
        if 'Price' in cols_num: cols_num.remove('Price')
        
        predictoras = st.multiselect("Selecciona variables predictoras numéricas:", cols_num)
        
        if st.button("Ejecutar Regresión") and predictoras:
            facade = FlujoRegresionFacade()
            resultados = facade.ejecutar(df, predictoras, 'Price')
            st.write("Muestra de Predicciones vs Realidad:")
            st.dataframe(resultados.head(10))
            st.plotly_chart(graficar_dispersion(resultados, 'Real', 'Predicho'))

    with tab_ia:
        st.subheader("🧠 Agente Interpretativo Local (Ollama)")
        pregunta = st.text_input("Hazle una pregunta al agente sobre los datos:")
        
        if st.button("Consultar"):
            with st.spinner("El agente está pensando (ejecución local)..."):
                agente = AgenteDatos(modelo="llama3.2")
                contexto_compacto = agente.construir_contexto(df)
                respuesta = agente.responder(pregunta, contexto_compacto)
                
                st.info(respuesta)
                with st.expander("Ver contexto enviado al modelo"):
                    st.write(contexto_compacto)
else:
    st.info("Por favor, sube un archivo CSV en la barra lateral para comenzar.")
