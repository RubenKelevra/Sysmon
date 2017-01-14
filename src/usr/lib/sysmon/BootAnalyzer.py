#!/usr/bin/env python3

from sys import exit as sys_exit
from MultiQueue import MultiQueue

from dbus import SystemBus, SessionBus, Interface

class BootAnalyzer:
	def __init__(self, send_queue):
		assert isinstance(send_queue, MultiQueue)
		self.send_queue = send_queue
		self.bus = SystemBus()
		self.systemd = self.bus.get_object('org.freedesktop.systemd1',
                        '/org/freedesktop/systemd1')
		self.manager = Interface(self.systemd, dbus_interface='org.freedesktop.systemd1.Manager')


	def __push(self, data, prio):
		self.send_queue.put_element(data, prio)

	def analyze(self):
		for e in self.manager.ListUnits():
			if len(e) != 10:
				continue

			name = str(e[0])
			description = str(e[1])
			load_state = str(e[2])
			active_state = str(e[3])
			sub_state = str(e[4])
			followed_unit = str(e[5])
			unit_object_path = str(e[6])
			queued_job_id = int(e[7])
			job_type = str(e[8])
			job_object_path = str(e[9])

			if not name.endswith('.service'):
				continue
			if name.startswith('user@'):
				continue
			if active_state == ACTIVE:
				continue
			if active_state == INACTIVE and sub_state == DEAD:
				continue
			print(e[0])
if __name__ == '__main__':
	sys_exit(0)