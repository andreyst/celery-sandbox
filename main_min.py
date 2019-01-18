# Minimal reproduce for redis fanount issue
from tasks_min import allhi

allhi.apply_async([], queue='broadcast_tasks')
print("Sent broadcast task")
