import socket
import sys
import random
import time
from functools import *

def checksum(data):
	"""
	Calculating checksum of a packet

	param data: data in packet
	"""
	return reduce(lambda x,y:x+y, map(ord, data)) % 256

def packet(data):
	"""
	Creating a packet containing data and checksum

	param data: data in packet
	"""
	pkt = data + str(checksum(data[:len(data)-1]))
	pkt = pkt.encode()
	return pkt

def corrupt(data, i):
	"""
	Creating a corrupt packet with real checksum

	param data: Original data
	param i : sequence no. of packet
	"""
	pkt = '0xf456#%d\n'%i + str(checksum(data[:len(data)-1]))
	pkt = pkt.encode()
	return pkt

def pack(i):
	"""
	Create and send packets and receive ACK

	param i: Sequence number of packet
	"""
	x = random.randint(1, 10)
	y = random.randint(0, 7)
	z = random.randint(1, 10)
	if (x < 6):                     #60% packets sent correctly
		time.sleep(y)               #delay
		print('Sending packet', i)
		sock.settimeout(None)
		sock.send(packet('Packet %d\n'%i))
		sock.settimeout(5)
		try:
			if(z > 8):                       #20% ACK lost
				raise Exception('ACK lost')
			data = sock.recv(100)
			val = data.decode().split('\n')[0]
			print(val,'\n')
			if int(val[4:]) != i:   #send packet again if received incorrect ACK
				pack(i)
			pack((i+1))       #send next packet after receiving ACK
		except:
			print('Timeout')       #in case of timeout send the packet again
			pack(i)
		
	else:                            #40% packets are corrupted
		print('Sending packet', i)
		sock.send(corrupt('Packet %d\n'%i, i))
		sock.settimeout(5)
		try:
			data = sock.recv(100)
			val = data.decode().split('\n')[0]
			print(val, '\n')
			if int(val[4:]) != i:    #in case of timeout send the packet again
				pack(i)
			pack((i+1))        #send next packet after receiving ACK
		except:
			print('Timeout')      #in case of timeout send the packet again
			pack(i)	



if len(sys.argv) < 3:
	print('Usage: python3 rdt_sender.py <hostname> <portnumber>')  #print usage format
	exit()		
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #creating a socket object
sock.connect((sys.argv[1], int(sys.argv[2])))
pack(0)



	