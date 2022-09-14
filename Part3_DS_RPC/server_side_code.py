"""
* DS CSE-5306-001 Project 1
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import os
import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

def synchronous_sort(list_to_sort):
	print("[*] Sorting compute done at Server")
	return sorted(list_to_sort)

def synchronous_add(a, b):
	print ("[*] Addition compute done at Server")
	return (a+b)
	
if __name__ == "__main__":
	print("\n*** Executing the program at the SERVER side ***\n")
	print("[***] Server Listening....")
	server = SimpleXMLRPCServer(('localhost', 9000))
	server.register_function(synchronous_add, 'synchronous_add')
	server.register_function(synchronous_sort, 'synchronous_sort')
	server.register_multicall_functions()
	server.serve_forever()

