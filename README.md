# 🚀 AutoLab v2.2 (DevOps Automation Tool)

**AutoLab** es una herramienta de automatización profesional escrita en Python, diseñada para simplificar el despliegue, gestión y mantenimiento de servidores Linux (Ubuntu/Debian) de forma segura y desatendida.

## ✨ Características Principales

### 🧩 Soporte Universal (Multi-Distro)
* **Detección Inteligente:** El sistema identifica automáticamente si el servidor es **Debian/Ubuntu** (`apt`) o **RHEL/CentOS/Fedora** (`dnf`).
* **Adaptación de Servicios:** Traduce automáticamente los nombres de paquetes y servicios (`apache2` ↔ `httpd`, `ufw` ↔ `firewalld`) según el entorno.

### 🛡️ Seguridad y Auditoría
* **Gestión de Credenciales:** Uso de variables de entorno (`.env`) y ocultación de input (`getpass`).
* **Sanitización Avanzada de Logs:** Filtro basado en **Regex** que elimina contraseñas en la consola incluso en comandos complejos o encadenados (`&&`).
* **Conexión SSH:** Uso de `Paramiko` para canales seguros y persistentes.

### 🎮 Experiencia de Usuario (UX)
* **Interfaz CLI Interactiva:** Menú limpio con barra de estado (`User@Host`).
* **Multi-Host (Hot Swap):** Capacidad de cambiar de servidor objetivo sin reiniciar la aplicación.
* **Feedback en Tiempo Real:** Visualización clara del progreso.

### ⚙️ Funcionalidades DevOps
* **System Update:** Actualización automática del SO (soporta `apt upgrade` y `dnf update`).
* **Web Stack Deployment:** Instalación desatendida de Stack LAMP (Apache/Httpd + PHP).
* **Comandos Remotos:** Ejecución de comandos arbitrarios en el servidor.

### 🌍 Portabilidad (Windows & Linux)
* **Zero-Config:** Scripts de lanzamiento que configuran el entorno virtual (`venv`) automáticamente.

### 🐳 Containerización (Docker)
* **Gestión de Ciclo de Vida:** Instalación del motor Docker, despliegue de contenedores (Nginx) y visualización de estado.
* **Formatos Personalizados:** Tablas de estado limpias y legibles integradas en la CLI.

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
- [x] **Fase 6:** Soporte Enterprise (RHEL/CentOS) y Hardening de Seguridad.
- [x] **Fase 7:** Implementación de DockerManager.

---

## 📂 Estructura del Código

```text
AutoLab/
├── src/                  # Código Fuente
│   ├── main.py           # Punto de entrada y menú principal
│   ├── docker_manager.py # Gestión de contenedores (Docker Engine)
│   ├── ssh_manager.py    # Cliente SSH con sanitización Regex
│   ├── system_updater.py # Actualizador universal (APT/DNF)
│   └── web_installer.py  # Instalador Web universal (Apache2/Httpd)
├── docs/                 # Documentación y Diarios
│   └── DIARIO_DE_BORDO.md
├── requirements.txt      # Dependencias (pip)
├── run_autolab.bat       # Lanzador Windows
├── run_autolab.sh        # Lanzador Linux
├── .gitignore            # Archivos excluidos (.env, venv/)
└── README.md             # Este archivo
```

---

## 🛠️ Tecnologías
- **Python 3.13**
- **Docker** (Motor de Contenedores)
- **VirtualBox** (Ubuntu Desktop / RHEL)
- **Git & GitHub**
- **Paramiko** (Librería SSH)

**Autor:** Ruvik
**Repositorio:** [(https://github.com/Ruviik/Proyecto-1-AutoLab)]

## 📋 Diario de Desarrollo
Consulta `DIARIO_DE_BORDO.md` para ver el progreso paso a paso y los problemas resueltos.