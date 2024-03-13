from celery import Celery

def make_celery(app_name=__name__):
    # Updated to use RabbitMQ as the broker
    return Celery(
        app_name,
        broker='amqp://guest:guest@localhost:5672/',
        backend='redis://localhost:6379/0',  # Keeping Redis as backend for results
    )

celery = make_celery('armada')
