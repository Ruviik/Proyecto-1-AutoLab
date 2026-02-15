import os
import sys
from dotenv import load_dotenv, set_key

def configurar_entorno():
    env_file = ".env"

    if os.path.exists(env_file):
        load_dotenv()
        return
    
    print("⚠️  No se ha detectado configuración previa.")
    print("🔧 Iniciando asistente de configuración inicial...")

    host = input("Introduzca la IP del servidor (ej: 192.168.56.10): ").strip()
    user = input("Introduzca el Usuario SSH: ").strip()
    password = input("Introduzca la Contraseña SSH: ").strip()

    with open(env_file, "w") as f:
        f.write(f"SSH_HOST={host}\n")
        f.write(f"SSH_USER={user}\n")
        f.write(f"SSH_PASS={password}\n")
    
    print(f"✅ Configuración guardada en '{env_file}'.")
    load_dotenv()

configurar_entorno()

HOST = os.getenv("SSH_HOST")
USER = os.getenv("SSH_USER")
PASS = os.getenv("SSH_PASS")

from ssh_manager import SSHClient
from system_updater import SystemUpdater
from web_installer import WebInstaller

if not all([HOST, USER, PASS]):
    print("❌ ERROR CRÍTICO: No se encontraron las credenciales en el archivo .env")
    print("Asegúrate de haber creado el archivo .env con SSH_HOST, SSH_USER y SSH_PASS.")
    sys.exit(1)

def main():
    print("🤖 Inicializando AutoLab v2.0 (Apache Edition)...")
    mi_servidor = SSHClient(HOST, USER, PASS)
    mi_servidor.conectar()

    if mi_servidor.client is None:
        print("❌ No se pudo establecer conexión. Abortando.")
        return

    actualizador = SystemUpdater(mi_servidor, PASS)
    instalador_web = WebInstaller(mi_servidor, PASS)

    while True:
        # Menú visual
        print("\n--- MENÚ DE CONTROL ---")
        print("1. Ejecutar comando manual")
        print("2. 🔄 ACTUALIZAR SISTEMA (Update + Upgrade + Autoremove)")
        print("3. 🌐 Instalar Servidor Web (Apache)")
        print("4. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cmd = input("Comando > ")
            print(mi_servidor.ejecutar_comando(cmd))
            
        elif opcion == "2":
            actualizador.actualizar_todo()
            
        elif opcion == "3":
            instalador_web.instalar_stack_lamp()
        
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

    mi_servidor.desconectar()
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()