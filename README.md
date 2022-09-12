# UTA_CSE_5306_001_PROJECT

## Authors:
Preetham Karanth Kota
pxk6418@mavs.uta.edu

## System Requirements:
_***Linux OS:***</br>
Developed and tested the software on Ubunut 22.04 LTS. Any linux distribution should do just fine
Python 3.10_

## Contents of the PROJECT:

### Part_1_DS:
A python application to DOWNLOAD, UPLOAD, RENAME, DELETE files between client-server </br>

**How to Use:**</br>
1. Open any Linux terminal and run the command "python3 server_side_code.py" to get the server running </br>
2. Open any Linux terminal and run the command "python3 client_side_code.py" to get the client running </br>
3. Enter operation to be performed when prompted i.e. Press 1 for UPLOAD, 2 for DOWNLOAD, 3 for DELETE, 4 for RENAME) </br>
4. Enter path from where the files are to be picked to upload/download/delete and rename at the client side </br>
5. Enter path wrom where the files are to be uploaded/downloaded/deleted and renamed at the client side </br>
6. Enter new name of file at client side to perform all the operations</br>

### Part_2_DS:
A python Application to emulate a synced folder system (such as Dropbox on Microsoft Windows)

** How to Use: ** </br>
1. Open any Linux termina and run the command "python3 helper_thread_server_side.py" to get the server running </br>
2. Open any Linux terminal and run the command "python3 helper_thread_server_side.p" to get the client running </br>
3. Enter path where both at client and server side where the folders are supposed to be in sync </br>
4. Make changes(addition, deletion, modifications) to files in the folder as mentioned </br>
5. Observe changes automatically be reflected on the synced_dir_server </br>