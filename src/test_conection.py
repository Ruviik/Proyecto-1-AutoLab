import paramiko
import time

HOSTNAME =  '192.168.56.10'
PORT = 22
USERNAME = 'NOMBRE_USUARIO'
PASSWORD = 'CONTRASEÑA'

def probar_conexion():
    print(f"Intenando conectar a {HOSTNAME}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
        print("¡Conexión exitosa!")

        comando = "hostname"
        print(f"Ejecutando comando remoto: {comando}")

        stdin, stdout, stderr = client.exec_command(comando)
        resultado = stdout.read().decode().strip()

        print(f"La maquina virtual responde: {resultado}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    probar_conexion()
