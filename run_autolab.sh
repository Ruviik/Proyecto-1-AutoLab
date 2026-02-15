#!/bin/bash

# Definir colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}     🚀 INICIANDO AUTOLAB v2.0 (Linux)${NC}"
echo -e "${BLUE}==========================================${NC}"

# 1. Comprobar si existe Python3
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}❌ Error Crítico: Python3 no está instalado.${NC}"
    echo "Por favor, instálalo con: sudo apt install python3"
    exit 1
fi

# 2. Comprobar/Crear Entorno Virtual (CON AUTO-REPARACIÓN)
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creando entorno virtual (venv)...${NC}"
    
    # Intentamos crear el entorno
    python3 -m venv venv 2> /dev/null
    
    # Si falla ($? es el código de salida del último comando, 0=éxito, !=0=error)
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Falta el módulo 'python3-venv'.${NC}"
        
        # Comprobamos si estamos en un sistema con APT (Debian/Ubuntu/Mint)
        if command -v apt &> /dev/null; then
            echo -e "${YELLOW}🔧 Intentando instalar dependencias automáticamente...${NC}"
            echo -e "${BLUE}🔐 Introduzca su contraseña de usuario para instalar el paquete:${NC}"
            
            # Ejecutamos la instalación
            sudo apt update && sudo apt install -y python3-venv
            
            # Si la instalación fue bien, reintentamos crear el venv
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Dependencia instalada. Reintentando...${NC}"
                python3 -m venv venv
            else
                echo -e "${RED}❌ Falló la instalación automática.${NC}"
                exit 1
            fi
        else
            echo -e "${RED}❌ No se pudo instalar automáticamente (no se detectó 'apt').${NC}"
            echo "Instala manualmente 'python3-venv' en tu distribución."
            exit 1
        fi
    fi
fi

# 3. Activar y verificar dependencias
echo -e "${BLUE}🔌 Activando entorno...${NC}"
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}⬇️  Verificando librerías...${NC}"
    # Pip install suele ser silencioso, pero mostramos errores si los hay
    pip install -r requirements.txt > /dev/null
else
    echo -e "${YELLOW}⚠️  No se encontró requirements.txt${NC}"
fi

# 4. Detectar sistema para limpiar pantalla y Lanzar
echo -e "${GREEN}✅ Todo listo. Ejecutando AutoLab...${NC}"
echo ""

# Ejecutamos el script principal
python3 src/main.py

# 5. Desactivar al salir
deactivate