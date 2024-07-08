# PlanificadorDocker
## Importante:
Debido a las librerias del programa este solo puede ser ejecutado en windows


# link video Drive

link : https://drive.google.com/file/d/17QZIcBc7RI2wYHqz1RszkPL1D0tDjR9B/view?usp=drive_link

## integrantes 

Alejandro Muñoz Guerrero 2242951

Bayron Jojoa R 2242917

## intrucciones Ejecucion

### Base de datos 

se corre el siguiente comando, la contraseña debe coincidir con el archivo base.py en modelito, en nuestro caso es pescado:

    docker run -e POSTGRES_PASSWORD=pescado -p 5432:5432 postgres

### Planificador de contenedores

se hace el git clone a este repositorio, se inicia un entrono virtual, se activa el entrono  y se instalan los requerimientos

instrucciones para windows:

    git clone https://github.com/BayronJDv/PlanificadorDocker.git

    python -m venv venv 

    venv\Scripts\Activate.ps1

    pip install -r requirements.txt

Finalmente se puede iniciar la aplicacion ejecutando main.py 

    python main.py 
