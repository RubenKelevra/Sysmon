#!/usr/bin/env python3

from sys import exit as sys_exit
from threading import Lock, Condition


class MasterSlaveLock:
	def __init__(self):
		self.__master_lock = Lock()
		self.__slave_locks_counter_condition = Condition()

		self.__slave_locks_count = 0

	def acquire_master(self):
		self.__master_lock.acquire()

		# wait for all slavelocks to unlock
		self.__slave_locks_counter_condition.acquire()
		while self.__slave_locks_count != 0:
			self.__slave_locks_counter_condition.wait()
		self.__slave_locks_counter_condition.release()

	def release_master(self):
		self.__master_lock.release()

	def acquire_slave(self):
		# stop further slave locks here, when master-process is waiting for a full stop of slave processes
		self.__master_lock.acquire()
		self.__master_lock.release()

		self.__slave_locks_counter_condition.acquire()
		self.__slave_locks_count += 1
		self.__slave_locks_counter_condition.release()

	def release_slave(self):
		self.__slave_locks_counter_condition.acquire()
		self.__slave_locks_count -= 1
		if not self.__slave_locks_count:  # we released the last lock, notify (maybe) waiting master-process
			self.__slave_locks_counter_condition.notify()
		self.__slave_locks_counter_condition.release()


if __name__ == '__main__':
	sys_exit(0)
