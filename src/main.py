import os
import sys
from dotenv import load_dotenv
from ssh_manager import SSHClient
from system_updater import SystemUpdater
from web_installer import WebInstaller

load_dotenv()

HOST = os.getenv("SSH_HOST")
USER = os.getenv("SSH_USER")
PASS = os.getenv("SSH_PASS")

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