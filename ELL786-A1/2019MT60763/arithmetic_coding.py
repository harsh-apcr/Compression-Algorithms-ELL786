import math


# finds the predecessor of 'symbol a' in alphabet set
def pred(a, alphabet):
    n = len(alphabet)
    for i in range(n):
        if alphabet[i] == a:
            return i - 1


# computes cdf for each symbol in the alphabet set
# alphabet - alphabet set
# prob_model - probability of each symbol in the alphabet
def compute_cdf(alphabet, prob_model):
    cdf_dict = dict()
    f = 0
    n = len(alphabet)
    for i in range(n):
        f += prob_model[i]
        cdf_dict[alphabet[i]] = f
    return cdf_dict


# generates tag for a sequence of symbols
# x - sequence for which to generate tag for
# alphabet - alphabet_set
# prob_model - probability of each symbol in the alphabet
def generate_tag(x, alphabet, prob_model):
    # x is a sequence of symbols (to encode)
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


# returns probability of a sequence
# s - sequence for which to compute probability for
# alphabet - alphabet set
# prob_model - probability of each symbol in the alphabet
def prob_seq(s, alphabet, prob_model):
    prob = 1.0
    for c in s:
        prob *= prob_model[alphabet.index(c)]
    return prob


# encoding tag into binary up to "length" many bits
# 0<=tag<1
def encode_tag(tag, length):
    code = ""
    i = 0
    while tag != 0.0 and i < length:
        tag *= 2
        code += str(math.floor(tag))
        tag = tag - math.floor(tag)
        i += 1
    if len(code) < length:
        code += "0"*(length - len(code))
    return code


# generates binary code for a sequence x with given alphabet set and probability model
def generate_binary_code(x, alphabet, prob_model):
    # tag value and probability of the sequence
    prob = prob_seq(x, alphabet, prob_model)
    tag = generate_tag(x, alphabet, prob_model)
    length = math.ceil(math.log(1 / prob, 2)) + 1
    return encode_tag(tag, length)


# decipher the tag value
# k: length of the sequence to decipher
# cdf_dict: dictionary of the (letter, cdf) pair
def decipher_tag(tag, k, cdf_dict):
    _l = 0
    _u = 1
    output = ""
    for i in range(k):
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


# decode a binary sequence s using arithmetic decoding given k is original sequence length
def arith_decode(s, k, alphabet, prob_model):   # k is length of original string in the message
    # s is a binary string
    tag = 0.0
    i = 1
    for c in s:
        if c == '1':
            tag += math.pow(2, -i)
        i += 1
    return decipher_tag(tag, k, compute_cdf(alphabet, prob_model))

