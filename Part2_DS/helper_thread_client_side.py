"""
* DS CSE-5306-001 Project 1
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import os
import socket 
import threading
import subprocess
import re

SEPARATOR                 = "<SEPARATOR>"        #Delimiter to seperate string
SEND_BUFFER_SIZE          = 1000;                #1000 Bytes
port                      = 7777                 # Creating a port number for our communication
host_name                 = socket.gethostname() # host name required to bind the port and host 
CLIENT_FOLDER             = "/"                  #default client path

def delete_a_file(file_name_to_be_sent):
	# Create a socket object
	socket_at_client = socket.socket()

	socket_at_client.connect((host_name, port))
	print("[*] Update required syncing.........")

	#while True:
	file_size_to_be_sent = 0 # As no file is present hence sending 0

	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_to_be_sent_bname = os.path.basename(file_name_to_be_sent)

	# send the filename,filesize and Operation
	Operation = "DELETE"

	#Using send function , enocde will convert the said message to utf-8 format
	socket_at_client.send(f"{file_name_to_be_sent_bname}{SEPARATOR}{file_size_to_be_sent}{SEPARATOR}{Operation}".encode())

	file_info = socket_at_client.recv(SEND_BUFFER_SIZE).decode()
	Operation , Seperator= file_info.split(SEPARATOR)

	if(os.path.isfile((CLIENT_FOLDER+file_name_to_be_sent))):
		os.system(("rm -rf "+ (CLIENT_FOLDER+file_name_to_be_sent_bname)))

	if (Operation ==  "PRESENT"):
		print("[*] Sync complete File Deleted: ",file_name_to_be_sent)
	else:
		print("[*] Sync complete File not found at server: ",file_name_to_be_sent)

def send_request_to_server_to_upload(file_name_to_be_sent):

	# Add a check to see if the file name exists PK!!
	file_size_to_be_sent = os.path.getsize((CLIENT_FOLDER+file_name_to_be_sent))

	if( os.path.isfile(CLIENT_FOLDER+file_name_to_be_sent) == False):
		print("[UPLOAD] File not present: ", (CLIENT_FOLDER+file_name_to_be_sent))
		return

	# Create a socket object
	socket_at_client = socket.socket()
	socket_at_client.connect((host_name, port))

	print("[*] Update required syncing.........")
	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_to_be_sent_bname = os.path.basename(file_name_to_be_sent)

	# send the filename,filesize and Operation
	Operation = "UPLOAD"
	socket_at_client.send(f"{file_name_to_be_sent_bname}{SEPARATOR}{file_size_to_be_sent}{SEPARATOR}{Operation}".encode())
	
	# Opening the file to be sent in the read binary mode so that blocks could be sent in the binary format
	with open((CLIENT_FOLDER+file_name_to_be_sent), "rb") as file_pointer:
		while True:
			bytes_read = file_pointer.read(SEND_BUFFER_SIZE) # read the bytes from the file with chunks as specified in SEND_BUFFER_SIZE
			if not bytes_read:
				break
			socket_at_client.sendall(bytes_read)
	print("[*] Sync complete updated file at server: ",file_name_to_be_sent)

	# close the socket
	socket_at_client.close()

def poll_to_update_the_contents_client_to_server(list_of_all_files,dict_of_md5sum):

	current_list_of_files = os.listdir(CLIENT_FOLDER)

	# All the extra file names in the old list states those files are missing when compared to contents of current dir
	# Hence deleting those files and updating in the temporary list
	list_of_files_missing_in_the_current_dir = list((set(list_of_all_files).difference(current_list_of_files)))
	temporary_list_of_all_files_old = list_of_all_files
	for file_name in list_of_files_missing_in_the_current_dir:
		del dict_of_md5sum[file_name]
		temporary_list_of_all_files_old.remove(file_name )
		delete_a_file(file_name)

	list_of_all_files = temporary_list_of_all_files_old

	for file_name_in_curr in current_list_of_files:
		if file_name_in_curr in list_of_all_files:
			md5sum_output = subprocess.getoutput(("md5sum "+ (CLIENT_FOLDER+str(file_name_in_curr))) )
			if (dict_of_md5sum[file_name_in_curr] != str((re.search(".* /",str(md5sum_output)))[0])[:-2].strip() ):
				dict_of_md5sum[file_name_in_curr] = str((re.search(".* /",str(md5sum_output)))[0])[:-2].strip()
				send_request_to_server_to_upload(file_name_in_curr)
		else:
			md5sum_output = subprocess.getoutput(("md5sum "+ (CLIENT_FOLDER+str(file_name_in_curr))) )
			dict_of_md5sum[file_name_in_curr] = str((re.search(".* /",str(md5sum_output)))[0])[:-2].strip()
			list_of_all_files.append(file_name_in_curr)
			send_request_to_server_to_upload(file_name_in_curr)
			#send delete
	
	threading.Timer(10, poll_to_update_the_contents_client_to_server,args=(list_of_all_files,dict_of_md5sum,)).start()

if __name__ == "__main__":
	print("\n*** Executing the program at the client side ***\n")
	CLIENT_FOLDER = input("Enter the CLIENT FOLDER (eg:/mnt/data0/): ")
	list_of_all_files = os.listdir(CLIENT_FOLDER)
	dict_of_md5sum = {}
	for file_name in list_of_all_files:
		md5sum_output = subprocess.getoutput(("md5sum "+ (CLIENT_FOLDER+str(file_name))) )
		#re will return list containing "md5sumhash filename" we need to get only md5sumhas in str form hence below logic str(list[0])[:-2]
		dict_of_md5sum[str(file_name)] = str((re.search(".* /",str(md5sum_output)))[0])[:-2].strip()
		#print("OUTPUT: ", md5sum_output)
	print("[*] Starting Sync routine")
	poll_to_update_the_contents_client_to_server(list_of_all_files,dict_of_md5sum)
