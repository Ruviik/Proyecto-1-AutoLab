# 🚀 AutoLab v2.0

Herramienta de automatización DevOps para despliegue y gestión de servidores Linux (Ubuntu).

## ✨ Características
- **Multiplataforma:** Funciona nativamente en Windows y Linux.
- **Zero-Config:** Asistente de configuración automática (creación de `.env`).
- **Portable:** No requiere instalación global de Python, usa entornos virtuales aislados.
- **Funciones:**
    - Actualización del sistema (`apt update/upgrade`).
    - Despliegue de Stack LAMP (Apache + PHP).
    - Gestión de conexiones SSH seguras.

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

## 🛠️ Tecnologías
- **Python 3.13**
- **VirtualBox** (Ubuntu Desktop)
- **Git & GitHub**
- **Paramiko** (Librería SSH)

**Autor:** Ruvik
**Repositorio:** [(https://github.com/Ruviik/Proyecto-1-AutoLab)]

## 📋 Diario de Desarrollo
Consulta `DIARIO_DE_BORDO.md` para ver el progreso paso a paso y los problemas resueltos.