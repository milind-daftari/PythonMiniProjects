import socket

def find_digit(input):
    count = 0
    digits = ""
    for i in input:
        if i.isdigit():
            count += 1
            digits += str(i)
    return count,digits

server = "127.0.0.1"  # Standard loopback interface address (localhost)
port = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(10)

while True:
    connection, address = s.accept()
    message = connection.recv(1000).decode("utf")
    if "SECRET" in message:
        count = 0
        digits = ""
        count, digits = find_digit(str(message))
        response = "Received: Digits: " + digits + " Count: " + str(count)
    else:
        response = "Secret code not found"
    connection.send(response.encode("utf"))
    connection.close()