from celery import Celery

app = Celery('demo')
app.config_from_object('workers.celeryconfig')
