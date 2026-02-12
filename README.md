# 🤖 Chatbot ICATHI 4.0 — Hojas de Cálculo

Chatbot interactivo para el curso de Hojas de Cálculo Básico, construido con Dash + OpenAI.

---

## 📁 Estructura del proyecto

```
chatbot-icathi/
├── app.py              # App principal Dash
├── funciones.py        # Lógica OpenAI
├── requirements.txt    # Dependencias Python
├── Procfile            # Comando para Render/gunicorn
├── .env                # API Key (NO subir a GitHub)
├── .gitignore          # Archivos ignorados por Git
└── assets/
    └── styles.css      # Estilos del chatbot
```

---

## 🚀 Despliegue paso a paso

### 1️⃣ Subir a GitHub

```bash
# Inicializar repositorio
git init
git add .
git commit -m "primer commit"

# Conectar con GitHub (crea el repo vacío primero en github.com)
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

> ⚠️ El archivo `.env` está en `.gitignore` — no se subirá. La API Key se configura en Render directamente.

---

### 2️⃣ Desplegar en Render.com

1. Entra a [render.com](https://render.com) e inicia sesión
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

| Campo | Valor |
|-------|-------|
| **Name** | chatbot-icathi |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:server --workers 1 --threads 4 --timeout 120` |

5. En la sección **"Environment Variables"** agrega:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-proj-tu-api-key-real` |

6. Click en **"Create Web Service"**
7. Esperar ~2 minutos mientras Render construye y despliega

---

## 💻 Ejecutar localmente

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env con tu API Key real

# 4. Ejecutar
python app.py
```

Abre http://localhost:8050 en tu navegador.

---

## ⚙️ Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `OPENAI_API_KEY` | API Key de OpenAI (obtenla en platform.openai.com) |
