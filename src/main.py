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
    from docker_manager import DockerManager 
except ImportError as e:
    print(f"❌ Error crítico importando módulos: {e}")
    sys.exit(1)

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
    print("🤖 Inicializando AutoLab v2.2 (Docker Edition)...")

    load_dotenv()
    host = os.getenv("SSH_HOST")
    user = os.getenv("SSH_USER")
    password = os.getenv("SSH_PASS")
    
    # 1. Chequeo de configuración
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

        # Si por algún motivo se perdió la conexión en el bucle anterior (reconect fallida)
        if mi_servidor is None:
            print("⚠️ No hay conexión activa. Por favor, selecciona la opción de reconectar o salir.")
            estado_conn = "DESCONECTADO"
        else:
            estado_conn = f"{user}@{host}"

        # --- CABECERA DE ESTADO ---
        print("\n" + "="*50)
        print(f"   🟢 CONECTADO A: {estado_conn}")
        print("="*50)

        print("\n--- MENÚ DE CONTROL ---")
        print("1. Ejecutar comando manual")
        print("2. 🔄 Actualizar sistema")
        print("3. 🌐 Instalar Servidor Web (Apache + PHP)")
        print("4. 🐳 Gestión de Contenedores (Docker) [NUEVO]")
        print("5. 🔌 Cambiar de Equipo (Reconectar)")
        print("6. Salir")
        print("-" * 50)
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1" and mi_servidor:
            cmd = input("Comando > ")
            resultado = mi_servidor.ejecutar_comando(cmd)
            print("\n--- RESULTADO ---")
            print(resultado)
            input("\nPress Enter para continuar...") 

        elif opcion == "2" and mi_servidor:
            actualizador.actualizar_todo()
            input("\nPress Enter para continuar...")
            
        elif opcion == "3" and mi_servidor:
            instalador_web.instalar_stack_lamp()
            input("\nPress Enter para continuar...")
        
        elif opcion == "4" and mi_servidor:
            docker_mgr = DockerManager(mi_servidor, password)
            
            # Sub-bucle para el menú de Docker
            while True:
                limpiar_pantalla()
                print("\n🐳 --- GESTIÓN DOCKER ---")
                
                # Comprobación rápida de estado
                instalado = docker_mgr.comprobar_docker()
                estado = "✅ INSTALADO" if instalado else "❌ NO INSTALADO"
                print(f"Estado: {estado}\n")
                
                print("1. 🛠️  Instalar Docker Engine")
                print("2. 📋 Listar Contenedores")
                print("3. 🚀 Desplegar Nginx (Test Web)")
                print("4. 🔙 Volver al menú principal")
                print("-" * 30)
                
                sub_opcion = input("Docker > ")
                
                if sub_opcion == "1":
                    if not instalado:
                        docker_mgr.instalar_docker()
                    else:
                        print("ℹ️  Docker ya está instalado.")
                    input("Enter para continuar...")
                    
                elif sub_opcion == "2":
                    if instalado:
                        docker_mgr.listar_contenedores()
                    else:
                        print("⚠️  Necesitas instalar Docker primero.")
                    input("Enter para continuar...")
                    
                elif sub_opcion == "3":
                    if instalado:
                        docker_mgr.desplegar_nginx()
                    else:
                        print("⚠️  Necesitas instalar Docker primero.")
                    input("Enter para continuar...")
                    
                elif sub_opcion == "4":
                    break # Rompe el while del submenú y vuelve al principal
        
        elif opcion == "5":
            print("\n🔄 Cerrando conexión actual...")
            if mi_servidor:
                mi_servidor.desconectar()
            
            # Pedimos nuevos datos
            host, user, password = solicitar_datos()
            
            # Reconectamos y regeneramos las herramientas
            mi_servidor, actualizador, instalador_web = conectar_y_preparar(host, user, password)
            
            if mi_servidor is None:
                print("⚠️ La reconexión falló.")
                input("Enter para continuar...")

        elif opcion == "6":
            break
        else:
            print("⚠️ Opción no válida o sin conexión.")
            time.sleep(1)

    if mi_servidor:
        mi_servidor.desconectar()
    print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupción de usuario. Cerrando...")
        sys.exit()