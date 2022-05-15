import socket
import threading as thr
import PySimpleGUI as sg
import rsa
from rsa import PublicKey

def turn_pub_key_to_string(pub_key):
	a = str(pub_key['n'])
	b = str(pub_key['e'])
	return (a + ',' + b).encode('ISO-8859-1')

def assemble_pub_key_from_string(pub_key):
	k = list(pub_key.decode('ISO-8859-1').split(','))
	pub_key = PublicKey(int(k[0]),int(k[1]))
	return pub_key

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'


name = input("Zgjidhni një emër: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
def has_alpha(s):
	for character in s:
		if character.isalpha():
			return True
	return False
	
def receive():	
	while True:	
		try:	
			message = client.recv(256)	
			decoded_Msg = message.decode('ISO-8859-1')	
			if 'NAME' in decoded_Msg:	
				client.send(name.encode('ISO-8859-1'))	
				print('Lidhja me serverin eshte kryer me sukses!')	
				pass	
			elif 'COLLECT_KEY' in decoded_Msg:	
				client.send(turn_pub_key_to_string(publicKey))	
			elif 'RECEIVE_KEY' in decoded_Msg:	
				msg = client.recv(638)	
				decoded_Msg = msg.decode('ISO-8859-1')	
				if decoded_Msg[-15:] == "420420420696969" and not has_alpha(decoded_Msg):	
					msg = decoded_Msg[:-15]	
					if msg.encode('ISO-8859-1') not in publicKeys:	
						publicKeys.append(msg.encode('ISO-8859-1'))
