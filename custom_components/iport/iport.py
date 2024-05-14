
import logging

import socket

from lxml import etree

import asyncio

import asyncio_datagram

import time

import sys

_LOGGER = logging.getLogger(__name__)

class IPORT(object):
	def __init__(self, ip, name):

		self._ip = ip
		self._name = name
		self._port = 10001
		self._port_name = []
		self.state = False

	async def async_udp_connect(self):
		try:
			self._udp_stream = await asyncio_datagram.connect((self._ip, self._port))

		except IOError as e:
			_LOGGER.critical("Cannot connect command socket %d: %s", e.errno, e.strerror)
		except:
			_LOGGER.critical("Unknown error on command socket connection %s", sys.exc_info()[0])

	async def async_udp_disconnect(self):

		try:
			self._udp_stream.close()
		except IOError as e:
			_LOGGER.critical("Cannot disconnect from command socket %d: %s", e.errno, e.strerror)
		except:
			_LOGGER.critical("Unknown error on command socket disconnection %s", sys.exc_info()[0])

	async def async_turn_on(self, port_number):
		_LOGGER.debug("Turn On area_%d", port_number)
		command = "Area On"
		await self.async_send_command(command, port_number)

	async def async_turn_off(self, port_number):
		_LOGGER.debug("Turn Off area_%d", port_number)
		command = "Area Off"
		await self.async_send_command(command, port_number)

	async def async_update(self, port_number):
		_LOGGER.debug("Calling update for area_%d", port_number)


	async def async_send_command(self, command, port_number, value = None):

		match command:
			case "Area On":
				_command = "area_on " + str(port_number)
				_LOGGER.debug("Area On for %d", port_number)
				self.state = True
			case "Area Off":
				_command = "area_off " + str(port_number)
				_LOGGER.debug("Area Off for %d", port_number)
				self.state = False
			case "All On":
				_command = "all_on"
			case "All Off":
				_command = "all_off"
			case "Intensity":
				_command = "inten_" + str(port_number) + "_" + value
			case "Colour":
				_command = "colour_" + str(port_number) + "_" + value
			case "Start Show":
				_command = "start_show"
			case "All Off":
				_command = "stop_show"

		_command = _command+"\r\n"

		try: 
			await self._udp_stream.send(_command.encode())
		except:
			try:
				_LOGGER.debug("Connection lost.  Attepting to reconnect")
				self.async_udp_connect()
				await self._udp_stream.send(command)

			except IOError as e:
				_LOGGER.critical("Cannot reconnect to command socket %d: %s", e.errno, e.strerror)
			except:
				_LOGGER.critical("Unknown error on command socket reconnection %s", sys.exc_info()[0])
