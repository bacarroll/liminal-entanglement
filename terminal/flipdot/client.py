#! /usr/bin/env python
#
# client.py -- client driver for Flipdot display
# supports both a UDP simulator, as well as a serial
# connected device

import socket

import serial

CHAN_UDP, CHAN_SERIAL = range(2)


class Client(object):

    def format_message(self, screen_id, data, refresh):
        dl = len(data)
        if dl == 112:
            msg = 0x82 if refresh else 0x81
        elif dl == 28:
            msg = 0x83 if refresh else 0x84
        elif dl == 56:
            msg = 0x85 if refresh else 0x86
        return bytearray([0x80, msg, screen_id]) + data + bytearray([0x8F])

    def open(self):
        raise NotImplemented

    def close(self):
        raise NotImplemented

    def send(self, screen_id, data, refresh=True):
        raise NotImplemented


class UDPClient(Client):
    def __init__(self, host, port):
        self.addr = (host, port)
        self.kind = CHAN_UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def open(self):
        self.sock.connect(self.addr)

    def close(self):
        self.sock.close()

    def send(self, screen_id, data, refresh=True):
        b = self.format_message(screen_id, data, refresh)
        self.sock.sendall(b)


class SerialClient(Client):
    def __init__(self, port):
        self.kind = CHAN_SERIAL
        self.chan = serial.Serial()
        self.chan.baudrate = 57600
        self.chan.port = port

    def open(self):
        self.chan.open()

    def close(self):
        self.chan.close()

    def send(self, screen_id, data, refresh=True):
        b = self.format_message(screen_id, data, refresh)
        self.chan.write(b)
