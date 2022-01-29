from experiment1 import text_to_binary, generate_random_binary_string, xor_binary_strings, binarystring_textfile
from huffman_coding import huffman, huffman_decode, compute_codebook, extended_huffman_encode, huffman_encode
from repetition_code import rep_encode, rep_decode
from arithmetic_coding import generate_binary_code, arith_decode
from functools import reduce
from itertools import groupby


def divide_str(s, k):
    parts = []
    i = 0
    n = len(s)
    while i < n:
        parts.append(s[i:i + k])
        i += k
    return parts


def compute_prob(s, alphabet):
    prob_list = []
    for a in alphabet:
        prob_list.append(s.count(a) / len(s))
    return prob_list


def compute_prob_extended(s, extended_alphabet, alphabet):
    prob_list = []
    single_prob_list = compute_prob(s, alphabet)
    for [x, y, z, w] in extended_alphabet:
        prob_list.append(single_prob_list[alphabet.index(x)] * single_prob_list[alphabet.index(y)] *
                         single_prob_list[alphabet.index(z)] * single_prob_list[alphabet.index(w)])
    return prob_list


# compare differences in two string of same sizes
def compare(s1, s2):
    n = len(s1)
    c = 0
    for i in range(n):
        if s1[i] != s2[i]:
            c += 1
    return c


file = open('message.txt', 'r')
message = file.read()
file.close()

# divide the input string into chunks of size k
chunks = divide_str(message, 16)  # k = 16

# alphabet set for each chunk
list_alphabet_set = [''.join(k for k, g in groupby(sorted(chunk))) for chunk in chunks]

# extended alphabet of size 4
list_alphabet_set4 = []
for alphabet in list_alphabet_set:
    alphabet_set4 = []
    for x in alphabet:
        for y in alphabet:
            for z in alphabet:
                for w in alphabet:
                    alphabet_set4.append([x, y, z, w])
    list_alphabet_set4.append(alphabet_set4)

# encode each chunk using huffman,extended huffman,arithmetic codes (data compression)

#####################################
probs_huffman = [compute_prob(s, a_set) for s, a_set in zip(chunks, list_alphabet_set)]
probs_extended_huffman = [compute_prob_extended(s, ea_set, a_set)
                          for s, ea_set, a_set in zip(chunks, list_alphabet_set4, list_alphabet_set)]

huffman_trees = [huffman(a_set, p) for p, a_set in zip(probs_huffman, list_alphabet_set)]
ehuffman_trees = [huffman(a_set, p) for p, a_set in zip(probs_extended_huffman, list_alphabet_set4)]
####################################


huffman_code = [rep_encode(huffman_encode(s, compute_codebook(a_set, tree)), 5)
                for s, a_set, tree in zip(chunks, list_alphabet_set, huffman_trees)]

extended_huffman_code = [rep_encode(extended_huffman_encode(4, s, compute_codebook(ea_set, tree)), 5)
                         for s, tree, ea_set in zip(chunks, ehuffman_trees, list_alphabet_set4)]

# prob for arithmetic code is same as prob required for huffman
arithmetic_code = [rep_encode(generate_binary_code(s, a_set, p), 5)
                   for s, a_set, p in zip(chunks, list_alphabet_set, probs_huffman)]


# generate random error pattern with hamming weight d , such that non-zero entries are uniformly distributed
# d = 10

error_pattern_huffman = generate_random_binary_string(reduce(lambda x, y: x + len(y), huffman_code, 0), 10)

error_pattern_extended_huffman = generate_random_binary_string(
    reduce(lambda x, y: x + len(y), extended_huffman_code, 0), 10)

error_pattern_arithmetic = generate_random_binary_string(reduce(lambda x, y: x + len(y), arithmetic_code, 0), 10)

# XOR the error pattern with encoded bits , call the obtained sequence y
y_huffman = []
i1, j1 = 0, 0
n1 = len(error_pattern_huffman)
while i1 < n1:
    k1 = len(huffman_code[j1])
    y_huffman.append(xor_binary_strings(error_pattern_huffman[i1:i1+k1], huffman_code[j1]))
    i1 += k1
    j1 += 1


y_extended_huffman = []
i2, j2 = 0, 0
n2 = len(error_pattern_extended_huffman)
while i2 < n2:
    k2 = len(extended_huffman_code[j2])
    y_extended_huffman.append(xor_binary_strings(error_pattern_extended_huffman[i2:i2+k2], extended_huffman_code[j2]))
    i2 += k2
    j2 += 1


y_arithmetic = []
i3, j3 = 0, 0
n3 = len(error_pattern_arithmetic)
while i3 < n3:
    k3 = len(arithmetic_code[j3])
    y_arithmetic.append(xor_binary_strings(error_pattern_arithmetic[i3:i3+k3], arithmetic_code[j3]))
    i3 += k3
    j3 += 1

# using y retrieve the text file by decoding

huffman_rep_decode = [rep_decode(y_huffman_code, 5) for y_huffman_code in y_huffman]
# pair of error decoded file and number of errors corrected

huffman_decoded = ""
huffman_corrected_errors = 0
for tree, e_decoded in zip(huffman_trees, huffman_rep_decode):
    huffman_decoded += huffman_decode(e_decoded[0], tree)
    huffman_corrected_errors += e_decoded[1]


ehuffman_rep_decode = [rep_decode(y_ehuffman, 5) for y_ehuffman in y_extended_huffman]
ehuffman_decoded = ""
ehuffman_corrected_errors = 0
for tree, e_decoded in zip(ehuffman_trees, ehuffman_rep_decode):
    ehuffman_decoded += huffman_decode(e_decoded[0], tree)
    ehuffman_corrected_errors += e_decoded[1]


arith_rep_decode = [rep_decode(y_arith, 5) for y_arith in y_arithmetic]
arith_decoded = ""
arith_corrected_errors = 0
for e_decoded, a_set, prob_model in zip(arith_rep_decode, list_alphabet_set, probs_huffman):
    arith_decoded += arith_decode(e_decoded[0], 16, a_set, prob_model)
    arith_corrected_errors += e_decoded[1]

print(arith_decoded)

# arithmetic_decoded = reduce(lambda x, y: x + arith_decode(y[0], len(y[1]), ['0', '1'], y[2]),
#                             zip(divide_str(arithmetic_rep_decode, 16), chunks, probs_arith), "")
#
# # Number of error corrected / detected
#
# print(arithmetic_code)
