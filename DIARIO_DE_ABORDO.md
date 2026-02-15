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