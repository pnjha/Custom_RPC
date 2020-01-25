import random
import copy
import pandas as pd
import sys, traceback
import socket
import pickle
import os
import threading as th
import Interface as Interface
from Server import Server as Server

debug = False

def send_to_client(conn,msg):
    m = pickle.dumps(msg)
    conn.send(m)

def receive_from_client(conn):
    received_msg = conn.recv(2048)
    if received_msg:
        received_obj = pickle.loads(received_msg)
        return received_obj
    return None

def close_connection(conn):
    conn.close()

def process_client(conn, client_addr, server_ip):

    client_IP = client_addr[0]
    client_port = client_addr[1]
    reply = {}
    request = {}

    server_impl_obj = Server()

    while True:
        request = receive_from_client(conn)
        function_name = getattr(server_impl_obj, request["type"])
        print(request["param_value"])
        val = function_name(**request["param_value"])

        print("No of Argument of Function")
        print(function_name.__code__.co_argcount-1)

        print("No of Argument as an Input")
        print(len(request["param_value"].keys()))


        if function_name.__code__.co_argcount-1 != len(request["param_value"].keys()):
            reply["response_value"] = "Issue Encountered while Calling Function"
            reply["status"] = 1
            send_to_client(conn,reply)
            server_impl_obj = None
            continue

        reply["response_value"] = val
        reply["status"] = 1
        send_to_client(conn,reply)

def main(server_IP,server_port):
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print("Error creating the socket")

    try:
        server.bind((server_IP, server_port))
        server.listen(15)
    except:
        print("Error binding to IP and port")
    while True:
        conn, client_addr = server.accept()
        print("Connection accepted for client: ", client_addr)
        th.Thread(target=process_client, args=(conn, client_addr, server_IP)).start()

    server.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Invalid argument format\n Correct usage:python3 [filename][IP Address][Port Number]")
        exit()
    server_IP = str(sys.argv[1])
    server_port = int(sys.argv[2])

    main(server_IP,server_port)
    
