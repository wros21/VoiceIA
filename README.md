# VoiceIA
Proyecto del Curso de IA para asistente virtual 

# VoiceAI 🎙️🤖

**VoiceAI** es un asistente virtual por voz que integra comandos automatizados, multimedia, clima y capacidades de conversación con IA como Claude IA.

## 🚀 Características

- 🗣️ Reconocimiento de voz (SpeechRecognition + PyAudio)
- 🧠 IA conversacional con ChatGPT o DeepSeek
- ☁️ Consulta del clima con OpenWeatherMap
- 🎵 Reproducción de música desde YouTube y Spotify
- ⚙️ Automatización de tareas: abrir aplicaciones, controlar el sistema
- 🗨️ Síntesis de voz para respuestas habladas
- 📧 Envío de Correo electrónico

## 📁 Estructura del proyecto


## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/wros21/VoiceAI.git
cd VoiceAI
```
2. Crea y activa un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # en Linux/macOS
venv\Scripts\activate     # en Windows
```
3. Instala las dependencias:
```bash
   pip install -r requirements.txt
```
4. Crea un archivo .env con tus claves de API:
```bash
   ANTHROPIC_API_KEY=tu_clave_claude
   OWM_API_KEY=tu_clave_openweather
   SPOTIPY_CLIENT_ID=tu_id_spotify
   SPOTIPY_CLIENT_SECRET=tu_secreto_spotify
   SPOTIPY_REDIRECT_URI=tu_url_spotify
   EMAIL_REMITENTE=correo
   EMAIL_CONTRASENA=contrasena_de_aplicacion
   API_ID=id_api_telegram
   API_HASH=api_hash_telegram
   PHONE_NUMBER=numero_telefono_propio(+502)
```
▶️ Uso

Ejecuta el asistente con:

python main.py

Para Inciiar el asistente di: "Hola Viernes"
Con este comando se inicia el ciclo de conversación

Habla comandos como:

    "¿Qué hora es?"

    "¿Qué clima hace en Ciudad de Guatemala?"

    "Reproduce en YouTube"

    "Abre el navegador"

    "Conversar con IA"
    
    "Busca en Google"

    "Abre el archivo"

    "Abre Spotify"

    "Informacion"

    "Enviar Correo"




