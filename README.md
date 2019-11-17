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

## Como crear ramas y desarrollar en ellas

Para empezar, diferenciaremos las ramas master, develop y las features.

Cuando alguien quiere crear una funcionalidad, debera crear una rama llamada feature/"nombre de departamento"/"nombre de la funcionalidad"

Los departamentos son: "design", "deveploment" y "analysis".

Es decir, tendremos nombre de ramas con estas caracteristicas:

feature/design/"nombre de la funcionalidad"

feature/deveploment/"nombre de la funcionalidad"

feature/analysis/"nombre de la funcionalidad"

Para crear una nueva rama, se deberá hacer:
git checkout -b "feature/design/'nombre de la funcionalidad'"

Una vez desarrollada la funcionalidad y los respectivos "git add ." y
"git commit -m 'titulo descriptivo'", se deberá hacer:
git push origin "feature/design/'nombre de la funcionalidad'"

Posteriormente, debera avisar al coordinador de su grupo para que revise su codificación y si es apta, el coordinador
de cada departamento, deberá hacer un merge de esa rama en develop.

Por ultimo, cuando se quiera desplegar los cambios, se hara merge en master y por ultimo, se despliega a heroku.

## Despligue en heroku

Una vez que los cambios deseados esten en master, se debera ejecutar el comando 
" git push heroku master ".

Si no se tiene agendado el dominio heroku, se deberá usar el comando 
" git remote add heroku https://git.heroku.com/pinfvot.git "

Por otra parte, si se ve que los modelos no se actualizan en el servidor,
ejecutar los dos comandos siguientes:

heroku run python manage.py makemigrations
heroku run python manage.py migrate

Para hacer esto, el usuario ha de tener el heroku-cli instalado y configurado
en su equipo.

Para instalar y configurar el heroku-cli, leasé https://devcenter.heroku.com/articles/heroku-cli