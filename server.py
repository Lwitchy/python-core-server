import logging
import socket
import time
import os
from threading import *

from Logic.Device import Device
from Logic.Player import Player
from Packets.PacketManager import packets

def _(*args):
	for arg in args:
		print(arg, end=' ')
	print()


class Server:
	Clients = {"ClientCounts": 0, "Clients": {}}
	ThreadCount = 0

	def __init__(self, ip: str, port: int):
		self.server = socket.socket()
		self.port = port
		self.ip = ip

	def start(self):


		self.server.bind((self.ip, self.port))
		_(f'[SERVER]: Server Started Listening: {self.ip}')
		while True:
			self.server.listen()
			client, address = self.server.accept()
			_(f'[SERVER]: New Connection: {address[0]}')
			ClientThread(client, address).start()
			Server.ThreadCount += 1


class ClientThread(Thread):
	def __init__(self, client, address):
		super().__init__()
		self.client = client
		self.address = address
		self.device = Device(self.client)
		self.player = Player()

	def recvall(self, length: int):
		data = b''
		while len(data) < length:
			s = self.client.recv(length)
			if not s:
				print("didn't recieved idk why WTF?!?")
				break
			data += s
		return data

	def run(self):
		last_packet = time.time()
		try:
			while True:
				header = self.client.recv(7)
				if len(header) > 0:
					last_packet = time.time()
					packet_id = int.from_bytes(header[:2], 'big')
					length = int.from_bytes(header[2:5], 'big')
					data = self.recvall(length)

					if packet_id in packets:
						_(f'Received packet! Id: {packet_id}')
						message = packets[packet_id](self.client, self.player, data)
						message.decode()
						message.process()

						if packet_id == 10101:
							Server.Clients["Clients"][str(self.player.low_id)] = {"SocketInfo": self.client}
							Server.Clients["ClientCounts"] = Server.ThreadCount
							self.player.ClientDict = Server.Clients

					else:
						_(f'[SERVER] Packet ID:{packet_id}')

				if time.time() - last_packet > 10:
					print(f"[SERVER]: {self.address[0]} disconnected!")
					self.client.close()
					break
		except ConnectionAbortedError or ConnectionResetError or TimeoutError:
			print(f"[SERVER]: {self.address[0]} disconnected!")
			self.client.close()

print("""                                        
Core Server By Lwitchy#1935                                                           
""")
if __name__ == '__main__':
	server = Server('0.0.0.0', 9339)
	server.start()
