import socket
import threading as thr
import PySimpleGUI as sg
import rsa
from rsa import PublicKey

HOST = '127.0.0.1' # Ndrysho hostin
PORT = 55543
publicKey, privateKey = rsa.newkeys(2048)
publicKeys = []
caesar_Key = 69
header_Size = 10

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

			else:
				if message != b'':
					if message == b'Lidhja me serverin eshte kryer me sukses!':
						print(decoded_Msg)
					elif 'U largua nga biseda!' in decoded_Msg:
						message = decoded_Msg.split('U largua nga biseda!')[0] + 'U largua nga biseda.'
						print(message)
					elif 'Ju bashkua bisedes!' in decoded_Msg:
						message = decoded_Msg.split('Ju bashkua bisedes!')[0] + 'Ju bashkua bisedes!'
						print(message)
					else:
						try:
							decMessage = rsa.decrypt(message, privateKey).decode()
							# decMessage = caesar_Decrypt(decMessage, int(turn_pub_key_to_string(publicKey).decode('ISO-8859-1')[caesar_Key]))
							print(decMessage)
							
						except Exception as e:
							#print(e)
							pass
		except Exception as e:
			print(e)
			print("Ka ndodhur një gabim!")
			client.close()
			break

receive_thread = thr.Thread(target = receive)

sg.theme('Black')   # Shtoni ngjyrat

# Të gjitha gjërat brenda dritares.
layout = [  [sg.Text('Mesazhi juaj:'), sg.InputText(key = "Input")],
            [sg.Button('Dërgo', key = "Dërgo"), sg.Button('Cancel')], 
			[sg.Button('Shfaq mesazhin e enkriptuar', key = "Shfaq_mesazhin_e_enkriptuar")]]

# Krijo dritaren
window = sg.Window('ChatRoom', layout, return_keyboard_events=True, use_default_focus=True)

sg.Print('Chat Room duke u ngarkuar ....', do_not_reroute_stdout=False)

printf = sg.Print

printf('Ju keni hyrë në ChatRoom.')
receive_thread.start()
# Event loop për të përpunuar "ngjarjet" dhe për të marrë "vlerat" e inputeve
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # Nëse përdoruesi mbyll dritaren ose klikon cancel
		break
	if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
		elem = window.FindElementWithFocus()
		if elem is not None and elem.Type == sg.ELEM_TYPE_BUTTON:
			window.Element("Dërgo").Click()
	elif event == 'Dërgo':
		message = f"{name}: {values['Input']}"
		if values["Input"] != "":
			for key in publicKeys:
				encMessage = rsa.encrypt(message.encode('ISO-8859-1'), assemble_pub_key_from_string(key))
				client.send(encMessage)
			window["Input"].Update('')
	elif event == "Shfaq_mesazhin_e_enkriptuar":
		message = f"{name}: {values['Input']}"
		if values["Input"] != "":
			xy = rsa.encrypt(message.encode('ISO-8859-1'), publicKey)
			print(f"Your Encrypted Message: {xy.decode('ISO-8859-1')}")
			
			for key in publicKeys:
				encMessage = rsa.encrypt(message.encode('ISO-8859-1'), assemble_pub_key_from_string(key))
				client.send(encMessage)
			window["Input"].Update('')
window.close()
client.close()
           