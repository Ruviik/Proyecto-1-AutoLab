import time

class SystemUpdater:
    """
    Clase especialista en mantenimiento del sistema.
    Recibe un cliente SSH ya conectado y le ordena tareas de actualización.
    """
    
    def __init__(self, ssh_client, sudo_password):
        self.ssh = ssh_client
        self.sudo_pass = sudo_password
        self.manager = None # 'apt' o 'dnf'
    
    def detectar_sistema(self):
        """Detecta si el sistema usa APT (Debian) o DNF/YUM (RHEL)."""
        print("🕵️  Analizando sistema operativo remoto...")
        
        # Probamos si existe el archivo de configuración de release
        # Usamos 'cat' para leerlo y ver qué ID tiene
        datos_os = self.ssh.ejecutar_comando("cat /etc/os-release")
        
        if "ID=ubuntu" in datos_os or "ID=debian" in datos_os or "ID_LIKE=debian" in datos_os:
            self.manager = "apt"
            print("🐧 Sistema detectado: Familia DEBIAN/UBUNTU (usando apt)")
        elif "ID=rhel" in datos_os or "ID=fedora" in datos_os or "ID=\"centos\"" in datos_os or "ID=\"rocky\"" in datos_os:
            self.manager = "dnf"
            print("🎩 Sistema detectado: Familia RHEL/FEDORA (usando dnf)")
        else:
            # Fallback básico: preguntar al sistema qué binario tiene
            check_apt = self.ssh.ejecutar_comando("which apt")
            if "/bin/apt" in check_apt:
                self.manager = "apt"
            else:
                self.manager = "dnf" # Asumimos dnf por defecto si no es apt
                print("⚠️  No se identificó la distro exacta, probaremos con DNF.")

    def actualizar_todo(self):
        print("\n🛡️ --- INICIANDO PROTOCOLO DE ACTUALIZACIÓN ---")
        
        # 1. Detectar sistema si no se ha hecho aún
        if not self.manager:
            self.detectar_sistema()

        # 2. Construir comandos según el gestor
        cmds = []
        
        if self.manager == "apt":
            # Comandos para Debian/Ubuntu
            cmds = [
                ("⏳ Actualizando lista de paquetes (APT)...", 
                f"echo {self.sudo_pass} | sudo -S apt update"),
                
                ("📦 Instalando actualizaciones...", 
                f"echo {self.sudo_pass} | sudo -S apt upgrade -y"),
                
                ("🧹 Limpiando paquetes obsoletos...", 
                f"echo {self.sudo_pass} | sudo -S apt autoremove -y")
            ]
            
        elif self.manager == "dnf":
            # Comandos para RHEL/CentOS/Fedora
            # En DNF, 'update' hace todo (refrescar e instalar)
            cmds = [
                ("⏳📦 Buscando e instalando actualizaciones (DNF)...", 
                f"echo {self.sudo_pass} | sudo -S dnf update -y"),
                
                ("🧹 Limpiando caché y paquetes huerfanos...", 
                f"echo {self.sudo_pass} | sudo -S dnf autoremove -y")
            ]

        # 3. Ejecución del bucle de comandos
        for mensaje, comando in cmds:
            print(mensaje)
            resultado = self.ssh.ejecutar_comando(comando)
            
            # Análisis básico de errores
            if "error" in resultado.lower() and "sudo" not in resultado:
                print(f"⚠️  Posible error detectado:\n{resultado}")
            
            time.sleep(1) # Pequeña pausa para no saturar

        print("✅ Sistema actualizado correctamente.")