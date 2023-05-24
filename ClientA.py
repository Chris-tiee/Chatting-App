import socket
import threading
import time

        
def flipS():
    if SEQ=='0':
        return '1'
    else:
        return '0'
        
def receive():
    global SEQ
    while(True):
    
        localIP     = "127.1.1.2"
        localPort   = 2000
        bufferSize  = 1024
        UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPSocket.bind((localIP, localPort))
        bytesAddressPair = UDPSocket.recvfrom(bufferSize)
        message = format(bytesAddressPair[0])
        
        tp=message[2]
        sequence=message[3]
        if tp=='1' and sequence==SEQ:
            serverAddressPort   = ("127.1.1.1", 2000)
            OK=str.encode("2"+SEQ+"ACK")
            UDPSocket.sendto(OK,serverAddressPort)
            x = "Message received: " + message[4:len(message)-1]
            print(x)
            SEQ=flipS()
        elif tp=='2' and SEQ==sequence:
            SEQ=flipS()
            
    

def send():
    global SEQ    
    while(True):
        localIP     = "127.1.1.2"
        localPort   = 2001
        UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPSocket.bind((localIP, localPort))

        x                   = input()
        bytesToSend         = str.encode("1"+SEQ+x)
        serverAddressPort   = ("127.1.1.1", 2000)
        ACK1=SEQ
        UDPSocket.sendto(bytesToSend, serverAddressPort)
        
        while True:
            time.sleep(0.5)
            if ACK1==SEQ:
                    UDPSocket.sendto(bytesToSend,serverAddressPort)
            else:
                break

def sendfile():
	import socket
	import tqdm
	import os

	SEPARATOR = "<SEPARATOR>"
	BUFFER_SIZE = 1024 * 4

	def send_file(filename, host, port):
	    filesize = os.path.getsize(filename)
	    s = socket.socket()
	    print(f"[+] Connecting to {host}:{port}")
	    s.connect((host, port))
	    print("[+] Connected.")
	
	    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
	
	    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	    with open(filename, "rb") as f:
	        while True:
	            bytes_read = f.read(BUFFER_SIZE)
	            if not bytes_read:
	                break
	            s.sendall(bytes_read)
	            progress.update(len(bytes_read))
	
	    s.close()

	if __name__ == "__main__":
	    filename = "a.txt"
	    host = "10.169.1.7"
	    port = 5001
	    send_file(filename, host, port)

def receivefile():
	import socket
	import tqdm
	import os


	SERVER_HOST = '10.169.1.7'
	SERVER_PORT = 5001
	BUFFER_SIZE = 4096
	SEPARATOR = "<SEPARATOR>"
	s = socket.socket()
	s.bind((SERVER_HOST, SERVER_PORT))
	s.listen(5)
	print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
	client_socket, address = s.accept() 
	print(f"[+] {address} is connected.")

	received = client_socket.recv(BUFFER_SIZE).decode()
	filename, filesize = received.split(SEPARATOR)
	filename = os.path.basename(filename)
	filesize = int(filesize)
	progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "wb") as f:
	    while True:
	        bytes_read = client_socket.recv(BUFFER_SIZE)
	        if not bytes_read:    
	            break
	        f.write(bytes_read)
	        progress.update(len(bytes_read))

	client_socket.close()
	s.close()

global SEQ
SEQ='0'

t1 = threading.Thread(target=sendfile)
t2 = threading.Thread(target=receivefile)
t3 = threading.Thread(target=send)
t4 = threading.Thread(target=receive)

x=1
time.sleep(1)
t1.start()
while True:
    if ((t1.is_alive()==False) and (x==1)):
        time.sleep(1)
        t2.start()
        x=2
    
    if ((t2.is_alive()==False) and (t1.is_alive()==False) and (x==2)):
        time.sleep(1)
        t3.start()
        t4.start()
        break
