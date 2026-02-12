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
            print(f"✅ Conectado exitosamente a {self.ip}")
            
        except Exception as e:
            print(f"❌ Error al conectar a {self.ip}: {e}")
            self.client = None # Marcamos que no hay conexión válida

    def ejecutar_comando(self, comando):
        """Envía una orden y devuelve la respuesta limpia"""
        if self.client is None:
            print("⚠️ No estás conectado. Usa .conectar() primero.")
            return None

        print(f"🚀 Ejecutando: {comando}")
        # Enviamos el comando y capturamos las 3 tuberías
        stdin, stdout, stderr = self.client.exec_command(comando)
        
        # Leemos la respuesta y el error
        respuesta = stdout.read().decode().strip()
        errores = stderr.read().decode().strip()

        if errores:
            print(f"⚠️ El comando generó un error/aviso: {errores}")
        
        return respuesta

    def desconectar(self):
        """Cierra la conexión para liberar recursos"""
        if self.client:
            self.client.close()
            print(f"🔒 Conexión con {self.ip} cerrada.")