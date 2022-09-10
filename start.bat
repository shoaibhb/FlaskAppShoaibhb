cd C:\Users\297554\PycharmProjects\project\
python -m venv project_env
CALL project_env\Scripts\activate
set FLASK_APP=__init__.py
set FLASK_DEBUG=1
flask run --host=0.0.0.0