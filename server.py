import socket
import threading as thr
import time

#local host
#host = 'server.srikar.tech' # Ndrysho hostin
host = '192.168.178.34'
port = 55543
print(host,port)
header_Size = 10
publicKeys = []
# internet, TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# lidhja e serverit me local host
server.bind((host, port))
# kërkon klientët
server.listen()
names = []
clients = []

def broadcast(message):
	for client in clients:
		client.send(message) # Dërgon një mesazh për të gjithë

def handle(client):
	while True:
		try:
			message = client.recv(256) # 1024 bytes
			broadcast(message)
			broadcast(b'')
			#print(publicKeys)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			key = publicKeys[index]
			publicKeys.remove(key)

			left_Message = f"{name} u largua nga biseda!"
			extra = 256 - len(left_Message)
			broadcast_msg = left_Message + extra*'x'
			broadcast(broadcast_msg.encode('ISO-8859-1'))
			names.remove(name)
			break

