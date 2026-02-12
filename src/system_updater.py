class SystemUpdater:
    """
    Clase especialista en mantenimiento del sistema.
    Recibe un cliente SSH ya conectado y le ordena tareas de actualización.
    """
    
    def __init__(self, ssh_client, sudo_password):
        self.ssh = ssh_client
        self.sudo_pass = sudo_password

    def actualizar_todo(self):
        print("\n🛡️ --- INICIANDO PROTOCOLO DE ACTUALIZACIÓN ---")
        
        # Lista de comandos a ejecutar en cadena
        # El '-y' es vital: le dice a Linux "Sí a todo" para que no pregunte.
        tareas = [
            ("Actualizando lista de paquetes...", "apt update"),
            ("Instalando actualizaciones...", "apt upgrade -y"),
            ("Limpiando paquetes obsoletos...", "apt autoremove -y")
        ]

        for descripcion, comando_linux in tareas:
            print(f"⏳ {descripcion}")
            
            # TRUCO DEL ALMENDRUCO:
            # "echo pass | sudo -S comando"
            # Esto inyecta la contraseña automáticamente.
            comando_final = f"echo {self.sudo_pass} | sudo -S {comando_linux}"
            
            respuesta = self.ssh.ejecutar_comando(comando_final)
            
            # Opcional: Mostrar respuesta si quieres ver el log completo
            # print(respuesta) 
            
            print("✅ Hecho.")

        print("✨ Sistema actualizado y limpio.")