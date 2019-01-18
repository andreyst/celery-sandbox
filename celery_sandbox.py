from celery import Celery
import datetime
import time
import redis
import settings
from kombu.common import Broadcast

broker_endpoint = 'amqp://{}:{}/'.format(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT)
# broker_endpoint = 'redis://{}:{}/{}'.format(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DATABASE)
# broker_endpoint = 'sqs://{}:{}/'.format(settings.SQS_HOST, settings.SQS_PORT)

app = Celery('hello', broker=broker_endpoint)
app.conf.broker_transport_options = {'fanout_prefix': True}
app.conf.broker_transport_options = {'fanout_patterns': True}

# app.conf.task_queues = (Broadcast('broadcast_tasks'),)
# app.conf.task_routes = {
#     'celery_sandbbox.allhi': {
#         'queue': 'broadcast_tasks',
#         'exchange': 'broadcast_tasks'
#     }
# }

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DATABASE)

@app.task
def allhi():
    print('all hi! ' + datetime.datetime.now().isoformat())
    return 'all hi! ' + datetime.datetime.now().isoformat()

@app.task
def hello():
    return 'hello world ' + datetime.datetime.now().isoformat()

@app.task
def add(x, y):
    return x + y

@app.task
def work(test_id, start_time):
    receive_time = time.time()
    elapsed_time = receive_time - start_time
    # print(elapsed_time)
    if elapsed_time <= 0.001:
      bucket = "1"
    elif elapsed_time <= 0.005:
      bucket = "5"
    elif elapsed_time <= 0.01:
      bucket = "10"
    elif elapsed_time <= 0.02:
      bucket = "20"
    elif elapsed_time <= 0.03:
      bucket = "30"
    elif elapsed_time <= 0.04:
      bucket = "40"
    elif elapsed_time <= 0.05:
      bucket = "50"
    elif elapsed_time <= 0.1:
      bucket = "100"
    elif elapsed_time <= 0.2:
      bucket = "200"
    elif elapsed_time <= 0.5:
      bucket = "500"
    elif elapsed_time <= 1:
      bucket = "1000"
    elif elapsed_time <= 2:
      bucket = "2000"
    elif elapsed_time <= 2:
      bucket = "2000"
    else:
      bucket = "inf"
    label = "ts_" + str(int(receive_time)) + "_" + bucket
    r.lpush("celery_load_test_" + str(test_id), elapsed_time)
    # r.incr(label)
    # print()