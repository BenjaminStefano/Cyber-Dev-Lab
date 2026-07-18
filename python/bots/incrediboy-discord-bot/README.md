# 🤖 Incrediboy Discord Bot

Bot multipropósito para Discord desarrollado con **Python** y
**discord.py**.

Incrediboy incluye comandos de entretenimiento, moderación, música,
economía y administración. El proyecto utiliza una arquitectura modular
basada en Cogs y persistencia local mediante SQLite.

## Características

- Comandos slash.
- Sistema modular mediante Cogs.
- Comandos de entretenimiento.
- Sistema de economía y tragamonedas.
- Recompensas diarias y clasificación de usuarios.
- Herramientas de moderación.
- Sistema de advertencias.
- Reproducción de música y cola de canciones.
- Comandos administrativos.
- Persistencia local mediante SQLite.
- Configuración segura mediante variables de entorno.

## Tecnologías

- Python 3
- discord.py
- SQLite
- yt-dlp
- FFmpeg
- python-dotenv
- aiohttp

## Estructura

```text
incrediboy-discord-bot/
├── bot.py
├── Incrediboy/
│   ├── cogs/
│   │   ├── fun.py
│   │   ├── help.py
│   │   ├── moderation.py
│   │   ├── music.py
│   │   └── system.py
│   └── utils/
│       └── helpers.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/BenjaminStefano/Cyber-Dev-Lab.git
```

Entra en el proyecto:

```bash
cd Cyber-Dev-Lab/python/bots/incrediboy-discord-bot
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

Edita `.env`:

```env
DISCORD_TOKEN=your_discord_bot_token
BOT_OWNER_ID=your_discord_user_id
```

El archivo `.env` está ignorado por Git y nunca debe publicarse.

También debes instalar FFmpeg y asegurarte de que el comando `ffmpeg`
esté disponible desde la terminal.

## Ejecución

```bash
python bot.py
```

Cuando el bot inicie correctamente, cargará los Cogs y sincronizará los
comandos slash.

## Módulos

### Entretenimiento

- Saludos.
- Bola mágica.
- Visualización de avatares.
- Tragamonedas.
- Balance y clasificación.
- Recompensa diaria.

### Moderación

- Sistema de advertencias.
- Herramientas para administrar usuarios y servidores.

### Música

- Reproducción de audio.
- Cola de canciones.
- Pausa y reanudación.
- Salto de canciones.
- Desconexión del canal de voz.

### Sistema

- Comandos reservados para el propietario del bot.

## Seguridad

- Nunca publiques el token del bot.
- No incluyas archivos `.env` en commits.
- Regenera inmediatamente cualquier token expuesto.
- Utiliza solo los intents y permisos necesarios.
- No publiques bases de datos con información de usuarios.

## Objetivos de aprendizaje

Con este proyecto practiqué:

- Programación asíncrona.
- Arquitectura modular con Cogs.
- Integración con la API de Discord.
- Comandos slash.
- Manejo de eventos e interacciones.
- Persistencia con SQLite.
- Variables de entorno.
- Reproducción de audio.
- Gestión de dependencias.
- Organización de un proyecto Python.

## Mejoras futuras

- [ ] Añadir logging estructurado.
- [ ] Centralizar la configuración.
- [ ] Agregar manejo global de errores.
- [ ] Limitar los intents utilizados.
- [ ] Crear pruebas automatizadas.
- [ ] Añadir migraciones para las bases de datos.
- [ ] Mejorar el sistema de permisos.
- [ ] Preparar despliegue con Docker.

## Uso responsable

Este proyecto fue desarrollado con fines educativos. Quien lo utilice
debe respetar los términos de servicio de Discord y las normas de los
servidores donde sea instalado.

## Licencia

Este proyecto forma parte de **Cyber-Dev-Lab**.
