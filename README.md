set up virtual environment

pip install flask
pip install flask-sqlalchemy
pip install flask-wtf

pip freeze > requirements.txt

mkdir app
mkdir app/static
mkdir app/templates

do stuff in app/__init__.py

do stuff in app/views.py

create run.py script in root (chmod a+x run.py if needed)