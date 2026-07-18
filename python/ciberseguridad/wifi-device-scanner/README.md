# WiFi Device Scanner

Herramienta de descubrimiento de dispositivos en una red local, desarrollada con **Python**, **Scapy** y **Rich**.

El programa realiza solicitudes ARP para detectar equipos activos dentro de una red IPv4 autorizada y presenta los resultados mediante una interfaz clara en la terminal.

> Utiliza esta herramienta únicamente en redes propias o donde tengas autorización explícita.

## Características

- Descubrimiento de dispositivos mediante ARP.
- Visualización de dirección IP.
- Visualización de dirección MAC.
- Resolución de hostname cuando está disponible.
- Identificación del equipo local.
- Tabla interactiva y paneles mediante Rich.
- Validación de redes IPv4 en formato CIDR.
- Límite de seguridad para rangos excesivamente grandes.
- Configuración del tiempo de espera.
- Manejo de errores y cancelación del escaneo.
- Resumen con cantidad de dispositivos y duración.

## Vista previa

![WiFi Device Scanner](assets/preview.png)

## Tecnologías

- Python 3
- Scapy
- Rich
- Npcap en Windows

## Estructura

```text
wifi-device-scanner/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── assets/
    └── preview.png
```

## Requisitos

### Windows

- Python 3.10 o superior.
- Npcap instalado.
- PowerShell ejecutado como administrador.

### Linux

- Python 3.10 o superior.
- Permisos para enviar paquetes de red.
- Ejecución mediante `sudo` cuando sea necesario.

## Instalación

Entra en la carpeta del proyecto:

```bash
cd python/ciberseguridad/wifi-device-scanner
```

Crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el programa indicando la red en formato CIDR:

```bash
python main.py 192.168.1.0/24
```

Puedes modificar el tiempo de espera:

```bash
python main.py 192.168.1.0/24 --timeout 4
```

Consulta la ayuda:

```bash
python main.py --help
```

## Ejemplo de información mostrada

- Red objetivo.
- Dirección IP local.
- Tiempo de espera.
- Fecha y hora del escaneo.
- Dirección IP de cada dispositivo.
- Dirección MAC.
- Hostname.
- Rol del dispositivo.
- Duración total.
- Cantidad de equipos detectados.

## Objetivos de aprendizaje

Con este proyecto practiqué:

- Fundamentos de redes.
- Protocolo ARP.
- Descubrimiento de hosts.
- Programación con Scapy.
- Interfaces de terminal con Rich.
- Argumentos de línea de comandos.
- Validación de direcciones y redes IPv4.
- Manejo de errores.
- Organización de proyectos Python.

## Limitaciones

- Solo analiza dispositivos de la misma red local.
- Esta versión admite únicamente IPv4.
- La resolución de hostname no siempre está disponible.
- Algunos dispositivos pueden no responder a solicitudes ARP.
- En Windows requiere Npcap y permisos de administrador.

## Roadmap

- [ ] Identificar el fabricante mediante la dirección MAC.
- [ ] Detectar automáticamente el gateway.
- [ ] Exportar resultados a JSON.
- [ ] Exportar resultados a CSV.
- [ ] Comparar escaneos anteriores.
- [ ] Detectar dispositivos nuevos.
- [ ] Añadir pruebas automatizadas.
- [ ] Seleccionar automáticamente la interfaz de red.

## Uso responsable

Este software fue creado con fines educativos y defensivos.

No debe utilizarse para analizar redes ajenas sin autorización. El usuario es responsable de cumplir las leyes, políticas y permisos aplicables.

## Licencia

Este proyecto forma parte de **Cyber-Dev-Lab**.
