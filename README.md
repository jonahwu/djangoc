


## start web server

```
python manage.py runserver 0.0.0.0:8000
```


## Enableing the worker

```
celery -A workers.tasks worker --loglevel=INFO
```

## Execute Periodic task

```
celery -A workers worker --beat --loglevel=INFO
```
