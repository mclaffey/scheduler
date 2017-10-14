from __init__ import TaskGroup

tasks = TaskGroup()
tasks.load_tasks("data/tasks.json")
tasks.check_and_run()
