# SenUCA
WebAPP in Python-Django. Trabajo para la asignatura de PINF (Proyectos Informáticos) 2019-2020 Grupo 1.

## Deployment

Instalar virtualenv para python3
```bash
sudo apt-get install python3-venv
```

Iniciar un entorno virtual
```bash
python3 -m venv env
```

Clonar el repositorio 
```bash
git clone URLGit
```

Activar el entorno virtual
```bash
source env/bin/activate
```

Instalar requirements.txt
```bash
cd SenUCA/
pip install -r requirements.txt
```

Realizar migraciones
```bash
./python manage.py migrate --run-syncdb
```

Lanzar servidor
```bash
./manage.py runserver
```

## Instrucciones básicas

**Nunca se trabaja en master, siempre en develop.**

Para cada issue **creamos una feature dentro de develop donde trabajaremos.** Ejemplo: feature/texto_descriptivo. 
