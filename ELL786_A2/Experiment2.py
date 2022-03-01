import numpy as np
from PIL import Image


# encoding function takes string and initial dictionary as input and encodes the string
# d0 is the initial dictionary primed with the alphabet set

Dict = dict()
for i in range(256):
    t = ""
    t += chr(i)
    Dict[t] = i+1
Dict['clear_code'] = 257
Dict['EOF'] = 258
 

def encoding(s, d0):
    
    code_table = d0
    n = len(s)
    p = ''
    
    s1=""
    k = len(d0)+1
    for i in range(n):
        c = s[i]
        
        if p + c not in code_table:
            code_table[p + c] = k
            
            # increasing pointer length by one as the dictionary size doubles 
            if(k<512):
                s1+=('{0:09b}'.format(code_table[p]))
            elif(k>=512  and k<1024):
                s1+=('{0:010b}'.format(code_table[p]))
            elif(k>=1024 and k<2048):
                s1+=('{0:011b}'.format(code_table[p]))
            elif(k>=2048 and k<4096):
                s1+=('{0:012b}'.format(code_table[p]))
                
            
            p = c
            k += 1
            
            # when dictionary size gets equal to 4096 then discard the prev dictionary
            # and start a new dictionary
            
            if(k == 4096):
                Dict = dict()
                for i in range(256):
                    t = ""
                    t += chr(i)
                    Dict[t] = i+1
                Dict['clear_code'] = 257
                Dict['EOF'] = 258
                code_table = Dict
                s1 += (bin(257))[2:]
                k = 259
                p = ''
               
        else:
            p += c
    
 
    if(k<512):
        s1+=('{0:09b}'.format(code_table[p]))
    elif(k>=512 and k<1024):
        s1+=('{0:010b}'.format(code_table[p]))
    elif(k>=1024 and k<2048):
        s1+=('{0:011b}'.format(code_table[p]))
    elif(k>=2048 and k<4096):
        s1+=('{0:012b}'.format(code_table[p]))
        
    s1+=(bin(258))[2:]
    return s1

#############################################################
  
#for encoding image and finding compression ratio

#Reading image form bmp format
image = Image.open("sample.bmp")
img = np.array(image).flatten()

#converting the bmp format image into binary string
m = ''.join(['{0:08b}'.format(num) for num in img])
print(len(m))

#code is the generated codes by encoding
code = encoding(m, Dict)
print(len(code))

#finding compression ratio
print("compression_ratio",(len(m))/len(code))

