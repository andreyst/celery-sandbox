==Main
1. Install docker
3. Configure same backend in celery-sandbox.py, docker-compose.yml
2. Launch backend and workers with `docker-compose up -d`
4. Open flower UI at localhost:5555
5. Run celery shell with `docker-compose run celery-worker bash`
6. Execute main.py in celery shell to run a task
7. View stats in flower UI
8. Scale worker containers with `docker-compose up  --scale celery-worker=2 -d`

Extra: run load test with `load-test.py` from inside celery shell.
Extra: follow worker logs with `docker-compose logs --follow celery-worker`
Extra: change backends to amqp/redis/sqs in `celery_sandbox.py` (don't forget to change flower backend also!)

==Redis fanout issue
Redis fanout does not work as expected: https://github.com/celery/celery/issues/5261
Minimal reproduce of this issue is in files `main_min.py`, `tasks_min.py`
