import time

class WebInstaller:
    """
    Especialista en desplegar servicios web (Apache).
    """
    
    def __init__(self, ssh_client, sudo_password):
        self.ssh = ssh_client
        self.sudo = sudo_password
        self.pkg_manager = None  # apt o dnf
        self.service_name = None # apache2 o httpd
        self.firewall_type = None # ufw o firewalld
    
    def detectar_distro(self):
        """Detecta la distribución y configura los nombres de paquetes."""
        print("🕵️  Detectando entorno para instalación Web...")
        datos_os = self.ssh.ejecutar_comando("cat /etc/os-release").lower()

        if "ubuntu" in datos_os or "debian" in datos_os:
            print("🐧 Detectado: Familia DEBIAN (Apache2)")
            self.pkg_manager = "apt"
            self.service_name = "apache2"
            self.firewall_type = "ufw"
            return True
            
        elif "rhel" in datos_os or "centos" in datos_os or "fedora" in datos_os or "rocky" in datos_os:
            print("🎩 Detectado: Familia RHEL (Httpd)")
            self.pkg_manager = "dnf"
            self.service_name = "httpd"
            self.firewall_type = "firewalld"
            return True
            
        else:
            print("❌ No reconozco esta distribución. No puedo instalar automáticamente.")
            return False

    def instalar_stack_lamp(self):
        # 1. Detectar antes de empezar
        if not self.detectar_distro():
            return

        print(f"\n🌐 --- INSTALANDO SERVIDOR WEB ({self.service_name}) ---")
        
        cmds = []

        # --- CONFIGURACIÓN DE COMANDOS SEGÚN DISTRO ---
        if self.pkg_manager == "apt":
            # UBUNTU/DEBIAN
            cmds = [
                ("📦 Instalando Apache y PHP...", 
                f"echo {self.sudo} | sudo -S apt install -y apache2 php libapache2-mod-php"),
                
                ("🔥 Configurando Firewall (UFW)...", 
                f"echo {self.sudo} | sudo -S ufw allow 'Apache'"),
                
                ("🚀 Iniciando Servicio...", 
                f"echo {self.sudo} | sudo -S systemctl enable apache2 && echo {self.sudo} | sudo -S systemctl start apache2")
            ]

        elif self.pkg_manager == "dnf":
            # RHEL/CENTOS/FEDORA
            cmds = [
                ("📦 Instalando Httpd y PHP...", 
                f"echo {self.sudo} | sudo -S dnf install -y httpd php"),
                
                ("🔥 Configurando Firewall (FirewallD)...", 
                f"echo {self.sudo} | sudo -S firewall-cmd --permanent --add-service=http && echo {self.sudo} | sudo -S firewall-cmd --reload"),
                
                ("🚀 Iniciando Servicio...", 
                f"echo {self.sudo} | sudo -S systemctl enable httpd && echo {self.sudo} | sudo -S systemctl start httpd")
            ]

        # --- EJECUCIÓN ---
        for mensaje, comando in cmds:
            print(mensaje)
            resultado = self.ssh.ejecutar_comando(comando)
            
            # Chequeo rápido de errores
            if "error" in resultado.lower() and "sudo" not in resultado:
                print(f"⚠️  Aviso: {resultado}")
            
            time.sleep(1)

        # --- PASO FINAL: CREAR PÁGINA DE PRUEBA ---
        print("📝 Creando página de prueba (info.php)...")
        cmd_test = f"echo '<?php phpinfo(); ?>' | sudo tee /var/www/html/info.php"
        # Usamos tee porque redireccionar con > a veces falla con sudo
        self.ssh.ejecutar_comando(f"echo {self.sudo} | sudo -S sh -c \"{cmd_test}\"")

        print(f"\n✅ ¡Instalación completada!")
        print(f"🌍 Abre en tu navegador: http://{self.ssh.ip}/info.php")