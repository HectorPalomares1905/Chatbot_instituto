import dash
from dash import dcc, html, Input, Output, State, no_update
import funciones

app = dash.Dash(
    __name__,
    assets_folder="assets",
    suppress_callback_exceptions=True   # ← fix: burbuja-bot se crea dinámicamente
)
app.title = "Chatbot - Hojas de Cálculo | ICATHI 4.0"

# Expuesto para gunicorn en producción (Render)
server = app.server

# ── MENSAJE DE BIENVENIDA ────────────────────
bienvenida = html.Div([
    html.Span("📊", className="wb-icon"),
    html.H3("Chatbot Hojas de Cálculo"),
    html.P(
        "Hola 👋 Soy tu asistente del curso. "
        "Puedes preguntarme sobre fórmulas, formato, gráficas y más. "
        "¿En qué te puedo ayudar?"
    )
], className="welcome-bubble")

# ── LAYOUT ──────────────────────────────────
app.layout = html.Div([

    html.Header([
        html.Div([
            html.Div("🤖", className="bot-avatar"),
            html.Div([
                html.Strong("Asistente ICATHI 4.0"),
                html.Span("Curso · Hojas de Cálculo Básico")
            ], className="header-title"),
        ], className="header-brand"),
        html.Div([
            html.Div([
                html.Div(className="status-dot"),
                html.Span("En línea"),
            ], className="status-pill"),
        ], className="header-right"),
    ], className="chat-header"),

    # ÁREA DE MENSAJES
    html.Div([bienvenida], id="chat-container"),

    # STORES internos
    dcc.Store(id="buffer", data=""),    # respuesta completa de la API
    dcc.Store(id="index",  data=0),     # cuántos chars ya se muestran
    dcc.Store(id="activo", data=False), # ¿hay animación en curso?

    # Interval: solo corre cuando activo=True
    dcc.Interval(id="intervalo", interval=30, disabled=True),

    # BARRA DE ENTRADA
    html.Div([
        dcc.Input(
            id="pregunta",
            type="text",
            placeholder="Escribe tu pregunta...",
            className="chat-input",
            debounce=False,
            n_submit=0,
            autoComplete="off",
        ),
        html.Button(
            "",
            id="btn-preguntar",
            className="send-button",
            n_clicks=0,
            title="Enviar"
        ),
    ], className="input-container"),

], className="app-wrapper")


# ════════════════════════════════════════════
# CALLBACK 1 — Enviar pregunta
# ════════════════════════════════════════════
@app.callback(
    Output("chat-container", "children",  allow_duplicate=True),
    Output("buffer",         "data",      allow_duplicate=True),
    Output("index",          "data",      allow_duplicate=True),
    Output("activo",         "data",      allow_duplicate=True),
    Output("intervalo",      "disabled",  allow_duplicate=True),
    Output("pregunta",       "value",     allow_duplicate=True),
    Input("btn-preguntar",   "n_clicks"),
    Input("pregunta",        "n_submit"),
    State("pregunta",        "value"),
    State("chat-container",  "children"),
    prevent_initial_call=True,
)
def enviar(n_clicks, n_submit, pregunta, historial):
    if not pregunta or not pregunta.strip():
        return no_update, no_update, no_update, no_update, no_update, no_update

    texto    = pregunta.strip()
    respuesta = funciones.responder_pregunta(texto)

    mensajes = list(historial or [])
    mensajes.append(html.Div(texto, className="user-message"))

    # Burbuja bot con dcc.Markdown — empieza con cursor solamente
    mensajes.append(
        html.Div(
            dcc.Markdown("▍", id="burbuja-bot", className="md-bot"),
            className="bot-message"
        )
    )

    return mensajes, respuesta, 0, True, False, ""


# ════════════════════════════════════════════
# CALLBACK 2 — Animación de escritura
# Solo actualiza el Markdown de la burbuja bot,
# no reconstruye todo el historial.
# ════════════════════════════════════════════
VELOCIDAD = 18   # caracteres por tick (ajusta para más/menos velocidad)

@app.callback(
    Output("burbuja-bot", "children",  allow_duplicate=True),
    Output("index",       "data",      allow_duplicate=True),
    Output("activo",      "data",      allow_duplicate=True),
    Output("intervalo",   "disabled",  allow_duplicate=True),
    Input("intervalo",    "n_intervals"),
    State("buffer",       "data"),
    State("index",        "data"),
    State("activo",       "data"),
    prevent_initial_call=True,
)
def animar(n, buffer, idx, activo):
    if not activo or not buffer:
        return no_update, no_update, False, True

    nuevo_idx = min(idx + VELOCIDAD, len(buffer))
    visible   = buffer[:nuevo_idx]
    terminado = nuevo_idx >= len(buffer)
    cursor    = "" if terminado else "\n\n▍"

    return visible + cursor, nuevo_idx, not terminado, terminado


if __name__ == "__main__":
    app.run(debug=False)