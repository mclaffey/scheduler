#!/usr/bin/env python

import scheduler

tasks = scheduler.TaskGroup()
tasks.load_tasks("data/tasks.json")
tasks.check_and_run()
