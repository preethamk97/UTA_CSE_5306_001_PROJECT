"""
* DS CSE-5306-001 Project 1
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import os
import threading
import subprocess
import re
import xmlrpc.client

CLIENT_FOLDER             = "/"                  #default client path

def delete_a_file(file_name_to_be_sent):

	# sending absolute file name so that would be easy at server side to split and write it to the same file
	file_name_to_be_sent = os.path.basename(file_name_to_be_sent)

	# send the filename,filesize and Operation
	Operation = "DELETE"
	file_data = 0
	proxy_server = xmlrpc.client.ServerProxy('http://localhost:9000')
	b_data = proxy_server.rpc_callback_at_server(file_name_to_be_sent,file_data,Operation)
	if(b_data != 1):
		print("[DELETE] Sync complete file Deleted: ",file_name_to_be_sent)
	else:
		print("[DELETE] Sync complete file not present at Server: ",file_name_to_be_sent )

def send_request_to_server_to_upload(file_name_to_be_sent):
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
		print("[UPLOAD] Sync complete file Uploaded: ",file_name_to_be_sent)
	else:
		print("[UPLOAD] Sync Complete UPLOAD Failure!!: ",file_name_to_be_sent)

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
