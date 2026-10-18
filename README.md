# Proyecto_Final
Demo de Proyecto Final · Streamlit + Ollama + Scikit-learn
Ejemplo básico para clase del módulo Paradigmas de Programación para Inteligencia Artificial y Análisis de Datos.
Caso de demostración
Se utiliza el dataset Watch Market Dataset, Este conjunto de datos contiene información sobre 500+ marcas de relojes y más de 45.000 relojes ⌚. Incluye detalles como marca, modelo, precio y más. Ideal para cualquiera interesado en construir modelos de predicción de precios.

Qué demuestra
Carga de un CSV incluido o de un CSV propio.
Perfil general y calidad de datos.
Exploración de variables y correlaciones.
Visualizaciones interactivas con Plotly.
Modelo básico de regresión lineal.
Funciones reutilizables organizadas por módulos.
Clase `LocalDataAgent` para conectar con Ollama.
Contexto analítico resumido para evitar enviar todo el dataset al LLM.
Explicación local de respaldo cuando Ollama no está disponible.
Estructura
```text
Proyecto_Final_Streamlit_Ollama_ScikitLearn/
📁 Proyecto_Final/
├── 📄 app.py                  
├── 📄 README.md               
├── 📄 requirements.txt        
├── 📄 .gitignore              
├── 📁 data/
│   └── 📄 watches_cleaned.csv 
└── 📁 src/
    ├── 📄 __init__.py         
    ├── 📄 data.py             
    ├── 📄 analytics.py        
    ├── 📄 visualizations.py   
    └── 📄 agent.py
```
1. Crear entorno virtual
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
2. Instalar dependencias
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
3. Ollama
Instalar Ollama desde su sitio oficial y, con el servicio activo, descargar un modelo ligero:
```bash
ollama pull llama3.2:3b
```
En equipos con recursos limitados puede usarse:
```bash
ollama pull llama3.2:1b
```
4. Ejecutar
```bash
python -m streamlit run app.py
```
La aplicación funciona en modo analítico aun si Ollama no está disponible. El agente mostrará una explicación local de respaldo.
GitHub
El proyecto está preparado para ser subido a GitHub. Para el proyecto final, el `README.md` debe documentar claramente instalación, dependencias, modelo de Ollama y ejecución local.
