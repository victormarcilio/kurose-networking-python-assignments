from socket import *
import sys

def get_content_type(filename):
    if filename.endswith('.pdf'):
        return 'application/pdf'
    if filename.endswith('.mp4'):
        return 'audio/mp4'
    
    return 'text/plain'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 10000))
serverSocket.listen(1)
while True:
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(4096).decode()
        print('message =', repr(message))
        filename = message.split()[1]
        print('filename =', repr(filename))
        print(filename[1:])
        f = open(filename[1:], 'rb')
        outputdata = f.read() 

        connectionSocket.send(f"HTTP/1.1 200 OK\r\nContent-Type: {get_content_type(filename.lower())}\r\nConnection: close\r\n\r\n".encode())
        connectionSocket.send(outputdata)
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        print(f'{filename} not present')
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode())
        connectionSocket.close()
serverSocket.close()
sys.exit()
