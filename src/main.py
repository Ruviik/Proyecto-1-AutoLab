import os
import sys
from dotenv import load_dotenv
from ssh_manager import SSHClient
from system_updater import SystemUpdater

load_dotenv()

HOST = os.getenv("SSH_HOST")
USER = os.getenv("SSH_USER")
PASS = os.getenv("SSH_PASS")

if not all([HOST, USER, PASS]):
    print("❌ ERROR CRÍTICO: No se encontraron las credenciales en el archivo .env")
    print("Asegúrate de haber creado el archivo .env con SSH_HOST, SSH_USER y SSH_PASS.")
    sys.exit(1)

def main():
    # 1. CREAR EL OBJETO (Instanciación)
    # Aquí es donde "rellenamos el formulario".
    # Creamos una variable 'mi_servidor' que ES una instancia de SSHClient.
    print("🤖 Inicializando el Asistente SSH...")
    mi_servidor = SSHClient(HOST, USER, PASS)

    # 2. CONECTAR
    # Le decimos a ESE objeto concreto que se conecte.
    mi_servidor.conectar()

    # Si la conexión falló, la propiedad .client será None. Verificamos:
    if mi_servidor.client is None:
        print("❌ No se pudo establecer conexión. Abortando.")
        return

    # 3. BUCLE DE COMANDOS (Interactividad)
    # Como la conexión está abierta, podemos pedirle cosas repetidamente
    while True:
        comando = input("\n💻 Escribe un comando (Escribe 'salir' o 'exit' para cerrar ): ")
        
        if comando.lower() in ['salir', 'exit']:
            break
        
        # Usamos el método de nuestro objeto para enviar la orden
        respuesta = mi_servidor.ejecutar_comando(comando)
        
        print("--- RESPUESTA ---")
        print(respuesta)
        print("-----------------")

    # 4. LIMPIEZA
    mi_servidor.desconectar()
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()