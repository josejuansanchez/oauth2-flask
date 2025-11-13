from flask import Flask, session, redirect, request, url_for, jsonify
from urllib.parse import urlencode
from dotenv import load_dotenv
import os, secrets
import requests

# ------------------------------------------------------------
# Cargamos las variables de entorno del archivo .env
# Esto nos permite configurar client_id, client_secret, etc.
# sin ponerlos directamente en el código.
# ------------------------------------------------------------
load_dotenv()

app = Flask(__name__)

# ------------------------------------------------------------
# Clave secreta de Flask usada para firmar cookies de sesión.
# Si no existe FLASK_SECRET en .env, generamos una automáticamente.
# ------------------------------------------------------------
app.secret_key = os.environ.get("FLASK_SECRET", secrets.token_hex(16))

# ------------------------------------------------------------
# Función para leer variables de entorno obligatorias.
# Si falta alguna, detenemos la ejecución de la aplicación.
# ------------------------------------------------------------
def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Falta la variable de entorno requerida: {name}")
    return value

# ------------------------------------------------------------
# Variables de entorno necesarias para utilizar OAuth con GitHub
# ------------------------------------------------------------
CLIENT_ID     = get_env("GITHUB_CLIENT_ID")
CLIENT_SECRET = get_env("GITHUB_CLIENT_SECRET")
AUTH_URL      = get_env("GITHUB_AUTH_URL")        # URL donde GitHub inicia el login
TOKEN_URL     = get_env("GITHUB_TOKEN_URL")       # URL donde se intercambia el code por access_token
API_URL       = get_env("GITHUB_API")             # URL base de la API de GitHub


# ------------------------------------------------------------
# Ruta principal: Muestra un enlace para iniciar el login en GitHub
# ------------------------------------------------------------
@app.route("/")
def home():
    return "<a href='/login'>Iniciar login con GitHub</a>"


# ------------------------------------------------------------
# Paso 1. Redirige al usuario a GitHub para iniciar sesión
# ------------------------------------------------------------
@app.route("/login")
def login():
    # --------------------------------------------------------
    # "state" es un token anti-CSRF.
    # GitHub nos devolverá este mismo valor y así validamos
    # que la respuesta corresponde a la sesión original.
    # --------------------------------------------------------
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state

    # --------------------------------------------------------
    # Parámetros del flujo OAuth clásico (authorization_code)
    # --------------------------------------------------------
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": url_for("callback", _external=True),  # A dónde debe volver GitHub
        "scope": "read:user user:email",                      # Permisos solicitados
        "state": state,                                       # Protección CSRF
        "response_type": "code"                               # Queremos un "authorization code"
    }

    # Redirigimos al usuario a GitHub con los parámetros adecuados
    return redirect(f"{AUTH_URL}?{urlencode(params)}")


# ------------------------------------------------------------
# Paso 2. GitHub nos devuelve "code" y "state"
# ------------------------------------------------------------
@app.route("/callback")
def callback():
    # --------------------------------------------------------
    # Validamos que el "state" recibido coincide con el enviado.
    # Si no coincide puede ser por un posible ataque CSRF.
    # --------------------------------------------------------
    if request.args.get("state") != session.get("oauth_state"):
        return "CSRF detected (state mismatch)", 400

    # GitHub nos entrega el código temporal para intercambiar por un access_token
    code = request.args.get("code")

    # --------------------------------------------------------
    # Paso 3. Intercambiar "code" por "access_token"
    # Este paso requiere el CLIENT SECRET (solo en OAuth Apps)
    # --------------------------------------------------------
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,  # Obligatorio en OAuth clásico
        "code": code,
        "redirect_uri": url_for("callback", _external=True)
    }

    headers = {"Accept": "application/json"}

    # Hacemos POST al endpoint de GitHub para obtener el access_token
    token_resp = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
    token_json = token_resp.json()

    # Si GitHub no devuelve access_token, mostramos el error
    access_token = token_json.get("access_token")
    if not access_token:
        return jsonify(token_json), 400

    # --------------------------------------------------------
    # Paso 4. Usar el access_token para llamar a la API de GitHub
    # --------------------------------------------------------

    # Obtenemos los datos del usuario autenticado
    user = requests.get(
        f"{API_URL}/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json"
        },
        timeout=10
    ).json()

    # Obtenemos el correo del usuario
    emails = requests.get(
        f"{API_URL}/user/emails",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json"
        },
        timeout=10
    ).json()

    # Mostramos los datos obtenidos
    return f"""
    <h2>¡Login OK con GitHub!</h2>
    <pre>/user -> {user}</pre>
    <pre>/user/emails -> {emails}</pre>
    """


# ------------------------------------------------------------
# Ejecutamos Flask
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=4000, debug=True)
