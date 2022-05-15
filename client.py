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
