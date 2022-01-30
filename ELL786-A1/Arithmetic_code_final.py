import math
import numpy as np


#string to encoded
x = "ramneek ramneek ramneek gfg"
#length of string to be encoded
k=len(x)

# string of unique characters
t=""
for i in range(k):
    if(t.find(x[i])==-1):
        t+=x[i]

# generating alphabet 
#alphabet is list of unique characters
alphabet=[t[0]]
for i in range(1,len(t)):
    alphabet.append(t[i])

# prob_model contains probability of each character
prob_model = np.zeros(len(t))
for i in range(len(t)):
    c = x.count(alphabet[i])
    prob_model[i] = c/k  

    
# pred function finds the predecessor of 'symbol a' in alphabet set
def pred(a, alphabet):
    
    n = len(alphabet)
    
    for i in range(n):
        if alphabet[i] == a:
            return i - 1

# compute_cdf function stores the cummulative distribution         
def compute_cdf(alphabet, prob_model):
    # cdf_dict is a dictionary with keys as symbols and values as cdf
    cdf_dict = dict()
    f = 0
    
    n = len(alphabet)
    
    for i in range(n):
        f += prob_model[i]
        cdf_dict[alphabet[i]] = f
    return cdf_dict


# generate_tags function finds the tag value
def generate_tag(x, alphabet, prob_model):
    
    # cdf_dict is a dictionary with keys as symbols and values as cdf
    cdf_dict = compute_cdf(alphabet, prob_model)
    n = len(x)
    _l = 0
    _u = 1
    
    for i in range(n):
        
        j = pred(x[i], alphabet)
        l = _l + (_u - _l) * cdf_dict[alphabet[j]] if j >= 0 else _l
        u = _l + (_u - _l) * cdf_dict[x[i]]

        _l = l
        _u = u
    return (_l + _u) / 2



def prob_seq(x, alphabet, prob_model):
    
    prob = 1.0
    for c in x:
        prob *= prob_model[alphabet.index(c)]
    return prob


# encode_tag function encode the tag
def encode_tag(tag, length):
    
    code = ""
    i = 0
    
    while tag != 0.0 and i < length:
        
        tag *= 2
        code += str(math.floor(tag))
        tag = tag - math.floor(tag)
        i += 1
    return code


def generate_binary_code(x, alphabet, prob_model):
    
    prob = prob_seq(x, alphabet, prob_model)
    
    tag = generate_tag(x, alphabet, prob_model)
    
    length = math.ceil(math.log(1 / prob, 2)) + 1
    return encode_tag(tag, length)


# decipher_tag function decipher the tag value
# k is the length of the sequence to be decipher
def decipher_tag(tag, k, cdf_dict):
    
    _l = 0
    _u = 1
    output = ""
    
    for k in range(k):
        t = (tag - _l)/(_u - _l)
        _f = 0    # value of f in prev iteration
        _s = ""   # value of s in prev iteration
        
        for s, f in cdf_dict.items():
            if _f <= t < f:
                output += s
                l = _l + (_u - _l) * cdf_dict[_s] if _s != "" else _l
                u = _l + (_u - _l) * cdf_dict[s]

                _l = l
                _u = u
                break
            else:
                _f = f
                _s = s
    return output


# arith_decode function decodes the binary string
# s is a binary string to be decoded
# k is length of original string in the message
def arith_decode(s, k, alphabet, prob_model):   
   
    tag = 0.0
    i = 1
    
    for c in s:
        if c == '1':
            tag += math.pow(2, -i)
        i += 1
        
    return decipher_tag(tag, k, compute_cdf(alphabet, prob_model))


print(generate_binary_code(s,alphabet,prob_model))
print(arith_decode("00000100000000001010010110101000110111011000101100110011",27,alphabet,prob_model))