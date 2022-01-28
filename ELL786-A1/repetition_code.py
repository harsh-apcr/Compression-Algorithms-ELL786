
# r must preferably an odd number
# transmitter side
def rep_encode(s, r):
    # s is binary string to encode
    # r is the value that is agreed commonly between transmitter and receiver
    output = ""
    for c in s:
        output += c*r
    return output


# receiver side
# decode using majority rule
def rep_decode(s, r):
    i = 0
    n = len(s)
    output = ""
    while i < n:
        if s.count('0', i, i+r) > r//2:
            output += '0'
        else:
            # even if s.count('0',i,i+r) == r/2 (in case r is even) then '1' is taken
            output += '1'
        i += r
    return output

