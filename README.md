# Grupo-R-BD2-1C2026

# Setear y correr el proyecto 

## Requisitos

- Python 3.12
- Extension de python: Python (para ejecutar proyectos de python de forma simple)
- MongoDB

## Clonar 

- ```git clone https://github.com/elidev72/Grupo-R-BD2-1C2026.git```
- crear entorno virtual (linea de comando)
    - Windows
        - crear entorno usando: ```python -m venv .venv```
        - activar entorno usando (usando powershell): ```.venv\Scripts\activate``` 
        - Nota: Asegurate de poder ejecutar scripts en powershell, sino usa el comando ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser``` (Creo que es temporal, si cerras la terminal lo tenes que volver a ejecutar)
- instalar dependencias con ```pip install -r requirements.txt```
- Crear .env con las variables ```MONGO_DB_NAME```, ```MONGO_HOST```, ```MONGO_PORT```. Si usan     autentificacion agreguen las variables de entorno correspondientes.
    - Busquen que va en cada variable (yo use lo por defecto para mongo, test, localhost, 27017)   
- Ejecutar desde main

     