#!/usr/bin/env python3

from queue import PriorityQueue
from sys import exit as sys_exit
from time import sleep

from MasterSlaveLock import MasterSlaveLock


class MultiQueue:
	def __init__(self):
		self.__queue_lock = MasterSlaveLock()
		self.__queue_lock.acquire_master()
		self.__queues = {}
		self.__queue_lock.release_master()

	def add_queue_if_not_exist(self, identifier):
		"""appends one queue to array, which gets all elements put

		"""
		self.__queue_lock.acquire_master()
		if not self.queue_exist(identifier):
			self.__queues[identifier] = PriorityQueue()
		self.__queue_lock.release_master()

	def queue_exist(self, identifier) -> bool:
		self.__queue_lock.acquire_slave()
		returnval = identifier in self.__queues
		self.__queue_lock.release_slave()
		return returnval

	def remove_queue(self, identifier):
		self.__queue_lock.acquire_master()
		try:
			del self.__queues[identifier]
		finally:
			self.__queue_lock.release_master()

	def pop_element(self, identifier):
		"""returns data from one queue

		:param identifier: select the queue
		:return: data
		"""
		self.__queue_lock.acquire_slave()
		try:
			returnval = self.__queues[identifier].get()
		finally:
			self.__queue_lock.release_slave()

		return returnval

	def put_element(self, data, prio=5):
		"""puts an element to all queues

		:param prio: between 0 and 10, while 0 is the highest
		:type prio: int
		"""
		if not (0 <= prio <= 10):
			raise ValueError

		self.__queue_lock.acquire_slave()
		while len(self.__queues) == 0:
			self.__queue_lock.release_slave()
			sleep(1)  # wait for worker queues
			self.__queue_lock.acquire_slave()

		for identifier in self.__queues:
			self.__queues[identifier].put(prio, data)
		self.__queue_lock.release_slave()


if __name__ == '__main__':
	sys_exit(0)
