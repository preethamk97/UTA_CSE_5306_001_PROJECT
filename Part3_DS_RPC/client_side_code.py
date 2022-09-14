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

def compute_asynchronous_reuest():
	print("\n[ASYNC OPTIONS]\n[*] Enter 1 For Addition\n[*] Enter 2 For Sorting")
	choice = int(input("[*] Enter Your choice: "))
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	multicall = xmlrpc.client.MultiCall(proxy_server)
	if (choice == 1):
		a = int(input("[*] Enter a Number to add : "))
		b = int(input("[*] Enter a Number to add : "))
		result =  multicall.synchronous_add(a, b)
		#print("[*] Adding the result moving ahead with other operation at client side")
		#print("[*] Result : ", result)

	elif (choice == 2):
		num_elem  = int(input("[*] Enter the number of elements: "))
		list_to_sort =  []
		for x in range(num_elem):
			param = int(input("[*] Enter the number: "))
			list_to_sort.append(param)

		result = multicall.synchronous_sort(list_to_sort)
		#print("[*] Below is the Sorted Array")
		#for x in range(num_elem):
		#	print (result[x])
	
	result_mc = multicall()
	print("[*] Result: ",tuple(result_mc)[0])




def compute_synchronous_reuest():
	print("\n[SYNC OPTIONS]\n[*] Enter 1 For Addition\n[*] Enter 2 For Sorting")
	choice = int(input("[*] Enter Your choice: "))
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	if (choice == 1):
		a = int(input("[*] Enter a Number to add : "))
		b = int(input("[*] Enter a Number to add : "))
		result = proxy_server.synchronous_add(a, b)
		print("[*] Result : ", result)

	if (choice == 2) :
		num_elem  = int(input("[*] Enter the number of elements: "))
		list_to_sort =  []
		for x in range(num_elem):
			param = int(input("[*] Enter the number: "))
			list_to_sort.append(param)
		result = proxy_server.synchronous_sort(list_to_sort)
		print("[*] Sorted List: ", list_to_sort)

def send_request_to_server():

	print("\n[OPTIONS] \n[*] Enter 1 For Synchronous Computation\n[*] Enter 2 For Asynchronous Computation")

	choice = int(input("[*] Enter Your choice: "))
	if (choice == 1):
		compute_synchronous_reuest()

	elif (choice == 2):
		compute_asynchronous_reuest()

if __name__ == "__main__":
	print("\n*** Executing the program at the client side ***\n")
	send_request_to_server()
