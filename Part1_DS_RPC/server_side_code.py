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

SERVER_FOLDER               = "/"           #default host folder is /

def rename_file_from_server_end(file_name_original,file_name_renamed,return_value_to_the_client):

	file_name_original = SERVER_FOLDER+ file_name_original
	file_name_renamed = SERVER_FOLDER+ file_name_renamed
	if(os.path.isfile(file_name_original)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		remove_file_at_server = "mv "+(file_name_original+" "+file_name_renamed)
		os.system(remove_file_at_server)
		#Using send function , enocde will convert the said message to utf-8 format
		print("[RENAME] File Successfully renamed to: ", file_name_renamed)
		return_value_to_the_client[0] = 0

	else:
		return_value_to_the_client[0] = 1
		print("[RENAME] Requested File to delete not present: ",file_name_original)

def delete_file_from_server_end(file_name,file_data,return_value_to_the_client):
	file_name = SERVER_FOLDER + file_name
	if(os.path.isfile(file_name)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		remove_file_at_server = "rm -rf "+file_name
		os.system(remove_file_at_server)
		#Using send function , enocde will convert the said message to utf-8 format
		print("[DELETE] File Successfully deleted:", file_name)
		return_value_to_the_client[0] = 0

	else:
		print("[DELETE] Requested File to delete not present: ", file_name)
		return_value_to_the_client[0] = 1


def download_file_from_server_end(file_name,file_data,return_value_to_the_client):
	file_name = SERVER_FOLDER + file_name
	global binary_data
	if(os.path.isfile(file_name)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		file_name_to_be_sent_bname = os.path.basename(file_name)

		file_pointer = open(file_name,"rb")
		binary_data = xmlrpc.client.Binary(file_pointer.read())
		return_value_to_the_client[0] = binary_data
		file_pointer.close()
		print("[DOWNLOAD] File Sent to Client to download: ",file_name)

	else:
		print("[DOWNLOAD] File not present at Server",file_name)
		return_value_to_the_client[1] = 1

def upload_file(file_name,file_data):
	file_pointer = open((SERVER_FOLDER+file_name),"wb")
	file_pointer.write(file_data.data)
	file_pointer.close()
	print("[UPLOAD] File upload complete at server end: ",file_name)


def rpc_callback_at_server(file_name,file_data,operation):

	#Creating Threads
	return_value_to_the_client = [0,0]
	if (operation == "UPLOAD"):
		print("Operation upload")
		thread1 = threading.Thread(target = upload_file, args = (file_name,file_data,))
		thread1.start()
		return 1	

	if (operation == "DOWNLOAD"):
		thread2 = threading.Thread(target = download_file_from_server_end, args = (file_name,file_data,return_value_to_the_client,))
		thread2.start()
		thread2.join()


	if (operation == "DELETE"):
		thread3 = threading.Thread(target = delete_file_from_server_end, args = (file_name,file_data,return_value_to_the_client,))
		thread3.start()
		thread3.join()

	if (operation == "RENAME"):
		thread4 = threading.Thread(target = rename_file_from_server_end, args = (file_name,file_data,return_value_to_the_client,))
		thread4.start()
		thread4.join()

	return return_value_to_the_client[0]

	
if __name__ == "__main__":
	print("\n*** Executing the program at the SERVER side ***\n")
	SERVER_FOLDER = input("Enter the SERVER FOLDER (eg:/mnt/data0/): ")
	print("[***] Server Listening....")
	server = SimpleXMLRPCServer(('localhost', 9000))
	server.register_function(rpc_callback_at_server, 'rpc_callback_at_server')
	server.serve_forever()

