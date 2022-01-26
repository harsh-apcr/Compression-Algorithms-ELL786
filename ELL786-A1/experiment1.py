import random
import numpy as np


#reading the input text file
txt_file = open("sample.txt", "r")
#data is the input string
data = txt_file.read()
txt_file.close()


#text_to_binary is function which converts the string into binary string
def text_to_binary(s):
    
    n = len(s)
    s1 = ""
    
    for i in range(n):
        s2 = ""
        
        #to get ascii value of character
        val = ord(s[i])
        
        #converting the ascii value into 7 bits binary string
        while(val>0):
            if(val%2==0):
                s2+='0'   
            else:
                s2+='1'
            val = val//2
            
        #if length of binary string is less than 7 then appending zeros    
        c=len(s2)
        if(c<7):
            for i in range(7-c):
                s2+='0'
        s2 = s2[::-1]
        
        #appending the binary string of each character 
        s1+=s2
    return s1   


#generate_random_binary_string function generates a binary string of length n with hamming weight d
#such that non-zero entries are distributed uniformly
def generate_random_binary_string(n,d):
    s = ""
    
    for i in range(n):
        s+='0'
    
    #random.sample generate list of uniformly distributed d random numbers in range 0-n 
    randomlist = random.sample(range(n), d)
    
    for i in range(d):
        c = randomlist[i]
        #using slicing of string 
        s = s[:c]+'1'+s[c+1:]
    return s


#xor_binary_strings function takes xor of two binary strings s1 and s2
def xor_binary_strings(s1,s2):
    
    n = len(s1)
    s = ""
    
    for i in range(n):
        
        #if both bits are same then xor will be 0
        if(s1[i]==s2[i]):
            s+='0'
        #if both bits are different then xor will be 0
        else:
            s+='1'
    return s


#binarystring_textfile function converts the binary string into text string
def binarystring_textfile(s):
    
    s1=""
    n = len(s)
    i=0
    
    while(i<n):
        
        #converting the chuncks of 7 bits into character using ascii
        s1=s1+chr(int(s[i:i+7], 2))
        i=i+7
    return s1    
    
    
#compare function calculates percentage of modified characters with
#respect to the input file   
def compare(s1,s2):
    
    n = len(s1)
    c=0
    for i in range(n):
        if(s1[i]!=s2[i]):
            c+=1  
    print("Number of Different characters are",c) 
    print("Percentage of Modified characters is",(c/n)*100)
    
#--------------------------------end----------------------------------

#testing with different values of d

#d=10
s1 = generate_random_binary_string(len(text_to_binary(data)),10)
t1 = binarystring_textfile(xor_binary_strings(s1,text_to_binary(data)))
print(compare(data,t1))
    
#d=100    
s2 = generate_random_binary_string(len(text_to_binary(data)),100)
t2 = binarystring_textfile(xor_binary_strings(s2,text_to_binary(data)))
print(compare(data,t2))

#d=200
s3 = generate_random_binary_string(len(text_to_binary(data)),200)
t3 = binarystring_textfile(xor_binary_strings(s3,text_to_binary(data)))
print(compare(data,t3))

#d=500
s4 = generate_random_binary_string(len(text_to_binary(data)),500)
t4 = binarystring_textfile(xor_binary_strings(s4,text_to_binary(data)))
print(compare(data,t4))

#d=5000
s5 = generate_random_binary_string(len(text_to_binary(data)),5000)
t5 = binarystring_textfile(xor_binary_strings(s5,text_to_binary(data)))
print(compare(data,t5))