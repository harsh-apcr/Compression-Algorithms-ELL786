import random
import numpy as np

txt_file = open("new.txt", "r")
data = txt_file.read()
txt_file.close()

def text_to_binary(s):
    n = len(s)
    s1 = ""
    for i in range(n):
        s2 = ""
        val = ord(s[i])
        while(val>0):
            if(val%2==0):
                s2+='0'   
            else:
                s2+='1'
            val = val//2
        c=len(s2)
        if(c<7):
            for i in range(7-c):
                s2+='0'
        s2 = s2[::-1]
        s1+=s2
    return s1   

def generate_random_binary_string(n,d):
    s = ""
    for i in range(n):
        s+='0'
    randomlist = random.sample(range(n), d)
    for i in range(d):
        c = randomlist[i]
        s = s[:c]+'1'+s[c+1:]
    return s


def xor_binary_strings(s1,s2):
    
    n = len(s1)
    s = ""
    for i in range(n):
        if(s1[i]==s2[i]):
            s+='0'
        else:
            s+='1'
    return s

def binarystring_textfile(s):
    s1=""
    n = len(s)
    i=0
    while(i<n):
        s1=s1+chr(int(s[i:i+7], 2))
        i=i+7
    return s1    
    
def compare(s1,s2):
    n = len(s1)
    c=0
    for i in range(n):
        if(s1[i]!=s2[i]):
            c+=1  
    return c,(c/n)*100


s1 = generate_random_binary_string(len(text_to_binary(data)),10)
t1 = binarystring_textfile(xor_binary_strings(s1,text_to_binary(data)))
print(compare(data,t1))
    
    
s2 = generate_random_binary_string(len(text_to_binary(data)),100)
t2 = binarystring_textfile(xor_binary_strings(s2,text_to_binary(data)))
print(compare(data,t2))

s3 = generate_random_binary_string(len(text_to_binary(data)),200)
t3 = binarystring_textfile(xor_binary_strings(s3,text_to_binary(data)))
print(compare(data,t3))

s4 = generate_random_binary_string(len(text_to_binary(data)),500)
t4 = binarystring_textfile(xor_binary_strings(s4,text_to_binary(data)))
print(compare(data,t4))

s5 = generate_random_binary_string(len(text_to_binary(data)),5000)
t5 = binarystring_textfile(xor_binary_strings(s5,text_to_binary(data)))
print(compare(data,t5))
    
def frequency(s):
    a = [0]*128
    n = len(s)
    for i in range(n):
        a[ord(s[i])]+=1
    return a    

b=frequency(data)
for i in range(128):
    if(b[i]!=0):
        print(i,b[i],chr(i))    