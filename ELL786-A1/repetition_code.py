

# rep_encode function takes string and integer as an argument and encodes it
# s is binary string to encode
# r is the value that is agreed commonly between transmitter and receiver
# r must preferably an odd number

def rep_encode(s, r):
    
    output = ""
    for c in s:
        output += c*r
        
    return output


# rep_decode function takes string and integer as an argument and decodes it
# s is binary string to encode
# r is the value that is agreed commonly between transmitter and receiver
# decoding using majority rule

def rep_decode(s, r):
    
    i = 0
    n = len(s)
    
    output = ""
    errors_corrected = 0
    while i < n:
        count0 = s.count('0', i, i+r)
        if count0 > r//2:
            output += '0'
        #else append 1
        else:
           
            output += '1'
        i += r
        errors_corrected += 1 if count0 != r else 0
    return output, errors_corrected

