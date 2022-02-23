import math


def int_binary(r, k):
    res = ''
    while k != 0:
        res = str(r % 2) + res
        r = r // 2
        k -= 1
    return res


def unary_code(q):
    # unary code of q
    return '1' * q + '0'


def codeword_remainder(r, m):
    if 0 <= r <= int(math.pow(2, math.ceil(math.log2(m)))) - m - 1:
        return int_binary(r, int(math.floor(math.log2(m))))
    else:
        return int_binary(r + int(math.pow(2, math.ceil(math.log2(m)))) - m, math.ceil(math.log2(m)))


def golomb_encode(m, n):
    q = n // m
    r = n % m
    return unary_code(q) + codeword_remainder(r, m)


def golomb_power_of_two(y, k):
    return unary_code(y >> k) + int_binary(y & ((1 << k) - 1), k)


# b = math.ceil(log2(M)) , where M is the alphabet-set size
# L - maximum codeword length
# constraint: L > b+1
def modified_GPO2(y, k, b, L):
    q = y >> k
    q_max = L-b-1
    if q < q_max:
        return golomb_power_of_two(y, k)
    else:
        return unary_code(q_max)+int_binary(y-1, b)
