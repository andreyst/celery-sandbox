# Minimal reproduce for redis fanount issue
from celery import Celery
from kombu.common import Broadcast

REDIS_HOST="10.0.1.36"
REDIS_PORT=6379
REDIS_DATABASE=0
RABBITMQ_HOST="10.0.1.36"
RABBITMQ_PORT=5672

broker_endpoint = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DATABASE)
# Works fine with RabbitMQ broker with no other changes
# broker_endpoint = 'amqp://{}:{}/'.format(RABBITMQ_HOST, RABBITMQ_PORT)

app = Celery('hello', broker=broker_endpoint)
app.conf.broker_transport_options = {'fanout_prefix': True}
app.conf.broker_transport_options = {'fanout_patterns': True}

app.conf.task_queues = (Broadcast('broadcast_tasks'),)
app.conf.task_routes = {
    'tasks_min.allhi': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks'
    }
}

@app.task
def allhi():
    print('all hi!')
