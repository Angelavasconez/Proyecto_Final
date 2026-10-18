import streamlit as st

st.title("Proyecto Final Integrador")

st.write("Este proyecto presenta el desarrollo de una aplicación modular en Streamlit para explorar y analizar un dataset relacionado con Watch Market Dataset")
st.write("Elaborado por: Angela Vásconez")

st.sidebar.image("UCG.jpeg")

st.sidebar.title("Configuración")
#Configuración incial de la interfaz gráfica de Streamlit
st.set_page_config(
  page_title="Proyecto Final - Agente Local",
  page_icon="🎓", 
  layout="wide"
)

#Capa de presentación en Streamlit para el Watch Market Dataset.
# Importaciones de la arquitectura modular (carpeta src/)
from src.data import perfil_calidad_datos
from src.analytics import (
    GestorDataset, 
    AnalizadorNumerico, 
    AnalizadorCategorico, 
    FlujoRegresionFacade
)
from src.visualizations import visualizar_datos
from src.agent import AgenteDatos

st.set_page_config(page_title="Watch Market Explorer", layout="wide")
st.title("⌚ Explorador del Mercado de Relojes con IA Local")

# ==========================================
# 1. CARGA DE DATOS (BARRA LATERAL)
# ==========================================
st.sidebar.header("Cargar Dataset")
archivo = st.sidebar.file_uploader("Sube tu archivo CSV", type="csv")
ruta_dataset = None

if archivo is not None:
    os.makedirs("data", exist_ok=True)
    ruta_dataset = os.path.join("data", archivo.name)
    with open(ruta_dataset, "wb") as f:
        f.write(archivo.getbuffer())
elif os.path.exists("data/watches (cleaned).csv"):
    ruta_dataset = "data/watches (cleaned).csv"
    st.sidebar.info("Utilizando dataset por defecto.")

# ==========================================
# 2. EJECUCIÓN DE LA APLICACIÓN
# ==========================================
if ruta_dataset:
    # Instanciamos el GestorDataset y cargamos los datos[cite: 52]
    try:
        gestor = GestorDataset(ruta_dataset)
        gestor.cargar_datos()
        df = gestor.obtener_datos()
        dimensiones = gestor.mostrar_dimensiones()
        
        st.sidebar.success(f"Dataset cargado: {dimensiones[0]} filas x {dimensiones[1]} columnas.")
        
        # Pestañas de navegación
        t1, t2, t3, t4 = st.tabs([
            "📊 Exploración", 
            "📈 Visualización", 
            "⚙️ Predicción ML", 
            "🤖 Agente IA"
        ])

        # --- PESTAÑA 1: EXPLORACIÓN FUNCIONAL Y POO ---
        with t1:
            st.subheader("Perfil de Calidad de Datos")
            # Uso de la función pura importada de data.py[cite: 53]
            st.dataframe(perfil_calidad_datos(df), use_container_width=True)
            
            st.divider()
            st.subheader("Análisis de Variables (Polimorfismo)")
            col_sel = st.selectbox("Elige una variable para analizar:", df.columns)
            
            # Instanciación dinámica según el tipo de dato[cite: 52]
            if pd.api.types.is_numeric_dtype(df[col_sel]):
                analizador = AnalizadorNumerico(col_sel, df[col_sel])
            else:
                analizador = AnalizadorCategorico(col_sel, df[col_sel])
                
            st.json(analizador.analizar())

        # --- PESTAÑA 2: VISUALIZACIONES ---
        with t2:
            st.subheader("Visualización Multibiblioteca")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                libreria = st.selectbox("Librería", ["plotly", "seaborn", "matplotlib"])
            with c2:
                tipo = st.selectbox("Tipo", ["histograma", "caja", "dispersion", "barras"])
            with c3:
                x_col = st.selectbox("Eje X", df.columns)
            with c4:
                opciones_y = [None] + list(df.select_dtypes(include=[np.number]).columns)
                y_col = st.selectbox("Eje Y (Para dispersión/caja)", opciones_y)
            
            if st.button("Generar Gráfico"):
                # Se utiliza la función modular que soporta las tres librerías[cite: 54]
                # Nota: Para integrarlo nativamente en Streamlit sin bloquear el hilo con plt.show(), 
                # asegúrese de que visualizar_datos retorne la figura o use st.pyplot() internamente.
                st.set_option('deprecation.showPyplotGlobalUse', False)
                visualizar_datos(df, tipo, x_col, y_col, libreria)
                if libreria in ["matplotlib", "seaborn"]:
                    st.pyplot()

        # --- PESTAÑA 3: PATRONES DE DISEÑO (FACADE) ---
        with t3:
            st.subheader("Predicción de Precios (Regresión Lineal)")
            cols_num = df.select_dtypes(include=[np.number]).columns.tolist()
            if "Price" in cols_num:
                cols_num.remove("Price")
                
            x_vars = st.multiselect("Variables Predictoras", cols_num)
            
            if st.button("Ejecutar Regresión") and x_vars:
                with st.spinner("Ejecutando patrón Facade..."):
                    # El FlujoRegresionFacade encapsula la limpieza, separación y uso del Factory[cite: 52]
                    sistema = FlujoRegresionFacade()
                    modelo, predicciones = sistema.ejecutar(df, x_vars, "Price")
                    
                    st.success("Flujo ejecutado con éxito.")
                    st.write("Muestra de Predicciones generadas:")
                    st.dataframe(pd.DataFrame({"Predicción": predicciones}).head(10))

        # --- PESTAÑA 4: AGENTE DE IA (OLLAMA) ---
        with t4:
            st.subheader("Asistente Local (Llama 3.2)")
            pregunta = st.text_input("Haz una pregunta sobre los estadísticos del dataset:")
            
            if st.button("Consultar Ollama"):
                with st.spinner("Analizando contexto localmente..."):
                    # Se extrae el resumen del dataset mediante el GestorDataset[cite: 52]
                    contexto_calculado = gestor.describir_dataset()
                    
                    # El AgenteDatos recibe el modelo llama3.2:1b y formatea el prompt[cite: 51]
                    agente = AgenteDatos(modelo="llama3.2:1b")
                    respuesta = agente.responder(pregunta, contexto_calculado)
                    
                    st.info(respuesta)

    except Exception as e:
        st.error(f"Error en la ejecución: {str(e)}")
else:
    st.info("Sube un archivo CSV en la barra lateral para comenzar.")
