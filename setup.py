#!/usr/bin/env python
from scheduler import Task, TaskGroup

tasks = TaskGroup()
tasks.add_task(Task("test 1", "9:44 AM", "CALL my_proc_1()"))
tasks.add_task(Task("test 2", "2:30 PM", "CALL my_proc_2()"))
tasks.save_tasks("data/tasks.json")

# show the contents of the task json file created by the above
with open('data/tasks.json', 'r') as f:
	for line in f:
		print line,
