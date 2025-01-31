# Deteccion de somnolencia:
Este repositorio se basa en la realización de ingeniería inversa de sistema de deteccion de somnolencia en tiempo real, basado en el repositorio publico de (https://github.com/AprendeIngenia/driver_fatigue_detection)

## Características:
- **Procesamiento en tiempo real:** Utiliza Mediapipe para detectar puntos clave faciales.
- **Interfaz gráfica:** Desarrollada con Flet para mostrar los resultados de la detección.
- **Dockerizable:** Facilita la ejecución en servidores remotos.
- **API robusta:** Utiliza FastAPI para ofrecer un backend modular y extensible.

## Requisitos:
- Sistema operativo: Windows, Linux o macOS
- Versión de Python: 3.10 o superior
- Version CUDA: 11.7
- Paquetes adicionales: NumPy, OpenCV, Flet, etc. Consultar el archivo [requirements.txt] del código
- Docker
- 
## Instalación

#### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:

#### 2. Crear y activar entorno virtual
```bash
python -m venv venv
```

Activar venv en Windows
```bash
./venv/Scripts/activate
```

Activar venv en Linux
```bash
source venv/bin/acitvate
```

#### 3. Instalar dependencias 
```bash
pip install -r requirements.txt
```

#### 4. Ejecutar el servidor
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### 5. Ejecutar interfaz grafica
```bash
flet main.py
```

## Dockerizacion
#### 1. Construir la imagen Docker
```bash
docker build -t drowsiness-server .
```

#### 2. Ejecutar el contenedor:
```bash
docker run -d -p 8000:8000 --name drowsiness-server drowsiness-server
```
Ó
```bash
docker start drowsiness-server
```


#### 3. Ejecutar interfaz grafica
```bash
flet main.py
``` 

#### 4. Detener el contenedor
```bash
docker stop drowsiness-server
``` 

#### 5. Revisar estado del contenedor
```bash
docker ps -a
```
