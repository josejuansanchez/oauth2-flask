# OAuth 2.0. Autorización Delegada

**OAuth 2.0** es un estándar abierto que permite la **autorización delegada**. Su objetivo es permitir que una aplicación de terceros (el *cliente*) acceda a información protegida que está almacenada en un servidor, **sin que el usuario tenga que compartir sus credenciales** con esa aplicación.

La especificación de OAuth 2.0 define varios roles fundamentales:

### **Cliente**

La aplicación que solicita acceso a un recurso protegido en nombre del usuario.

### **Propietario del recurso**

La entidad que posee el recurso protegido y que concede el permiso de acceso. Normalmente es el usuario final.

### **Servidor de autorización**

El servidor encargado de autenticar al propietario del recurso y emitir los *tokens de acceso*.

### **Servidor de recursos**

El servidor donde están almacenados los recursos protegidos a los que el cliente quiere acceder.

## Flujo de OAuth 2.0

OAuth 2.0 se basa en **tokens de acceso** para otorgar autorización.
Un token de acceso representa el permiso concedido a una aplicación para actuar en nombre del usuario.

Para obtener estos tokens, existen varios **flujos (grant types)**, cada uno diseñado para un escenario concreto. Los principales son:

### **Flujo de código de autorización (Authorization Code Flow)**

El más seguro y el más utilizado. Involucra al servidor de autorización y está pensado para aplicaciones web y móviles.

### **Flujo de credenciales del cliente (Client Credentials Flow)**

Permite que una aplicación obtenga un token usando sus propias credenciales, sin intervención del usuario. Se usa para procesos backend o automatizados.

### **Flujo de contraseña del propietario del recurso (Resource Owner Password Flow)**

El cliente envía directamente el usuario y la contraseña del propietario del recurso. Está obsoleto y se desaconseja por motivos de seguridad.

### **Flujo implícito (Implicit Flow)**

Diseñado originalmente para aplicaciones web sin backend. Hoy está en desuso y se prefiere el Authorization Code Flow con PKCE.

## Diagrama del flujo de código de autorización

![](images/oauth20-flow.png)

Imagen obtenida de [IBM](https://www.ibm.com/docs/es/cics-ts/6.x?topic=cics-oauth-20).

1. El usuario (propietario del recurso) inicia una acción en la aplicación cliente.

2. La aplicación cliente redirige al usuario hacia el servidor de autorización para solicitar permiso.

3. El servidor de autorización pide al usuario que se autentique y confirme la autorización para la aplicación cliente.

4. El usuario se autentica y concede el permiso solicitado por la aplicación.

5. El servidor de autorización envía un código de autorización a la aplicación cliente (normalmente a través de una redirección).

6. La aplicación cliente envía ese código al servidor de autorización para intercambiarlo por un token de acceso.

7. El servidor de autorización devuelve un token de acceso a la aplicación cliente.

8. La aplicación cliente usa el token de acceso para solicitar el recurso protegido al servidor de recursos.

9. El servidor de recursos responde a la aplicación cliente con la información solicitada.

10. La aplicación cliente entrega la respuesta final al usuario.

## Cómo crear una OAuth App en GitHub

En la documentación oficial de GitHub se explica cómo [crear una OAuth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app).

## GitHub OAuth Scopes

Los **OAuth Scopes** definen los permisos que una aplicación solicita al usuario durante el proceso de autorización.

Estos permisos determinan qué acciones puede realizar la aplicación en nombre del usuario y a qué datos puede acceder.

En la documentación oficial de GitHub puede encontrar una lista completa de los [OAuth Scopes](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps) disponibles.

**Ejemplos de scopes relacionados con el usuario**

| Scope | Permisos |
| ----- | -------- |
| `read:user`  | Leer información pública y privada básica del usuario |
| `user:email` | Leer correos electrónicos privados del usuario |

**Ejemplos de scopes relacionados con repositorios**

| Scope | Permisos |
| ----- | -------- |
| `repo` | Acceso total a repositorios públicos y privados |
| `public_repo` | Acceso a repositorios públicos |
| `repo:status` | Ver estados de commits  |

## Cómo ejecutar la aplicación de ejemplo

1. Clona este repositorio:

    ```bash
    git clone https://github.com/josejuan/oauth2-flask.git
    ```

2. Navega al directorio del proyecto:

    ```bash
    cd oauth2-flask/ejemplo
    ```

3. Crea un entorno virtual e instale las dependencias:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Crea un archivo `.env` y configura las variables de entorno necesarias. Tendrá que configurar el `CLIENT_ID` y `CLIENT_SECRET` de tu OAuth App de GitHub.

5. Ejecuta la aplicación Flask:

    ```bash
    python3 app.py
    ```

6. Abre tu navegador a la URL `http://localhost:4000` para interactuar con la aplicación.


## Referencias

- [OAuth Playground](https://www.oauth.com/playground/)
- [Introducción a OAuth 2](https://www.digitalocean.com/community/tutorials/una-introduccion-a-oauth-2-es). Digital Ocean.
- [Cross-site request forgery](https://es.wikipedia.org/wiki/Cross-site_request_forgery). Wikipedia.
