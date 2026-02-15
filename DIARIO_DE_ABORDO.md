# Diario de Desarrollo - AutoLab

## Fase 0: Inicialización y Configuración

- **Fecha:** 11/02/2026
- **Objetivo:** Preparar el entorno de desarrollo local y la máquina virtual.
- **Estado:** ✅ Completada.

### 📋 Avances
- Estructura de carpetas creada (`src`, `docs`, `tests`).
- Repositorio Git iniciado y vinculado a GitHub.
- VM Ubuntu Desktop instalada.
- Red configurada: Host-Only IP `192.168.56.10`.

### 🧠 Conceptos Aprendidos

#### Git (Control de Versiones)
Git es un **sistema de control de versiones distribuido**. Actúa como una "máquina del tiempo" para el código, permitiendo experimentar sin miedo y manteniendo un historial profesional.

**Flujo de Trabajo (The Git Workflow):**
1.  **Working Directory:** Donde edito mis archivos.
2.  **Staging Area:** Zona intermedia (el "carrito") donde elijo qué incluir.
3.  **Repository:** Donde se guardan los `commits` definitivos.

**Comandos Clave:**
- `git init`: Inicializa el repositorio.
- `git status`: Muestra el estado de los archivos (GPS del proyecto).
- `git add .`: Mueve cambios al Staging Area.
- `git commit -m "mensaje"`: Guarda la versión (snapshot) en el historial.

### ⚠️ Incidencias
- **Error en creación de venv:**
    - **Síntoma:** `KeyboardInterrupt` y traza de error en `subprocess.py`.
    - **Solución:** Borrar la carpeta corrupta y reintentar la creación sin interrupciones.

---

## Fase 1: Conectividad SSH y Entornos Virtuales

- **Fecha:** 12/02/2026
- **Objetivo:** Lograr comunicación programática entre Python y la VM Ubuntu.
- **Estado:** ✅ Completada.

### 📋 Avances
- Creación de script de prueba de concepto (`test_connection.py`).
- Implementación de librería `Paramiko`.
- Gestión de dependencias con `pip`.

### 🧠 Conceptos Aprendidos

#### 1. Entornos Virtuales (`venv`)
- **¿Qué es?:** Entorno aislado para evitar conflictos de librerías.
- **Uso:** `python -m venv venv` para crear y `.\venv\Scripts\Activate` para activar.
- **Regla de oro:** La carpeta `venv` se añade al `.gitignore` (nunca se sube).

#### 2. Librería `Paramiko`
- **Función:** Cliente SSH puro para Python.
- **Métodos clave:**
    - `.connect()`: Establece el túnel.
    - `.exec_command()`: Envía instrucciones Bash.

#### 3. Los 3 Canales de Linux (Streams)
Al ejecutar un comando remoto, se gestionan 3 flujos:
- **`stdin`:** Entrada de datos.
- **`stdout`:** Salida estándar (éxito).
- **`stderr`:** Salida de error/avisos.

---

## Fase 2: Estructura POO y Sesión Interactiva

- **Fecha:** 12/02/2026
- **Objetivo:** Refactorizar el código "espagueti" a una arquitectura profesional orientada a objetos.
- **Estado:** ✅ Completada.

### 📋 Avances
- **Refactorización:**
    - `src/ssh_manager.py`: Clase `SSHClient` (el plano técnico).
    - `src/main.py`: Lógica de negocio y menú de usuario.
- **Hito:** Implementación de una shell interactiva que reutiliza la conexión SSH (persistencia).

### 🧠 Conceptos Aprendidos

#### 1. Clases vs. Objetos
- **Clase (`class`):** La plantilla o plano (ej: `SSHClient`).
- **Objeto (Instancia):** El ente creado en memoria (`mi_servidor`).
- **`self`:** Referencia a la propia instancia, permitiendo que cada objeto gestione sus propios datos (IP, usuario) sin mezclarse.

#### 2. Persistencia de Conexión
- A diferencia de un script lineal (abrir-ejecutar-cerrar), con objetos mantenemos el atributo `self.client` vivo mientras el bucle `while` espera órdenes del usuario.

---

## Fase 3: Automatización de Tareas (System Updater)

- **Fecha:** 13/02/2026
- **Objetivo:** Crear un módulo capaz de actualizar el sistema operativo sin intervención humana.
- **Estado:** ✅ Completada.

### 📋 Avances
- Creación del módulo `SystemUpdater`.
- Automatización de `apt update`, `upgrade` y `autoremove`.
- Limpieza profunda del historial de Git (`git-filter-repo`).

### 🧠 Conceptos Aprendidos

#### 1. Automatización de `sudo`
- **Problema:** `sudo` es interactivo y detiene la ejecución.
- **Solución:** Inyección de contraseña por tubería estándar:
  `echo 'password' | sudo -S comando`

#### 2. Canales de Salida
- Herramientas como `apt` o `sudo` a menudo escriben prompts o avisos en `stderr`, lo cual no implica necesariamente un error fatal en el script.

### 🔐 Seguridad y Sanitización
- **Incidencia:** Credenciales expuestas (hardcoded) en `main.py` y subidas al historial.
- **Solución:** Uso de **`git-filter-repo`** con un archivo de reemplazos para reescribir la historia del repositorio, eliminando las contraseñas de todos los commits anteriores.

---

## Fase 4: Servidor Web (LAMP) y Variables de Entorno

- **Fecha:** 15/02/2026
- **Objetivo:** Desplegar un stack LAMP y securizar credenciales.
- **Estado:** ✅ Completada.

### 📋 Avances
- Implementación de **Variables de Entorno** (`.env`).
- Creación del módulo `WebInstaller`.
- Despliegue automático de **Apache2** y **PHP**.
- Verificación automática mediante inyección de archivo `info.php`.

### 🧠 Conceptos Aprendidos

#### 1. Seguridad con `.env`
- Uso de `python-dotenv` para separar configuración (secretos) del código.
- Inclusión estricta de `.env` en `.gitignore`.

#### 2. El problema de las redirecciones y Sudo
- **El conflicto:** `sudo echo "x" > archivo` falla porque la redirección `>` se ejecuta con permisos de usuario normal antes de elevar privilegios.
- **Conflicto de Tuberías:** `echo pass | echo contenido | sudo ...` rompe el flujo de la contraseña.
- **Solución Técnica:** Encapsulamiento en sub-shell:
  ```python
  echo password | sudo -S sh -c "echo 'contenido' > archivo"

---

## Fase 5: Portabilidad y Despliegue Universal (Cross-Platform)

- **Fecha:** 15/02/2026
- **Objetivo:** Convertir la herramienta en una aplicación "Portable" (Plug & Play) que funcione en Windows y Linux sin configuración manual previa.
- **Estado:** ✅ Completada.

### 📋 Avances
- **Estandarización de Dependencias:** Creación de `requirements.txt` (`pip freeze`).
- **Wizard de Configuración:** `main.py` ahora detecta si falta el archivo `.env` y lanza un asistente interactivo para crearlo automáticamente.
- **Lanzadores Automáticos:**
    - **Windows (`run_autolab.bat`):** Script Batch que crea el entorno, instala dependencias y lanza la app.
    - **Linux (`run_autolab.sh`):** Script Bash con **auto-reparación**. Si detecta que falta `python3-venv`, solicita permisos `sudo` e instala el paquete automáticamente.
- **Compatibilidad OS:** Uso de la librería `platform` en Python para alternar entre `cls` (Windows) y `clear` (Linux).

### 🧠 Conceptos Aprendidos

#### 1. Congelación de Dependencias (`pip freeze`)
- Para que el proyecto funcione en otro PC, necesitamos una "lista de ingredientes" exacta.
- Comando: `pip freeze > requirements.txt`.
- Instalación: `pip install -r requirements.txt`.

#### 2. Scripting de Automatización (Batch vs Bash)
- **Batch (`.bat`):** Lenguaje nativo de Windows. Limitado pero funcional. Aprendimos a usar `cd /d "%~dp0"` para forzar la ruta relativa correcta.
- **Bash (`.sh`):** Lenguaje nativo de Linux. Más potente. Permite lógica condicional compleja como detectar si un comando falla (`$?`) y ejecutar una reparación (`apt install`).

#### 3. UX en Herramientas de Consola (CLI)
- Una herramienta DevOps no debe romperse si falta configuración. Debe **guiar al usuario**.
- Implementamos el patrón "Check & Ask": Si no existe configuración -> Preguntar -> Guardar -> Continuar.

#### 4. Permisos de Ejecución en Linux
- A diferencia de Windows, Linux requiere marcar explícitamente los scripts como ejecutables por seguridad: `chmod +x script.sh`.

## Fase 5.1: Madurez del Software (Seguridad, UX y Portabilidad)

- **Fecha:** 16/02/2026
- **Objetivo:** Profesionalizar la herramienta mejorando la experiencia de usuario, la seguridad de las credenciales y la compatibilidad entre sistemas operativos.
- **Estado:** ✅ Completada.

### 📋 Avances
1.  **Portabilidad Total:**
    - Creación de `run_autolab.bat` (Windows) y `run_autolab.sh` (Linux).
    - Implementación de **auto-reparación** en Linux: el script detecta si falta `python3-venv` y solicita permisos para instalarlo automáticamente.
2.  **Seguridad (Security Hardening):**
    - **Input Oculto:** Implementación de librería `getpass` para que las contraseñas no se vean al escribirlas.
    - **Sanitización de Logs:** Corrección de una vulnerabilidad crítica donde la contraseña se mostraba en texto plano al ejecutar comandos `sudo`. Ahora el `ssh_manager.py` detecta estos patrones y los sustituye por `[PASSWORD OCULTA]` en la consola.
3.  **Experiencia de Usuario (UX):**
    - **Barra de Estado:** El menú ahora muestra permanentemente a qué servidor y usuario estamos conectados (`User@IP`).
    - **Cambio de Host en Caliente:** Nueva opción en el menú para desconectar y conectar a otro servidor sin reiniciar el programa.
    - **Flujo Limpio:** Uso de `cls`/`clear` y pausas estratégicas para que la terminal no se sature de texto.

### 🧠 Lecciones Aprendidas
- **Seguridad en Automatización:** Nunca se debe imprimir el comando crudo (`raw command`) si este contiene credenciales inyectadas mediante `echo | sudo -S`. Es vital filtrar los logs.
- **Gestión de Estado:** Para cambiar de servidor sin cerrar el programa, es necesario reiniciar las instancias de las clases (`Updater`, `Installer`) con el nuevo objeto de conexión SSH.
- **UX en Terminal:** Un menú estático que se limpia en cada iteración da una sensación mucho más profesional que un "scroll infinito".