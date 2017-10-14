import datetime
import json
import os


class TaskGroup(object):
	"""A collection of tasks that can be saved and checked as a group
	"""
	def __init__(self):
		self.tasks = []

	def add_task(self, task):
		self.tasks.append(task)

	def save_tasks(self, json_path):
		"""Write each task to a json properties file
		"""
		list_of_task_dicts = [t.to_dict() for t in self.tasks]
		with open(json_path, 'w') as f:
			json.dump(list_of_task_dicts, f,
				sort_keys=True, indent=4, separators=(',', ': ')) # pretty-print

	def load_tasks(self, json_path):
		"""Add tasks from a json property file
		"""
		with open(json_path, 'r') as f:
			list_of_task_dicts = json.load(f)
		for d in list_of_task_dicts:
			task = Task.from_dict(d)
			self.tasks.append(task)

	def check_and_run(self):
		"""Check and run each tasks
		"""
		if not self.tasks:
			print "No tasks"
		else:
			for t in self.tasks:
				t.check_and_run()

class Task(object):
	"""SQL code with an assigned run time, and the ability to check if the task should be run
	"""
	def __init__(self, name, time, sql):
		self._time = None
		self._time_str = None

		self.name = name
		self.time = time
		self.sql = sql

		self._history_path = "./data/{}.txt".format(self.name)
		self._history = []


	@property
	def time(self):
		"""The time property is the string that the user submitted.
		"""
		return self._time_str

	@time.setter
	def time(self, time_str):
		"""When setting the time string, we also parse the string to a datetime.time
		"""
		self._time_str = time_str
		self._time = datetime.datetime.strptime(time_str, "%I:%M %p").time()

	def to_dict(self):
		return dict(
			name = self.name,
			time = self._time_str,
			sql = self.sql,
			)

	@classmethod
	def from_dict(klas, d):
		return klas(**d)

	def check_and_run(self):
		self.load_history()
		todays_runs = [run[0] for run in self._history if run[0].date() == datetime.datetime.today().date()]
		if todays_runs:
			print "{:20s} - last ran today at {}".format(self.name, max(todays_runs))
		else:
			if datetime.datetime.today().time() > self._time:
				print "{:20s} - Due at {}, running now".format(self.name, self.time)
				self.run()
			else:
				print "{:20s} - Due at {}, not yet time".format(self.name, self.time)

	def run(self):
		print "  Executing {}".format(self.sql)
		self.append_history()

	def load_history(self):
		if not os.path.exists(self._history_path):
			return
		with open(self._history_path, 'r') as f:
			for line in f:
				time_str, status =  line.split(",")
				time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
				self._history.append((time, status))

	def append_history(self):
		time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open(self._history_path, 'a+') as f:
			f.write("{},ok\n".format(time_str))



