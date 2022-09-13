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

CLIENT_FOLDER             = "/"                  #default client path
def rename_a_file():
	file_name_original = input("[*] Enter the Original Filename that needs to be renamed: ") 
	file_name_renamed = input("[*] Enter the New name for the file: ") 

	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_original  = os.path.basename(file_name_original) 
	file_name_renamed  = os.path.basename(file_name_renamed) 

	# send the filename original/new and Operation
	Operation = "RENAME"
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	b_data = proxy_server.rpc_callback_at_server(file_name_original,file_name_renamed,Operation)
	if(b_data != 1):
		print("[RENAME] File Was renamed to:",file_name_renamed," at server end")
	else:
		print("[RENAME] File ",file_name_original," was not present at the server")

	if(os.path.isfile((CLIENT_FOLDER+file_name_original))):
		os.system(("mv "+(CLIENT_FOLDER+file_name_original)+" "+(CLIENT_FOLDER+file_name_renamed)))


def delete_a_file():
	file_name_to_be_sent = input("[*] Enter the Filename that needs to be deleted: ") 

	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_to_be_sent = os.path.basename(file_name_to_be_sent)

	# send the filename,filesize and Operation
	Operation = "DELETE"
	file_data = 0
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	b_data = proxy_server.rpc_callback_at_server(file_name_to_be_sent,file_data,Operation)
	if(b_data != 1):
		print("[DELETE] File Deleted Sucessfully at server: ",file_name_to_be_sent)
	else:
		print("[DELETE] File Not present at server: " ,file_name_to_be_sent)
		

def get_file_from_the_server():
	# Create a socket object
	file_name_to_be_sent = input("[*] Enter the Filename that needs to be downloaded: ") #"ds_client_system/raw_text_file.txt"
	file_name_to_be_sent_bname = os.path.basename(file_name_to_be_sent)

	if( os.path.isfile(CLIENT_FOLDER+file_name_to_be_sent) == False):
		print("[UPLOAD] File not present: ", (CLIENT_FOLDER+file_name_to_be_sent))
		return
	
	os.system(("rm -rf "+(CLIENT_FOLDER+file_name_to_be_sent)))

	# send the filename,filesize and Operation
	Operation = "DOWNLOAD"
	file_data = 0
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	file_pointer_to_write_at_client = open((CLIENT_FOLDER+file_name_to_be_sent),"wb")
	b_data = proxy_server.rpc_callback_at_server(file_name_to_be_sent,file_data,Operation)
	if(b_data != 1):
		file_pointer_to_write_at_client.write(b_data.data)
		print("[DOWNLOAD] File Downloaded Successfully present at : ",(CLIENT_FOLDER+file_name_to_be_sent) )
	else:
		print("[DOWNLOAD] File Not present at server: ",file_name_to_be_sent )
		
	file_pointer_to_write_at_client.close()

def send_request_to_server_to_upload():
	file_name_to_be_sent = input("[UPLOAD] Enter the File name to Upload: ") 
	if( os.path.isfile(CLIENT_FOLDER+file_name_to_be_sent) == False):
		print("[UPLOAD] File not present: ", (CLIENT_FOLDER+file_name_to_be_sent))
		return

	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	file_pointer = open((CLIENT_FOLDER+file_name_to_be_sent), "rb")
	binary_data = xmlrpc.client.Binary(file_pointer.read())
	operation = "UPLOAD"
	status = proxy_server.rpc_callback_at_server(file_name_to_be_sent, binary_data,operation)
	file_pointer.close()
	if (status == 1):
		print("[UPLOAD] File Sent Successfully to the Server: ", file_name_to_be_sent)
	else:
		print("[UPLOAD] UPLOAD Failure!! : ",file_name_to_be_sent)

def send_request_to_server():

	print("\n[OPTIONS] File Operations [*] Enter 1 to UPLOAD\n[*] Enter 2 to DOWNLOADd\n[*] Enter 3 to DELETE\n(*) Enter 4 to RENAME \n(*) 5 to exit\n")

	choice = int(input("[*] Enter Your choice: "))
	if (choice == 1):
		send_request_to_server_to_upload()

	elif (choice == 2):
		get_file_from_the_server()

	elif(choice == 3):
		delete_a_file()

	elif(choice == 4):
		rename_a_file()

	elif(choice ==5):
		return
	send_request_to_server()

if __name__ == "__main__":
	print("\n*** Executing the program at the client side ***\n")
	CLIENT_FOLDER = input("Enter the CLIENT FOLDER (eg:/mnt/data0/): ")
	send_request_to_server()
