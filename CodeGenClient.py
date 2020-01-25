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

class CodeGenClient:

	def __init__(self,conn):
		self.conn = conn
		self.function_name = None
		self.interface = Interface()
		l = dir(self.interface)
		for i in reversed(l):
			if "__" in i:
				break
			setattr(self.interface, i, self.call_server)	

	def call_server(self,**args):
		request = {}
		request["type"] = str(self.function_name)
		request["param_value"] = args
		self.send_to_server(request)
		reply = self.receive_from_server()

		if reply["status"] == 1:
			return reply["response_value"]

	def set_function_name(self,name):
		self.function_name = name

	def send_to_server(self,msg):
	    m = pickle.dumps(msg)
	    self.conn.send(m)

	def receive_from_server(self):
	    received_msg = self.conn.recv(4096)
	    if received_msg:
	        received_obj = pickle.loads(received_msg)  
	        return received_obj
	    return None

	def close_connection(self):
	    request={}
	    request["type"] = "quit"
	    self.send_to_server(request)
	    self.conn.close()