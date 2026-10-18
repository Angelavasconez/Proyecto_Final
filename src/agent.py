%%writefile src/agent.py
import ollama

class AgenteDatos:
    def __init__(self, modelo="llama3.2"):
        self.modelo = modelo

    def construir_contexto(self, df):
        # Creamos un contexto muy resumido
        nulos_criticos = df.isnull().mean().sort_values(ascending=False).head(3).to_dict()
        stats_precio = df['Price'].describe().to_dict() if 'Price' in df.columns else "No disponible"
        
        contexto = {
            "filas": df.shape[0],
            "nulos_principales": nulos_criticos,
            "estadisticas_precio": stats_precio
        }
        return str(contexto)

    def responder(self, pregunta, contexto):
        prompt_sistema = f"""Eres un analista de datos experto en relojes. 
        Responde la consulta del usuario basándote EXCLUSIVAMENTE en este contexto calculado por la app:
        CONTEXTO: {contexto}. 
        Sé conciso, analítico y profesional. No inventes datos."""
        
        try:
            respuesta = ollama.chat(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": pregunta}
                ]
            )
            return respuesta['message']['content']
        except Exception as e:
            return f"Error al conectar con Ollama: {str(e)}"
