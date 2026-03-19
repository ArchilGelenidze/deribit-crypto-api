from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    main="deribit_worker",
    broker=settings.redis_url
)

celery_app.conf.update(
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(["app.tasks"])


celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "update_crypto_prices_task",
        "schedule": crontab(minute="*")
    }
}