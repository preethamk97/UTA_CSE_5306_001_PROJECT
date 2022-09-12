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

SEPARATOR                 = "<SEPARATOR>"        #Delimiter to seperate string
SEND_BUFFER_SIZE          = 1000;                #1000 Bytes
port                      = 7777                 # Creating a port number for our communication
host_name                 = socket.gethostname() # host name required to bind the port and host 
CLIENT_FOLDER             = "/"                  #default client path
list_of_all_files         = []
def rename_a_file():
	# Create a socket object
	socket_at_client = socket.socket()

	print("[*] Connecting to Host: ",host_name," Port: ",port)
	socket_at_client.connect((host_name, port))
	print("[*] Connection Established with the server")

	#while True:
	file_name_original = input("[*] Enter the Original Filename that needs to be renamed: ") 
	file_name_renamed = input("[*] Enter the New name for the file: ") 

	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_original  = os.path.basename(file_name_original) 
	file_name_renamed  = os.path.basename(file_name_renamed) 

	# send the filename,filesize and Operation
	Operation = "RENAME"

	#Using send function , enocde will convert the said message to utf-8 format
	socket_at_client.send(f"{file_name_original}{SEPARATOR}{file_name_renamed}{SEPARATOR}{Operation}".encode())

	file_info = socket_at_client.recv(SEND_BUFFER_SIZE).decode()
	Operation , Seperator= file_info.split(SEPARATOR)

	if(os.path.isfile((CLIENT_FOLDER+file_name_original))):
		os.system(("mv "+(CLIENT_FOLDER+file_name_original)+" "+(CLIENT_FOLDER+file_name_renamed)))

	if (Operation ==  "PRESENT"):
		print("[RENAME] File Was renamed to :",file_name_renamed," at server end")
	else:
		print("[RENAME] File ",file_name_original," was not present at the server")

def delete_a_file():
	# Create a socket object
	socket_at_client = socket.socket()

	print("[*] Connecting to Host: ",host_name," Port: ",port)
	socket_at_client.connect((host_name, port))
	print("[*] Connection Established with the server")

	#while True:
	file_name_to_be_sent = input("[*] Enter the Filename that needs to be deleted: ") #"ds_client_system/raw_text_file.txt"
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
		print("[DELETE] File deleted at Server")
	else:
		print("[DELETE] File not present at the server")


def get_file_from_the_server():
	# Create a socket object
	socket_at_client = socket.socket()

	print("[*] Connecting to Host: ",host_name," Port: ",port)
	socket_at_client.connect((host_name, port))
	print("[*] Connection Established with the server")

	file_name_to_be_sent = input("[*] Enter the Filename that needs to be downloaded: ") #"ds_client_system/raw_text_file.txt"
	file_size_to_be_sent = 0 # As no file is present hence sending 0
	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_to_be_sent_bname = os.path.basename(file_name_to_be_sent)

	# send the filename,filesize and Operation
	Operation = "DOWNLOAD"
	socket_at_client.send(f"{file_name_to_be_sent_bname}{SEPARATOR}{file_size_to_be_sent}{SEPARATOR}{Operation}".encode())

	file_info = socket_at_client.recv(SEND_BUFFER_SIZE).decode()
	file_name_at_c, file_size_at_c, Operation = file_info.split(SEPARATOR)

	if (Operation == "PRESENT"):
		file_name_at_c = CLIENT_FOLDER + file_name_at_c	
		# start receiving the file from the socket and writing to the file stream, open it in write binary mode
		file_pointer = open(file_name_at_c, "wb")

		read_bytes = socket_at_client.recv(int(file_size_at_c))
		file_pointer.write(read_bytes)
		file_pointer.close()
		print("[DOWNLOAD] File Downloaded Successfully present at : ", file_name_at_c)
	else:
		print("[DOWNLOAD] File is not present at the server")

	# close the socket
	socket_at_client.close()

def send_request_to_server_to_upload():

	# Add a check to see if the file name exists PK!!
	file_name_to_be_sent = input("[UPLOAD] Enter the File name to Upload: ") 
	file_size_to_be_sent = os.path.getsize((CLIENT_FOLDER+file_name_to_be_sent))

	if( os.path.isfile(CLIENT_FOLDER+file_name_to_be_sent) == False):
		print("[UPLOAD] File not present: ", (CLIENT_FOLDER+file_name_to_be_sent))
		return

	# Create a socket object
	socket_at_client = socket.socket()

	print("[UPLOAD] Connecting to Host: ",host_name," Port: ",port)
	socket_at_client.connect((host_name, port))
	print("[UPLOAD] Connection Established with the server")

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
	print("[UPLOAD] File Sent Successfully to the Server")

	# close the socket
	socket_at_client.close()

def send_request_to_server():

	print("\n[OPTIONS] (*) Press 1 to Upload a File\t(*) Press 2 to Download a file\t(*) Press 3 to Delete a file\t(*) Press 4 to Rename a file (*) 5 to exit\n")

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
