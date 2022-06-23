#!/usr/bin/python

import threading
import sys
from socket import*
from datetime import datetime
import os
import select
import signal




def assignsocket():
    i=1;
    p=3;
    q=0;
    num_ports=int((len(sys.argv)-3))
    port=[]
    sockets=[]
    while q<num_ports:
        port.append(int(sys.argv[p]))
        print(int(sys.argv[p]))
        p=p+1
        serverSocket= socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(("",port[q]))
        sockets.append(serverSocket)
        q=q+1
        serverSocket.listen(1)
        print('The server is ready to recieve')
    return sockets
    
def connectandsend(socketlist):
    def pagedisplay():
        while True:
            readable, writable, exceptional=select.select(socketlist, [], [])
            for t in readable:
                connectionSocket, addr= t.accept()
            try:
                command=sys.argv[1]
                program=sys.argv[2]
                if command=="INI" or command=="STP" or command=="RPT":
                    if command=="INI":
                        sentence=("INI "+ program + " ..")
                        connectionSocket.send(sentence.encode())
                        signal=connectionSocket.recv(1024)
                        signal=str(signal.decode())
                        if signal=="SUC":
                            print("ok")
                            connectionSocket.close()
                            break
                        else:
                            print("error occured")
                            connectionSocket.close()
                    if command=="STP":
                        sentence=("STP "+ program + " ..")
                        connectionSocket.send(sentence.encode())
                        print("ok")
                        connectionSocket.close()
                        break
                    if command=="RPT":
                        sentence=("RPT "+ program + " ..")
                        connectionSocket.send(sentence.encode())
                        print("ok")
                        report=connectionSocket.recv(1024)
                        report=report.encode()
                        print(report)
                        connectionSocket.close()
                        break

            except ValueError:
                print("invalid input")
                connectionSocket.close()

   # try:
    x=threading.Thread(target=pagedisplay, args=())
    x.start()
   # except:
   #     print("Error: unable to start thread")
def main():
    socketlist=[]
    socketlist=assignsocket()
    connectandsend(socketlist)

main()
