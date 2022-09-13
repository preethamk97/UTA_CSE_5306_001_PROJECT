"""
* DS CSE-5306-001 Project 1
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import os
import threading
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

SERVER_FOLDER               = "/"           #default host folder is /

def delete_file_from_server_end(file_name,file_data,return_value_to_the_client):
	file_name = SERVER_FOLDER + file_name
	if(os.path.isfile(file_name)):
		remove_file_at_server = "rm -rf "+file_name
		os.system(remove_file_at_server)
		#Using send function , enocde will convert the said message to utf-8 format
		print("[DELETE] Sync complete file Successfully deleted:", file_name)
		return_value_to_the_client[0] = 0

	else:
		print("[DELETE] Sync complete Requested File to delete not present: ",file_name)
		return_value_to_the_client[0] = 1

def upload_file(file_name,file_data):
	if(os.path.isfile(file_name)):
		os.system("rm -rf ",(SERVER_FOLDER+file_name))
	file_pointer = open((SERVER_FOLDER+file_name),"wb")
	file_pointer.write(file_data.data)
	file_pointer.close()
	print("[UPLOAD] Sync complete File uploaded: ",(SERVER_FOLDER+file_name))


def rpc_callback_at_server(file_name,file_data,operation):

	#Creating Threads
	return_value_to_the_client = [0,0]
	if (operation == "UPLOAD"):
		thread1 = threading.Thread(target = upload_file, args = (file_name,file_data,))
		thread1.start()
		return 1	

	if (operation == "DELETE"):
		thread2 = threading.Thread(target = delete_file_from_server_end, args = (file_name,file_data,return_value_to_the_client,))
		thread2.start()
		thread2.join()

	return return_value_to_the_client[0]
		
if __name__ == "__main__":
	print("\n*** Executing the program at the SERVER side ***\n")
	SERVER_FOLDER = input("Enter the SERVER FOLDER (eg:/mnt/data0/): ")
	print("[***] Server Listening....")
	server = SimpleXMLRPCServer(('localhost', 9000))
	server.register_function(rpc_callback_at_server, 'rpc_callback_at_server')
	server.serve_forever()
