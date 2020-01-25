import sys, traceback
import socket
import pickle
import os
import random
import copy
import pandas as pd
import re
import copy
import threading as th
from Interface import Interface as Interface
from CodeGenClient import CodeGenClient as CodeGenClient

debug = False

def main(client_IP,client_port,server_IP,server_port):
	
	conn = None
	try:
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.bind((client_IP, client_port))
		conn.connect((server_IP, server_port))
	except:
		print("Failed to connect with Server")
		exit()

	cg = CodeGenClient(conn)

	while True:
		cmd = str(input("Enter your command: ")).lower()
		cmd_param = re.split("\s",cmd)
		cmd_name = cmd_param[0]

		cg.set_function_name(cmd_name)
		
		if cmd_name == "get_items_list":
			result = cg.interface.get_items_list()
			try:
				if result == -1:
					print("Invalid arguments")
					continue
			except:
				continue		
			for item, value in result.items():
				print(item," : ",value)

		elif cmd_name == "buy":
			result = cg.interface.buy(args=cmd_param[1])
			if result==0:
				print("Item Unavailable")
			if result == -1:
				print("Invalid arguments")

		elif cmd_name == "help":
			print("Command list\n1.get_items_list\n2.buy [product_name]")

		else:
			print("Invalid Command")
		
			
if __name__ == '__main__':

	if len(sys.argv) != 5:
		print("Invalid Input Format\n python3 [FileName][Client IP][Client Port][Server IP][Server Port]")
		exit()

	client_IP = str(sys.argv[1])
	client_port = int(sys.argv[2])
	server_IP = str(sys.argv[3])
	server_port = int(sys.argv[4])
	main(client_IP,client_port,server_IP,server_port)