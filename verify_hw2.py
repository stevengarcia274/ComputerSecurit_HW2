# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 10:05:57 2022

@author: Steve
"""

import sys
from Crypto.Hash import SHA256
import math


def main():
    if len(sys.argv) != 3:
        return sys.stderr.write("Number of arguments is  incorrect, please check command line.\n")
    else:
        inputPDF = sys.argv[1]
        origHashValue = sys.argv[2]
            
        with open(inputPDF, 'rb') as f:
            inputBA = f.read()
            
        numIte = math.ceil(len(inputBA)/4096)
        #print(numIte)
        t  = numIte
        
        lastBlockSize = len(inputBA) % 4096
        #print(lastBlockSize)
        start = len(inputBA) - lastBlockSize
        end = len(inputBA)
       
        curDigest = b''
        
        #print(t)
        
        while t > 0:
            hashVal = SHA256.new()
            curBlock = []
            
            myStart = start
            
            while myStart < end:
                curBlock.append(inputBA[myStart])
                myStart = myStart + 1
            end = start
            start = start - 4096
            byteBlock = bytearray(curBlock)
            if t == numIte:
                hashVal.update(byteBlock)
                curDigest = hashVal.digest()
                
            else:
                
                comboByte = byteBlock + bytearray(curDigest)
                #print(len(comboByte))
                hashVal.update(comboByte)
                curDigest = hashVal.digest()

                
                
            t = t - 1
        
        if curDigest.hex() != origHashValue:
            #print(origHashValue)
            return print("False")
        else:
            return print("True")
            
if __name__ == "__main__":
    main()      