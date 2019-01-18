import celery_sandbox
from celery_sandbox import add, hello, work, allhi
import time
import redis
import settings
import math
import sys

ITERATIONS = 10000

def percentile(N, percent):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return N[int(k)]
    d0 = N[int(f)] * (c-k)
    d1 = N[int(c)] * (k-f)
    return d0+d1

# hello.delay()
# celery_sandbox.allhi.apply_async([], exchange='broadcast_tasks')
# sys.exit(1)

# hello.delay()
# add.delay(1,2)
test_id = int(time.time())
for i in range(ITERATIONS):
  work.delay(test_id, time.time())

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DATABASE)
label = "celery_load_test_" + str(test_id)
while r.llen(label) < ITERATIONS:
  time.sleep(0.5)

lst = r.lrange(label, 0, ITERATIONS)
lst = sorted([float(val) for val in lst])
print("p1:   {}".format(percentile(lst, 0.01)))
print("p50:  {}".format(percentile(lst, 0.5)))
print("p90:  {}".format(percentile(lst, 0.9)))
print("p95:  {}".format(percentile(lst, 0.95)))
print("p99:  {}".format(percentile(lst, 0.99)))
print("p100: {}".format(percentile(lst, 1)))
r.delete(label)