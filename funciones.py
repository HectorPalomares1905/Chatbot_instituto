from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI()

# ===============================
# TEMARIO BASE DEL CURSO
# ===============================
TEMARIO = """
Curso: Hojas de cálculo nivel básico

Unidad 1: Inicio y edición de hojas y libros
- Inicio y edición de datos
- Edición de libros y hojas de cálculo
- Operaciones con archivos
- Manipulación de celdas

Unidad 2: Formato y configuración de página
- Formato de fuente
- Formato de alineación
- Estilos de celda
- Formato de números
- Bordes
- Relleno
- Corrección ortográfica

Unidad 3: Uso de fórmulas
- Fórmulas
- Estructura de fórmula
- Operadores
- Funciones básicas (SUMA, PROMEDIO, etc.)

Unidad 4: Gráficas e impresión
- Creación de gráficas
- Edición de gráficas
- Impresión
"""

SYSTEM_PROMPT = """
Eres un asistente de un curso de Hojas de Cálculo nivel básico.

FORMATO DE RESPUESTA:
- Usa **negritas** para resaltar conceptos clave.
- Usa listas con viñetas ( - ) o numeradas cuando corresponda.
- Usa `código` para fórmulas o funciones. Ejemplo: `=SUMA(A1:A10)`.
- Usa encabezados (##) solo si la respuesta es larga.
- Tono amigable, claro y conciso.

REGLAS:
1) SOLO responde temas del temario.
2) Si es de hojas de cálculo pero NO está en el temario:
   Responde EXACTAMENTE: "Este tema no forma parte del curso."
3) Si NO tiene relación con hojas de cálculo:
   Responde EXACTAMENTE: "Solo puedo responder temas del curso de hojas de cálculo."
4) No inventes contenido fuera del temario.
"""


def responder_pregunta(pregunta: str) -> str:
    user_prompt = f"TEMARIO:\n{TEMARIO}\n\nPregunta del alumno:\n{pregunta}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error al consultar el modelo: {str(e)}"