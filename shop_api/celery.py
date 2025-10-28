import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'cleanup-expired-sessions-every-sunday': {
        'task': 'users.tasks.cleanup_expired_sessions',
        'schedule': crontab(day_of_week=0, hour=2, minute=0), 
        'args': (1000,), 
    },

    'send-weekly-report-every-hour': {
        'task': 'users.tasks.send_weekly_report',
        'schedule': timedelta(hours=1),
        'args': ('superman@dailyplanet.com', 'WeeklyReport'),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')