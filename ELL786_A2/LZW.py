
# d0 : initial dictionary primed with the alphabet set
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

    code_stream.append(code_table[p])
    return code_stream


def decoding(v, d0):
    # invert d0 mapping
    Dict = {v: k for k, v in d0.items()}
    # dictionary with keys as integers
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


# initial dictionary must be same both at the encoder as well at the decoder side
m = "abababababababa"
d = {" ": 1,
     "a": 2,
     "b": 3,
     "o": 4,
     "w": 5}

code = encoding(m, d)
print(code)
m_dec = decoding(code, d)
print(m_dec)
print(m_dec == m)