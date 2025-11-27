Lía Voice Assistant 1.1

Asistente de voz modular en Python creado por Joaco & Lía

Lía Voice Assistant es un asistente de voz totalmente offline, modular, extensible y escrito en Python.
Incluye reconocimiento de voz (ASR), síntesis de voz (TTS), detección de intenciones, habilidades personalizadas y un CLI para ejecutarlo fácilmente.

Esta versión usa Vosk para el reconocimiento de voz y pyttsx3 para el TTS en español.

🚀 Características principales
🎙️ ASR – Speech-to-Text con Vosk

Reconocimiento de voz offline.

Modelo Vosk configurable mediante .env.

Grabación de audio por bloques.

🔊 TTS – Text-to-Speech con pyttsx3

Usa voces en español del sistema.

Permite pronunciar respuestas de manera natural.

Inicialización automática al iniciar el asistente.

🧠 Detección de Intenciones (NLU simple)

El archivo intents.py incluye expresiones regulares para detectar:

Saludo

Hora

Fecha

Cotización del dólar (oficial / blue)

Abrir una aplicación del sistema

Despedida

🛠️ Skills (habilidades)

Las habilidades están en skills.py, incluyendo:

skill_greeting()

skill_time()

skill_date()

skill_dolar()

skill_open_app()

skill_goodbye()

skill_router(intent, info) para enrutar respuestas

⚙️ Config

El módulo config.py permite:

Cargar variables de entorno desde .env

Obtener la URL de API para el dólar

Cargar un archivo apps.yml con las apps que se pueden abrir por voz

Configurar duración máxima del ASR

Configurar modelos de Vosk

🧩 Modularidad real

Cada parte del asistente está separada:

asr.py → audio + voz a texto

tts.py → texto a voz

intents.py → detección de intenciones

skills.py → respuestas

assistant.py → bucle principal del asistente

cli.py → interfaz de línea de comandos
