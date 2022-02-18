def encoding(s):
    Dict = dict()
    n = len(s)
    for i in range(256):
        t = ""
        t += chr(i)
        Dict[t] = i
    p =""
    c =""
    p += s[0]
    k = 256
    list = []
    for i  in range(n):
        if (i != n- 1):
            c += s[i + 1];
        if (p+c in Dict): 
            p = p + c
        else:
            list.append(Dict[p])
            Dict[p+c] = k
            k+=1
            p=c
        c=""
    list.append(Dict[p])  
    
    return list


def decoding(v):
    Dict = dict()
    k =""
    for i in range(256):
        t = ""
        t += chr(i)
        Dict[i] = t
        
    old = v[0]
    s=Dict[old]
    c=""
    c+=s[0]
    k+=s
    count=256
    for i  in range(len(v)-1):
        n=v[i+1]
        if ((n in Dict)==False): 
            s = Dict[old]
            s = s + c
        else:
            s = Dict[n] 
        k+=s 
        c=""
        c+=s[0]
        Dict[count] = Dict[old]+c
        count+=1
        old = n
    return k

print(encoding("00011100"))
print(decoding(encoding("00011100")))
        
        