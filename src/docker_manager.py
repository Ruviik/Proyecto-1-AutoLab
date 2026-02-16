import time

class DockerManager:
    def __init__(self, ssh_client, password):
        self.ssh = ssh_client
        self.password = password

    def comprobar_docker(self):
        """Verifica si Docker ya está instalado y corriendo."""
        print("🐳 Comprobando estado de Docker...")
        resultado = self.ssh.ejecutar_comando("docker --version")
        if "Docker version" in resultado:
            return True
        return False

    def instalar_docker(self):
        """Instala Docker automáticamente según la distro."""
        print("\n🛠️  --- INICIANDO INSTALACIÓN DE DOCKER ---")
        datos_os = self.ssh.ejecutar_comando("cat /etc/os-release").lower()
        
        cmds = []
        if "ubuntu" in datos_os or "debian" in datos_os:
            cmds = [
                ("📦 Actualizando repositorios...", f"echo {self.password} | sudo -S apt update"),
                ("🐳 Instalando Docker.io...", f"echo {self.password} | sudo -S apt install -y docker.io"),
                ("🔌 Habilitando servicio...", f"echo {self.password} | sudo -S systemctl enable --now docker")
            ]
        elif "rhel" in datos_os or "centos" in datos_os or "rocky" in datos_os:
            cmds = [
                ("📦 Instalando utilidades...", f"echo {self.password} | sudo -S dnf install -y yum-utils"),
                ("🐳 Instalando Docker...", f"echo {self.password} | sudo -S dnf install -y docker"),
                ("🔌 Habilitando servicio...", f"echo {self.password} | sudo -S systemctl enable --now docker")
            ]
        
        for mensaje, comando in cmds:
            print(mensaje)
            self.ssh.ejecutar_comando(comando)
            time.sleep(1)

        # Añadir usuario al grupo docker para evitar usar sudo en el futuro
        self.ssh.ejecutar_comando(f"echo {self.password} | sudo -S usermod -aG docker {self.ssh.user}")
        print("✅ Instalación finalizada.")

    # --- NUEVAS FUNCIONES ---

    def listar_contenedores(self):
        """Muestra qué contenedores están corriendo."""
        print("\n📋 --- CONTENEDORES ACTIVOS ---")
        # Usamos 'sudo' por seguridad si el grupo docker aún no refrescó permisos
        cmd = f"echo {self.password} | sudo -S docker ps -a --format 'table {{{{.ID}}}}\t{{{{.Image}}}}\t{{{{.Status}}}}\t{{{{.Names}}}}'"
        resultado = self.ssh.ejecutar_comando(cmd)
        print(resultado)

    def desplegar_nginx(self):
        """Lanza un contenedor Nginx en el puerto 8080."""
        print("\n🚀 Desplegando servidor Nginx (Puerto 8080)...")
        
        # 1. Limpieza previa (borrar si ya existe para evitar error de nombre duplicado)
        print("🧹 Limpiando contenedores antiguos...")
        self.ssh.ejecutar_comando(f"echo {self.password} | sudo -S docker rm -f autolab-nginx")
        
        # 2. Ejecutar
        # -d: Detached (segundo plano)
        # -p 8080:80 -> Puerto 8080 del host al 80 del contenedor
        # --name: Nombre para identificarlo fácil
        cmd = f"echo {self.password} | sudo -S docker run -d -p 8080:80 --name autolab-nginx nginx"
        
        resultado = self.ssh.ejecutar_comando(cmd)
        
        if "Error" not in resultado:
            print("✅ ¡Contenedor desplegado con éxito!")
            print(f"🌍 Accede vía web en: http://{self.ssh.ip}:8080")
        else:
            print(f"❌ Error al desplegar: {resultado}")