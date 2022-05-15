import socket
import threading as thr
import time

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

