import socket
import random
import time
from functools import *


def checksum(data):
	"""
	Calculating checksum of a packet

	param data: data in packet
	"""
	return reduce(lambda x,y:x+y, map(ord, data)) % 256

def isCorrupt(data):
	"""
	Checking if a packet is corrupt by calculating and 
	comparing with its checksum
	"""
	val = data.split('\n')
	if (checksum(val[0]) == int(val[1])):
		return False
	return True

port = 100       # port           
s = socket.socket() #creating a socket object            
							   
s.bind(('localhost', port))  #binding the receiver to local machine       
s.listen()  
conn, addr = s.accept()
print ('Got connection from', addr)
m = ''
while True:
	x = random.randint(0, 7)
	y = random.randint(1, 10)
	conn.settimeout(5)
	try:
		if (y > 8):                      #20% packets lost
			raise Exception("Packet lost")
		data = conn.recv(512)
		conn.settimeout(None)
		val = data.decode()
		s = val.split('\n')[0]
		if isCorrupt(val):
			print('Packet %d is corrupted'%int(s[s.find('#')+1:]))     #in case packet is corrupted start the timer again
			continue
		if m == int(s[7:]):
			print('Duplicate', s, '\n', end = '')                #Handling duplicate packets
		else:	 
			print(s,'\n', end='')
		m = int(s[7:])	
		time.sleep(x)                                         #delay
		print('Sending ACK for Packet %d'%int(s[7:]))        #send ACK if packet received correctly
		conn.send(b'ACK %d\n'%int(s[7:]))
		m = int (s[7:])
	except:
		print('Timeout')                                     #incase of timeout start the timer again
		continue	                                       
    



