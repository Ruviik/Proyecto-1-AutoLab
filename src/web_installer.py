class WebInstaller:
    """
    Especialista en desplegar servicios web (Apache).
    """
    
    def __init__(self, ssh_client, sudo_password):
        self.ssh = ssh_client
        self.sudo_pass = sudo_password

    def instalar_stack_lamp(self):
        print("\n🌐 --- INICIANDO DESPLIEGUE DE STACK LAMP (Apache + PHP) ---")
        
        pasos = [
            ("Instalando Apache, PHP y módulos...", "apt install apache2 php libapache2-mod-php php-mysql -y"),
            
            ("Iniciando servicio Apache...", "systemctl start apache2"),
            ("Habilitando inicio automático...", "systemctl enable apache2"),
            
            ("Abriendo puertos del Firewall...", "ufw allow 'Apache'")
        ]

        for descripcion, comando in pasos:
            print(f"🔨 {descripcion}")
            cmd_sudo = f"echo {self.sudo_pass} | sudo -S {comando}"
            self.ssh.ejecutar_comando(cmd_sudo)

        print("📝 Generando archivo de prueba (info.php)...")
        comando_php = "echo '<?php phpinfo(); ?>' | sudo -S tee /var/www/html/info.php"
        cmd_final = f"echo {self.sudo_pass} | sudo -S sh -c \"echo '<?php phpinfo(); ?>' > /var/www/html/info.php\""
        self.ssh.ejecutar_comando(cmd_final)

        print("🔄 Reiniciando Apache para aplicar cambios...")
        self.ssh.ejecutar_comando(f"echo {self.sudo_pass} | sudo -S systemctl restart apache2")

        # Verificación final
        print("🔍 Verificando estado del servicio...")
        estado = self.ssh.ejecutar_comando("systemctl is-active apache2")
        
        if estado == "active":
            print("✅ ¡ÉXITO! Apache está corriendo y activo.")
            return True
        else:
            print(f"⚠️ Alerta: El estado de Apache es '{estado}'. Revisa los logs.")
            return False