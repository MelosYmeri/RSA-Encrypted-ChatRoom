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
				
def recieve():	
	while True:	
		client, address = server.accept()	
		print(f"I lidhur me {str(address)}")	
		client.send(('NAME' + str(252*'x')).encode('ISO-8859-1'))	
		try:	
			name = client.recv(1024).decode('ISO-8859-1')	
			names.append(name)	
		except:	
			pass	
		clients.append(client)	
		client.send(('COLLECT_KEY' + 245*'x').encode('ISO-8859-1'))	
		key = client.recv(623)	
		key = key.decode('ISO-8859-1') + "420420420696969"	
		if key.encode('ISO-8859-1') not in publicKeys:	
			publicKeys.append(key.encode('ISO-8859-1'))	
		for pk in publicKeys:	
			broadcast(('RECEIVE_KEY' + (245*'x')).encode('ISO-8859-1'))
            #print(pk)
			time.sleep(0.5)
			broadcast(pk)
			time.sleep(0.5)

		print(f"emri i klientit është {name}!")
		broadcast_msg = f"{name} iu bashkua bisedës!"
		extra = 256 - len(broadcast_msg)
		broadcast_msg = broadcast_msg + extra*'x'
		time.sleep(1)
		
		broadcast(broadcast_msg.encode('ISO-8859-1'))
		
		thread = thr.Thread(target = handle, args = (client,))
		thread.start()

print("Serveri po funksionon")
recieve()
