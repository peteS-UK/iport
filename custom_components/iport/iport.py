import logging

import socket

import asyncio_datagram


import sys

_LOGGER = logging.getLogger(__name__)


class IPORT(object):
    def __init__(self, ip, name):
        self._ip = ip
        self._name = name
        self._port = 10001
        self._port_name = []
        self.state = False

    @classmethod
    def discover(cls):
        # No IP specified, so try discovery
        _LOGGER.debug("Discovery Started")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            sock.settimeout(2.0)
            sock.sendto(b"\x00\x01\x00\xf6", ("255.255.255.255", 30718))
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        except (socket.error, socket.timeout):
            _LOGGER.debug("Discovery Failure.")
            sock.close()
            return None
        else:
            _LOGGER.debug("Broadcast Response: %s", data)
            iPortIp = str(addr[0])
            _LOGGER.debug("Discovered iPort IP: %s", iPortIp)
        finally:
            sock.close()

        return iPortIp

    async def async_udp_connect(self):
        try:
            self._udp_stream = await asyncio_datagram.connect((self._ip, self._port))

        except IOError as e:
            _LOGGER.critical(
                "Cannot connect command socket %d: %s", e.errno, e.strerror
            )
        except Exception:
            _LOGGER.critical(
                "Unknown error on command socket connection %s", sys.exc_info()[0]
            )

    async def async_udp_disconnect(self):
        try:
            self._udp_stream.close()
        except IOError as e:
            _LOGGER.critical(
                "Cannot disconnect from command socket %d: %s", e.errno, e.strerror
            )
        except Exception:
            _LOGGER.critical(
                "Unknown error on command socket disconnection %s", sys.exc_info()[0]
            )

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

    async def async_send_command(self, command, port_number, value=None):
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

        _command = _command + "\r\n"

        try:
            await self._udp_stream.send(_command.encode())
        except Exception:
            try:
                _LOGGER.error("Connection lost.  Attepting to reconnect")
                await self.async_udp_connect()
                await self._udp_stream.send(command)

            except IOError as e:
                _LOGGER.critical(
                    "Cannot reconnect to command socket %d: %s", e.errno, e.strerror
                )
            except Exception:
                _LOGGER.critical(
                    "Unknown error on command socket reconnection %s", sys.exc_info()[0]
                )
