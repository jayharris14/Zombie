#!/usr/bin/python

import sys

import os

import threading

from socket import*

from os.path import exists

import subprocess

import multiprocessing as multiproc


def myclient():
    serverName= 'turing'
    serverPort= 1707
    clientSocket= socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    order= clientSocket.recv(1024)
    order=str(order.decode())
    print(order)
    i=4
    runprogram="./"
    program=""
    while order[i]!=" ":
        runprogram=str(runprogram+ order[i])
        program=str(program+ order[i])
        i=i+1
    if order.find("INI")!=-1:
        file_exists=exists(program)
        if file_exists==True:
            sentence=("SUC")
            clientSocket.send(sentence.encode())
    def run():
        if order.find("INI")!=-1:
            file1=open("data.txt", "w")
            file1.write(subprocess.check_output(runprogram, stderr=subprocess.STDOUT, shell=True))
            file1.close()
        if order.find("RPT")!=-1:
            if os.path.getsize("data.txt")==0:
                sentence="pending"
                clientSocket.send(sentence.encode())
                file1=open("data.txt", "w")
                file1.write(subprocess.check_output(runprogram, stderr=subprocess.STDOUT, shell=True))
                file1.close()
            else:
                file1=open("data.txt", "r")
                page=file1.read()
                file1.close()
                clientSocket.send(page.encode())
                clientSocket.close()
    x=threading.Thread(target=run, args=())
    x.start() 
    if threading.activeCount()>=3:
        clientSocket.send("pending")
    
    
    
    
    
def main():
    myclient()
   # save(modifiedSentence1)

main()
