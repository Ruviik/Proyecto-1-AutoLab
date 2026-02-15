import paramiko

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
        self.client = None # Aún no tenemos conexión real, solo los datos.

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

        log_comando = comando
        if "echo" in comando and "sudo -S" in comando:
            # Dividimos el comando por la tubería '|'
            partes = comando.split('|')
            if len(partes) > 1:
                # Reconstruimos solo la parte derecha (el comando real)
                # Ejemplo visual: "🚀 Ejecutando: [SUDO] sudo -S apt update"
                log_comando = f"[PASSWORD OCULTA] | {partes[1].strip()}"
        
        print(f"🚀 Ejecutando: {log_comando}")
        # -------------------------------------------

        try:
            stdin, stdout, stderr = self.client.exec_command(comando)
            # sudo -S necesita la contraseña por stdin a veces, pero con el truco del 'echo'
            # suele bastar. Sin embargo, paramiko a veces necesita vaciar buffers.
            
            salida = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                # Algunos comandos tiran warnings por stderr (como apt), no siempre es fallo crítico
                print(f"⚠️  El comando generó un error/aviso: {error}")
            
            return salida

        except Exception as e:
            return f"❌ Error ejecutando comando: {e}"