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

#Creating threading lock object to create threading lock
lock = threading.Lock()
RCV_BUFFER_SIZE             = 1000 	    #1000 Bytes
SEPARATOR                   = "<SEPARATOR>" #Delimiter used to slplit the string 
port                        =  7777         #Creating a port number for our communication
host_name                   = "0.0.0.0"     #socket.gethostname() #host name required to bind the port and host 
SERVER_FOLDER               = "/"           #default host folder is /

def rename_file_from_server_end(file_name_original,file_name_renamed,client_sock):
	file_name_original = SERVER_FOLDER+ file_name_original
	file_name_renamed = SERVER_FOLDER+ file_name_renamed
	if(os.path.isfile(file_name_original)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		Operation = "PRESENT"
		remove_file_at_server = "mv "+(file_name_original+" "+file_name_renamed)
		os.system(remove_file_at_server)
		#Using send function , enocde will convert the said message to utf-8 format
		client_sock.send(f"{Operation}{SEPARATOR}".encode())
		print("[RENAME] File Successfully renamed to:", file_name_renamed)

	else:
		Operation = "NOT_PRESENT"
		client_sock.send(f"{Operation}".encode())
		print("[RENAME] Requested File to delete not present")

def delete_file_from_server_end(file_name_at_c,file_size_at_c,client_sock):
	file_name_at_c = SERVER_FOLDER + file_name_at_c
	if(os.path.isfile(file_name_at_c)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		Operation = "PRESENT"
		remove_file_at_server = "rm -rf "+file_name_at_c
		os.system(remove_file_at_server)
		#Using send function , enocde will convert the said message to utf-8 format
		client_sock.send(f"{Operation}{SEPARATOR}".encode())
		print("[DELETE] File Successfully deleted:", file_name_at_c)

	else:
		Operation = "NOT_PRESENT"
		client_sock.send(f"{Operation}".encode())
		print("[DELETE] Requested File to delete not present")


def download_file_from_server_end(file_name_at_c,file_size_at_c,client_sock):
	file_name_at_c = SERVER_FOLDER + file_name_at_c
	if(os.path.isfile(file_name_at_c)):
		# sending absolute file name so that would be easy at server side to split and write it to the same file
		file_size_at_c = int(os.path.getsize(file_name_at_c))
		file_name_to_be_sent_bname = os.path.basename(file_name_at_c)
		Operation = "PRESENT"
		#Using send function , enocde will convert the said message to utf-8 format
		client_sock.send(f"{file_name_to_be_sent_bname}{SEPARATOR}{file_size_at_c}{SEPARATOR}{Operation}".encode())
	
		# Opening the file to be sent in the read binary mode so that blocks could be sent in the binary format
		with open(file_name_at_c, "rb") as file_pointer:
			while True:
				bytes_read = file_pointer.read(RCV_BUFFER_SIZE) # read the bytes from the file with chunks as specified in SEND_BUFFER_SIZE
				if not bytes_read:
					break
				client_sock.sendall(bytes_read)
			print("[DOWNLOAD] File Sent Successfully From Server File size: ", file_size_at_c)

	else:
		Operation = "NOT_PRESENT"
		client_sock.send(f"{file_name_to_be_sent_bname}{SEPARATOR}{file_size_at_c}{SEPARATOR}{Operation}".encode())
		print("[DOWNLOAD] File Not Present at: ", file_size_at_c)

def upload_file_at_server_end(file_name_at_c,file_size_at_c,client_sock):
	file_name_at_c = SERVER_FOLDER + file_name_at_c	
	file_size_at_c = int(file_size_at_c)
	# start receiving the file from the socket and writing to the file stream, open it in write binary mode
	with open(file_name_at_c, "wb") as file_pointer:
		while True:
			bytes_read = client_sock.recv(RCV_BUFFER_SIZE)
			if not bytes_read:
				break
			# write to the file the bytes we just received
			file_pointer.write(bytes_read)

	print("[UPLOAD] File Successfully recieved From Client Present at: ", file_name_at_c)

def send_request_to_server():

	#Create a socket object
	socket_at_server = socket.socket()
	socket_at_server.bind((host_name,port))
	socket_at_server.listen(100)

	print("[*] Listening as: ",host_name," Port: ",port)

	#Accepting the connnection at server end
	while True:
		#Accepting the connnection at server end
		client_sock , client_address = socket_at_server.accept()
		file_info = client_sock.recv(RCV_BUFFER_SIZE).decode()
		file_name_at_c, file_size_at_c, Operation = file_info.split(SEPARATOR)
		print("[*] Connection Established with the Client Address: ", client_address)

		#Creating Threads
		thread1 = threading.Thread(target = upload_file_at_server_end, args = (file_name_at_c,file_size_at_c,client_sock,))
		thread2 = threading.Thread(target = download_file_from_server_end, args = (file_name_at_c,file_size_at_c,client_sock,))
		thread3 = threading.Thread(target = delete_file_from_server_end, args = (file_name_at_c,file_size_at_c,client_sock,))
		thread4 = threading.Thread(target = rename_file_from_server_end, args = (file_name_at_c,file_size_at_c,client_sock,))

		if (Operation == "UPLOAD"):
			thread1.start()

		if (Operation == "DOWNLOAD"):
			thread2.start()

		if (Operation == "DELETE"):
			thread3.start()

		if (Operation == "RENAME"):
			thread4.start()

	#Note need to Join all the threads TO DO AT ALL COSTS	
	client_sock.close()
	socket_at_server.close()

if __name__ == "__main__":
	print("\n*** Executing the program at the SERVER side ***\n")
	SERVER_FOLDER = input("Enter the SERVER FOLDER (eg:/mnt/data0/): ")
	send_request_to_server()
