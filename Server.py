import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_pc = ""
port = 12348
s.bind((local_pc, port))
s.listen()

while True:
    print("Server Listening: ")
    conn, addr = s.accept()
    print("Connection OK ", addr)
    try:
        while True:
            command = input("Command: ")
            logfile = open("Logfile.txt",'a')
            logfile.write("Command: " + command + "\n")
            if len(command) > 0 and command[:7] != "getfile":
                if command[:6] == "upload":
                    conn.sendall(command.encode())
                    status = conn.recv(1000).decode()
                    if "Ready" in status:
                        f = open(command[7:],'rb')
                        conn.sendall(f.read())
                        f.close()
                        print("File Uploaded")
                    else:
                        print("Client not ready")

                else:
                    conn.sendall(command.encode())
                    packet = conn.recv(5000)
                    decoded = packet.decode()
                    print(decoded)
                    logfile.write(decoded)
                    logfile.close()

            elif len(command) > 0 and command[:7] == "getfile":
                newfilename = input("Enter New Filename")
                conn.sendall(command.encode())
                packet = conn.recv(5000)
                decoded = packet.decode()
                print("Decoded")
                f = open(newfilename, "wb")
                f.write(packet)
                f.close()

            elif len(command) > 0 and command[:4] == "cat":
                packet = conn.recv(5000)
                # decoded = packet.decode()
                print("Contents:\n")
                print(packet)

            else:
                print("No empty Commands")


    except:
        print("Dissocnnected from Addr: ", addr)



