import paramiko
import re  

class SSHClient:
    """
    Gestiona la conexión SSH y la ejecución de comandos.
    Es el 'mando a distancia' universal para cualquier servidor.
    """

    def __init__(self, ip, usuario, password):
        """
        Constructor: Se ejecuta AUTOMÁTICAMENTE al crear un objeto.
        Aquí guardamos los datos de identidad de ESTA conexión específica.
        """
        self.ip = ip        
        self.user = usuario
        self.password = password
        self.client = None 

    def conectar(self):
        """Establece el túnel SSH"""
        print(f"🔌 Conectando a {self.ip}...")
        try:
            # 1. Crear el objeto paramiko (la herramienta)
            self.client = paramiko.SSHClient()
            # 2. Configurar la política de 'confiar en todos'
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 3. Llamar (usando los datos guardados en 'self')
            self.client.connect(self.ip, username=self.user, password=self.password)
            return True
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            self.client = None # Marcamos que no hay conexión válida
            return False
        
    def desconectar(self):
        if self.client:
            self.client.close()
            self.client = None

    def ejecutar_comando(self, comando):
        if not self.client:
            return "❌ No hay conexión establecida."

        # --- LÓGICA DE SEGURIDAD AVANZADA (REGEX) ---
        # Usamos expresiones regulares para sustituir TODAS las apariciones de
        # "echo loquesea | sudo -S" por "echo [PASSWORD OCULTA] | sudo -S"
        # Esto funciona incluso si hay varios comandos encadenados con &&
        log_comando = re.sub(r"echo .*? \| sudo -S", "echo [PASSWORD OCULTA] | sudo -S", comando)
        
        print(f"🚀 Ejecutando: {log_comando}")
        # -------------------------------------------

        try:
            stdin, stdout, stderr = self.client.exec_command(comando)
            # sudo -S necesita la contraseña por stdin a veces, pero con el truco del 'echo'
            # suele bastar. Sin embargo, paramiko a veces necesita vaciar buffers.
            
            salida = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                # Filtramos mensajes técnicos comunes que no son errores reales
                if "Warning" in error or "password" in error:
                    pass 
                print(f"⚠️  El comando generó un error/aviso: {error}")
            
            return salida

        except Exception as e:
            return f"❌ Error ejecutando comando: {e}"