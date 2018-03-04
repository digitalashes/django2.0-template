from celery import Celery

from config import settings

app = Celery(main='Isis')
app.config_from_object(settings.CeleryConfig)
app.autodiscover_tasks(lambda: settings.LOCAL_APPS, force=True)
