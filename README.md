# 🏥 Backend MEDAPP

Backend FastAPI para aplicación médica.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- Git
- Mongosh
- Cuenta MongoDB Atlas

### Instalación y Ejecución de Backend


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
### Creacion de Base de Datos
Para crear la base de datos, es necesario tener una cuenta de MongoDB Atlas y base de datos en la nube. 

En .env introduce URI de base de datos en nube.
```
# Base de datos
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=medapp_db
```
Descarga librerias necesarias
```
  pip install -r requirements.txt
```
Ejecuta Script de Inicializacion de Base de Datos
```
python init_db.py
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
- **API**: http://localhost:5000
- **Documentación**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health

