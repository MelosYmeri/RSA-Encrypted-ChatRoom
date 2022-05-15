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