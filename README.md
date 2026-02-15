# 🚀 AutoLab v2.2 (DevOps Automation Tool)

**AutoLab** es una herramienta de automatización profesional escrita en Python, diseñada para simplificar el despliegue, gestión y mantenimiento de servidores Linux (Ubuntu/Debian) de forma segura y desatendida.

## ✨ Características Principales

### 🛡️ Seguridad y Auditoría
* **Gestión de Credenciales:** Uso de variables de entorno (`.env`) y ocultación de input (`getpass`).
* **Sanitización de Logs:** Filtro inteligente que oculta contraseñas en la salida de consola durante la ejecución de comandos `sudo`.
* **Conexión SSH:** Uso de `Paramiko` para canales seguros y persistentes.

### 🎮 Experiencia de Usuario (UX)
* **Interfaz CLI Interactiva:** Menú limpio con barra de estado (`User@Host`).
* **Multi-Host (Hot Swap):** Capacidad de cambiar de servidor objetivo sin reiniciar la aplicación.
* **Feedback en Tiempo Real:** Visualización clara del progreso de actualizaciones e instalaciones.

### ⚙️ Funcionalidades DevOps
* **System Update:** Automatización de `apt update`, `upgrade` y `autoremove`.
* **Web Stack Deployment:** Instalación desatendida de Apache2 y PHP.
* **Comandos Remotos:** Ejecución de comandos arbitrarios en el servidor.

### 🌍 Portabilidad (Windows & Linux)
* **Zero-Config:** Scripts de lanzamiento automático que crean el entorno virtual (`venv`) e instalan dependencias.
* **Auto-Reparación (Linux):** El lanzador detecta y corrige faltas de librerías del sistema automáticamente.

---

## 🛠️ Instalación y Uso Rápido

No necesitas instalar librerías manualmente. Los lanzadores lo hacen todo por ti.

### 🪟 En Windows
1. Clona el repositorio.
2. Haz doble clic en el archivo **`run_autolab.bat`**.
3. El script creará el entorno virtual e instalará las dependencias automáticamente.

### 🐧 En Linux (Ubuntu/Debian)
1. Clona el repositorio
2. Dale permisos de ejecución al lanzador (solo la primera vez):
   ```bash
   chmod +x run_autolab.sh
3. Ejecuta el lanzdor
   ```bash
   ./run_autolab.sh

---

## 🚦 Estado del Proyecto
- [x] **Fase 0:** Configuración de Red y Git.
- [x] **Fase 1:** Conexión SSH básica (Proof of Concept).
- [x] **Fase 2:** Estructura POO (Clases y Objetos) con sesión interactiva.
- [x] **Fase 4:** Instalación de Servicios Web (Apache + PHP) y Variables de Entorno.
- [x] **Fase 5:** Creación de launchers para mejorar portabilidad (Windows/Linux).

---

## 📂 Estructura del Código

```text
AutoLab/
├── src/                  # Código Fuente
│   ├── main.py           # Punto de entrada y menú principal
│   ├── ssh_manager.py    # Clase para gestión de conexión SSH
│   ├── system_updater.py # Módulo de actualizaciones del SO
│   └── web_installer.py  # Módulo de instalación Web (LAMP)
├── docs/                 # Documentación y Diarios
│   └── DIARIO_DE_BORDO.md
├── requirements.txt      # Lista de dependencias (pip)
├── run_autolab.bat       # Lanzador automático para Windows
├── run_autolab.sh        # Lanzador automático para Linux
├── .gitignore            # Archivos excluidos del repo (.env, venv/)
└── README.md             # Este archivo
```

---

## 🛠️ Tecnologías
- **Python 3.13**
- **VirtualBox** (Ubuntu Desktop)
- **Git & GitHub**
- **Paramiko** (Librería SSH)

**Autor:** Ruvik
**Repositorio:** [(https://github.com/Ruviik/Proyecto-1-AutoLab)]

## 📋 Diario de Desarrollo
Consulta `DIARIO_DE_BORDO.md` para ver el progreso paso a paso y los problemas resueltos.