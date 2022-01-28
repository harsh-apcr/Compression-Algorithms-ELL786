import random
import numpy as np
from itertools import groupby

#reading text file
txt_file = open("new.txt", "r")
data = txt_file.read()
txt_file.close()


#length of input string
n  = len(data)

#string of unique characters
s = ''.join(k for k, g in groupby(sorted(data)))

#number of unique characters 
l = len(s)

#x stores occurence of each character
x = np.zeros(l)
#y stores probability of each character
y = np.zeros(l)

for i in range(l):
    #c in number of occurence of each character
    c = data.count(s[i])
    x[i] = c
    y[i] = c/n

#calculate sum upto to some index of array
def sum_upto_index(a,i):
    s = 0
    for j in range(i+1):
        s+=a[j]
    return s

#cp stores the cumulative summation of 'p' from '1' till last value of 'p
cp = np.zeros(l)
for i in range(l):
    cp[i] = sum_upto_index(y,i)
    
modified_cp = np.zeros(l+1)
for i in range(l):
    modified_cp[i+1] = cp[i]

#inter stores the intervals    
inter = np.zeros((l,2))
for i in range(l):
    inter[i][0] = modified_cp[i]
    inter[i][1] = cp[i]    


#encoding
l1 = 0
h1 = 1
for i in range(n):
    for j in range(l):
    
        #if character from data matches with the string s
        if(data[i]==s[j]):
            p = j
            j+=1
            r = h1-l1
            h1 = l1 + r*(inter[p][1])
            l1 = l1 + r*(inter[p][0])
            i+=1
            break

l1 = (l1+h1)/2
print(l1)


#decoding

decoded_string = ""

for i in range(n):
    for j in range(l):
        
        #if l1 value falls within the range
        if (l1>inter[j][0] and l1<inter[j][1]):
            
            p1 = j
            l1 = (l1 - inter[p1][0])/(y[j])
            decoded_string+=s[p1]
            break

<<<<<<< HEAD
print(decoded_string)
print(decoded_string == data)
=======
print(decoded_string)            
>>>>>>> 907d0a5f283985b49b1c2c91c29eef0ce348e23c
