# 🏥 Backend MEDAPP

Backend FastAPI para aplicación médica.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- Git

### Instalación y Ejecución

#### 🚀 Opción 1: Setup Automático
```powershell
# Windows (PowerShell)
.\setup.ps1
```

```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh
```

#### 🔧 Opción 2: Setup Manual
```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd Backend-MEDAPP

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
# En Windows (CMD):
.venv\Scripts\activate.bat
# En Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install fastapi uvicorn motor python-dotenv python-multipart

# 5. Ejecutar servidor
# En Windows:
npm run dev
# En Linux/Mac:
npm run dev:unix
# o alternativamente:
# Windows: .\run-dev.ps1
# Linux/Mac: ./run-dev.sh
```

### Opción rápida por plataforma
```powershell
# Windows (PowerShell)
npm run dev
# o
.\run-dev.ps1

# Para setup automático en una nueva máquina:
.\setup.ps1
```

```bash
# Linux/Mac
npm run dev:unix
# o
chmod +x run-dev.sh
./run-dev.sh
```

## 🌐 URLs

Una vez ejecutando:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
