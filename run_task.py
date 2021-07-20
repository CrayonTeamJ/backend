import tasks

for i in range(10, 100):
	tasks.slow_task.delay(i)

tasks.quick_task.delay(100)