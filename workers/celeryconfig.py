from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'workers.tasks'
)

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'workers.tasks.getKeywords',
         'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
         #'args': (5, 8)                           # 任务函数参数
    }
   # 'multiply-at-some-time': {
   #     'task': 'periodtasks.task2.multiply',
   #     'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
   #     'args': (3, 7)                            # 任务函数参数
   # }
}
