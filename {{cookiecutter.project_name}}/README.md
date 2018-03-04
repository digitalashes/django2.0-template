## 1. Install requirements

Local requirements:

    pip install -r requirements/local.txt

Production requirements:

    pip install -r requirements/production.txt

## 2. Django Management commands

* ``./manage.py migrate``
* ``./manage.py createsuperuser``

{%- if cookiecutter.use_celery == "y" %}
## 3. Celery worker:

* ``celery worker -A project.apps.taskapp -E -l INFO -Q high -n high``
* ``celery worker -A project.apps.taskapp -E -l INFO -Q normal -n normal``
* ``celery worker -A project.apps.taskapp -E -l INFO -Q low -n low``

## 4. Celery beat:

* ``celery beat -A project.apps.taskapp -l INFO``

## 5. Flower:

* ``sudo rabbitmq-plugins enable rabbitmq_management``
* ``sudo service rabbitmq-server restart``

    Execute the lines above only once time.
* ``celery flower -A project.apps.taskapp --address=0.0.0.0 --port=5555 --broker_api=http://guest:guest@localhost:15672/api/ --basic_auth=foo:bar``
{%- endif %}
