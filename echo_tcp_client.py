import sys
import socket

server = "127.0.0.1"  # The server's hostname or IP address
port = 65432  # The port used by the server
message = ""

for i in range(1, len(sys.argv)):
    message += sys.argv[i]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
s.send(message.encode("utf"))
response = s.recv(1000).decode("utf")
s.close()
print(response)
