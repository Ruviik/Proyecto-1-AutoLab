# Diario de Desarrollo - AutoLab

## Fase 0: Inicialización

- **Fecha:** [11/02/2026]
- **Avances:**
    - Estructura de carpetas creada (src, docs, tests).
    - Repositorio Git iniciado.
    - VM Ubuntu Desktop instalada y configurada.
    - Red configurada: Host-Only IP 192.168.56.10.
- **Estado:** ✅ Completada.

- **Conceptos aprendidos:**

    ## Git (Control de Versiones)

    ### ¿Qué es Git y por qué lo usamos?
    Git es un **sistema de control de versiones distribuido**. No es simplemente una herramienta para "guardar copias de seguridad", sino una **máquina del tiempo** para el código.
    En este proyecto (AutoLab), Git actúa como nuestra red de seguridad. Nos permite:
    1.  **Experimentar sin miedo:** Si rompo el código en la Fase 3, puedo volver al estado exacto de la Fase 2 en segundos.
    2.  **Historial:** Saber qué cambié, cuándo y por qué (gracias a los mensajes de commit).
    3.  **Profesionalización:** Es el estándar de la industria. Trabajar sin Git hoy en día no es viable.

    ### El Flujo de Trabajo (The Git Workflow)
    Git no guarda automáticamente cada vez que pulsamos `Ctrl+S`. Funciona en tres etapas:
    1.  **Working Directory (Taller):** Donde edito mis archivos (lo que veo en la carpeta).
    2.  **Staging Area (El Escenario/Carrito):** Una zona intermedia donde elijo qué cambios quiero incluir en la próxima "foto".
    3.  **Repository (El Álbum):** Donde se guardan las "fotos" (commits) definitivas de la historia del proyecto.

    ### Comandos Utilizados

    #### 1. `git init`
    - **Función:** Inicializa un repositorio.
    - **Explicación:** Convierte una carpeta normal en una carpeta gestionada por Git. Crea un directorio oculto `.git` donde se almacena toda la base de datos de cambios. Solo se hace una vez por proyecto.

    #### 2. `git status`
    - **Función:** Muestra el estado actual del proyecto.
    - **Explicación:** Es como mirar el GPS. Nos dice:
        - Qué archivos son nuevos y Git no los conoce ("Untracked").
        - Qué archivos han cambiado pero no están listos para guardarse.
        - Qué archivos están listos en el "Staging Area" para ser confirmados.

    #### 3. `git add <archivo>`
    - **Función:** Mueve cambios del "Working Directory" al "Staging Area".
    - **Explicación:** Es como preparar la maleta antes del viaje. Le digo a Git: "Quiero que incluyas este archivo en la próxima foto".
        - `git add .` : Añade todo lo que haya cambiado en la carpeta actual.

    #### 4. `git commit -m "mensaje"`
    - **Función:** Crea una nueva versión (snapshot) en el historial.
    - **Explicación:** Es el momento de "sacar la foto". Coge todo lo que había en el "Staging Area" y lo guarda permanentemente en la base de datos de Git con un identificador único (hash).
        - **Importante:** El flag `-m` nos permite adjuntar una nota explicando qué hemos hecho. Sin esto, en el futuro no sabríamos qué contiene esa versión.

**Incidencias Encontradas**:
- **Error en creación de venv:**
  - **Síntoma:** `KeyboardInterrupt` y traza de error en `subprocess.py` al ejecutar `python -m venv venv`.
  - **Consecuencia:** Carpeta `venv` creada pero incompleta (faltaba el script `activate`).
  - **Causa probable:** Interrupción del proceso de instalación de dependencias (pip) o bloqueo por parte del sistema/antivirus.
  - **Solución:** Borrar la carpeta corrupta y reintentar la creación.

---
## Fase 1: Conectividad SSH y Entornos Virtuales

- **Fecha:** [12/02/2026]
- **Objetivo:** Lograr que Python "hable" con la VM Ubuntu y ejecute comandos.
- **Estado:** ✅ Completada.

- **Conceptos aprendidos:**

    #### 1. Entornos Virtuales (`venv`)
    - **¿Qué es?:** Una "caja de herramientas" aislada para el proyecto.
    - **¿Por qué?:** Evita mezclar librerías de distintos proyectos y romper el sistema operativo.
    - **Comandos clave:**
    - Crear: `python -m venv venv`
    - Activar: `.\venv\Scripts\Activate` (Aparece `(venv)` en la terminal).
    - **Importante:** La carpeta `venv` NUNCA se sube a Git (se añade al `.gitignore`).

    #### 2. Librería `Paramiko` y SSH
    - Python necesita la librería `paramiko` para gestionar conexiones SSH.
    - **Flujo del script:**
    1.  **Importar:** Traer la librería.
    2.  **Cliente:** Crear el objeto "teléfono" (`client = paramiko.SSHClient()`).
    3.  **Política:** Aceptar claves desconocidas automáticamente (evita el "yes/no" manual).
    4.  **Conectar:** `client.connect(IP, usuario, pass)`.
    5.  **Ejecutar:** `client.exec_command("comando")`.

    #### 3. Los 3 Canales de Linux (Streams)
    Al ejecutar un comando remoto, recibimos 3 flujos de datos:
    - **`stdin`:** Entrada estándar (para enviar datos al comando).
    - **`stdout`:** Salida estándar (la respuesta correcta).
    - **`stderr`:** Salida de error (si algo falla).
    *Es necesario leer (`read()`) y decodificar (`decode()`) estos flujos para ver texto legible.*

    #### 4. GitHub (Remoto)
    - Vinculado el repositorio local con GitHub.
    - Primer `git push` realizado con éxito. El código ahora está respaldado en la nube.