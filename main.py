import celery_sandbox
from celery_sandbox import add, hello, work, allhi
import time
import redis
import settings
import math
import sys

hello.delay()
