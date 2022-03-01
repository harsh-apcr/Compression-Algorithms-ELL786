import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# encoding function takes string and initial dictionary as input and encodes the string
# d0 is the initial dictionary primed with the alphabet set
# the alphabet set keys must start from 1 to its length with increments of 1

def encoding(s, d0):

    code_table = d0
    n = len(s)
    p = ''
    
    code_stream = []
    k = len(d0)+1
    
    for i in range(n):
        c = s[i]
        
        if p + c not in code_table:
            code_table[p + c] = k
            code_stream.append(code_table[p])
            p = c
            k += 1
        else:
            p += c
    
    #printing dictionary
    #print((code_table))
    code_stream.append(code_table[p])
    return code_stream

# decoding function takes codes and initial dictionary as input and decodes the string

def decoding(v, d0):

    # invert d0 mapping
    Dict = {v: k for k, v in d0.items()}
    
    k = ""
    old = v[0]
    s = Dict[old]
    c = ""
    c += s[0]
    k += s
    
    count = len(d0)+1
    
    for i in range(len(v) - 1):
        n = v[i + 1]
        
        if n not in Dict:
            s = Dict[old]
            s = s + c
        else:
            s = Dict[n]
        k += s
        c = ""
        c += s[0]
        Dict[count] = Dict[old] + c
        count += 1
        old = n
        
    return k
    
    
#############################################################
  
#for encoding message "a·bar·array·by·barrayar·bay"

#initial dictionary of letters a,b,r,y,·
d = {"a": 1,"b": 2,"r":3,"y":4,"·":5}
#message to be encoded
m = "a·bar·array·by·barrayar·bay"
code = encoding(m, d)
print(code)
m_dec = decoding(code, d)
print(m_dec == m)



#for encoding image and finding compression ratio

#Reading image form bmp format
image = Image.open("sample.bmp")
img = np.array(image).flatten()

#converting the bmp format image into binary string
m = ''.join(['{0:08b}'.format(num) for num in img])
print(len(m))

#initial dictionary containes only 0 and 1
d = {"0": 1,"1": 2}

#code is the generated codes by encoding
code = encoding(m, d)

#finding compression ratio

#converting codes into binary format
#print(max(code))
p = ''.join(['{0:020b}'.format(num) for num in code])
print(len(p))


print("compression_ratio",(len(m))/len(p))

m_dec = decoding(code, d)
print(m_dec == m)