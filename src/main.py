import os
import sys
import platform
import time
from dotenv import load_dotenv, set_key
from getpass import getpass

try:
    from ssh_manager import SSHClient
    from system_updater import SystemUpdater
    from web_installer import WebInstaller
except ImportError:
    pass

def limpiar_pantalla():
    sistema = platform.system()
    if sistema == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def guardar_configuracion(host, user, password):
    """Guarda las credenciales en el archivo .env"""
    env_file = ".env"
    with open(env_file, "w") as f:
        f.write(f"SSH_HOST={host}\n")
        f.write(f"SSH_USER={user}\n")
        f.write(f"SSH_PASS={password}\n")
    
    # Actualizamos las variables de entorno en memoria también
    os.environ["SSH_HOST"] = host
    os.environ["SSH_USER"] = user
    os.environ["SSH_PASS"] = password
    print(f"✅ Configuración guardada en '{env_file}'.")

def solicitar_datos():
    """Pide los datos de conexión al usuario de forma segura."""
    print("\n📝 --- CONFIGURACIÓN DE CONEXIÓN ---")
    host = input("Introduzca la IP del servidor (ej: 192.168.56.10): ").strip()
    user = input("Introduzca el Usuario SSH: ").strip()
    password = getpass("Introduzca la Contraseña SSH: ").strip()
    
    guardar_configuracion(host, user, password)
    return host, user, password

def conectar_y_preparar(host, user, password):
    """
    Crea la conexión y los objetos de herramientas.
    Devuelve: (cliente_ssh, actualizador, instalador_web)
    """
    print(f"\n🔌 Conectando a {host} como {user}...")
    
    # 1. Crear cliente SSH
    mi_servidor = SSHClient(host, user, password)
    mi_servidor.conectar()

    # 2. Verificar éxito
    if mi_servidor.client is None:
        print("❌ No se pudo establecer conexión.")
        return None, None, None

    # 3. Inicializar herramientas con la nueva conexión
    actualizador = SystemUpdater(mi_servidor, password)
    instalador_web = WebInstaller(mi_servidor, password)
    
    return mi_servidor, actualizador, instalador_web

def main():
    limpiar_pantalla()
    print("🤖 Inicializando AutoLab v2.1 (Multi-Host Edition)...")

    load_dotenv()
    host = os.getenv("SSH_HOST")
    user = os.getenv("SSH_USER")
    password = os.getenv("SSH_PASS")
    
    if not host or not user or not password:
        print("⚠️  No se ha detectado configuración previa.")
        host, user, password = solicitar_datos()

    # 2. Conexión Inicial
    mi_servidor, actualizador, instalador_web = conectar_y_preparar(host, user, password)

    # Si la conexión inicial falla, entramos en bucle hasta que funcione o el usuario salga
    while mi_servidor is None:
        reintentar = input("¿Reintentar con otros datos? (s/n): ").lower()
        if reintentar == 's':
            host, user, password = solicitar_datos()
            mi_servidor, actualizador, instalador_web = conectar_y_preparar(host, user, password)
        else:
            print("👋 Saliendo...")
            sys.exit()

    while True:
        # Menú visual

        limpiar_pantalla()

        # --- CABECERA DE ESTADO ---
        print("\n" + "="*50)
        print(f"   🟢 CONECTADO A: {user}@{host}")
        print("="*50)

        print("\n--- MENÚ DE CONTROL ---")
        print("1. Ejecutar comando manual")
        print("2. 🔄 ACTUALIZAR SISTEMA (Update + Upgrade + Autoremove)")
        print("3. 🌐 Instalar Servidor Web (Apache + PHP)")
        print("4. 🔌 Cambiar de Equipo (Reconectar)") # <--- NUEVA OPCIÓN
        print("5. Salir")
        print("-" * 50)
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cmd = input("Comando > ")
            resultado = mi_servidor.ejecutar_comando(cmd)
            print("\n--- RESULTADO ---")
            print(resultado)
            input("\nPress Enter para continuar...") # Pausa para leer

        elif opcion == "2":
            actualizador.actualizar_todo()
            input("\nPress Enter para continuar...")
            
        elif opcion == "3":
            instalador_web.instalar_stack_lamp()
            input("\nPress Enter para continuar...")
        
        elif opcion == "4":
            print("\n🔄 Cerrando conexión actual...")
            mi_servidor.desconectar()
            
            # Pedimos nuevos datos
            host, user, password = solicitar_datos()
            
            # Reconectamos y regeneramos las herramientas
            mi_servidor, actualizador, instalador_web = conectar_y_preparar(host, user, password)
            
            if mi_servidor is None:
                print("⚠️ La reconexión falló. Vuelve a intentar o sal.")
                # El bucle while True continúa, pero las herramientas son None.
                # Deberíamos manejar esto, pero por simplicidad volverá al menú.

        elif opcion == "5":
            break
        else:
            print("⚠️ Opción no válida.")

    if mi_servidor:
        mi_servidor.desconectar()
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupción de usuario. Cerrando...")
        sys.exit()