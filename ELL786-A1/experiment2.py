from experiment1 import generate_random_binary_string, xor_binary_strings
from huffman_coding import huffman, huffman_decode, compute_codebook, extended_huffman_encode, huffman_encode
from repetition_code import rep_encode, rep_decode
from arithmetic_coding import generate_binary_code, arith_decode
from functools import reduce
from itertools import groupby


# divide input string s into parts of size k
# last part is of size <= k
def divide_str(s, k):
    parts = []
    i = 0
    n = len(s)
    while i < n:
        parts.append(s[i:i + k])
        i += k
    return parts


# computes probability of each symbol in the alphabet assuming sequence is valid representation of statistical redundancy
def compute_prob(s, alphabet):
    prob_list = []
    for a in alphabet:
        prob_list.append(s.count(a) / len(s))
    return prob_list


# computes probability of each symbol in the extended_alphabet of size 4 , given the alphabet set
def compute_prob_extended(s, extended_alphabet, alphabet):
    prob_list = []
    single_prob_list = compute_prob(s, alphabet)
    for [x, y, z, w] in extended_alphabet:
        prob_list.append(single_prob_list[alphabet.index(x)] * single_prob_list[alphabet.index(y)] *
                         single_prob_list[alphabet.index(z)] * single_prob_list[alphabet.index(w)])
    return prob_list


# compare differences in two string
def compare(s1, s2):
    n = len(s1)
    m = len(s2)
    c = 0
    for i in range(n):
        if i < m and s1[i] != s2[i]:
            c += 1
        elif i == m:
            c += n - m
            return c
    if n < m:
        c += m - n
    return c


k = 8
d = 5000

file = open('message.txt', 'r')
message = file.read()
file.close()

# divide the input string into chunks of size k (preferably a multiple of 4)
chunks = divide_str(message, k)  # k = 8

# alphabet set for each chunk
list_alphabet_set = [''.join(k for k, g in groupby(sorted(chunk))) for chunk in chunks]

# extended alphabet of size 4 for each corresponding chunk in chunks
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

# probs_huffman : probability of symbols in each alphabet set in list_alphabet_set given the sequence s
probs_huffman = [compute_prob(s, a_set) for s, a_set in zip(chunks, list_alphabet_set)]

# probs_extended_huffman : probability of symbols in each alphabet set in list_alphabet_set4 given the sequence s
probs_extended_huffman = [compute_prob_extended(s, ea_set, a_set)
                          for s, ea_set, a_set in zip(chunks, list_alphabet_set4, list_alphabet_set)]

# huffman_trees : computes huffman tree for each alphabet set in list_alphabet_set
huffman_trees = [huffman(a_set, p) for p, a_set in zip(probs_huffman, list_alphabet_set)]

# ehuffman_trees : computes huffman tree for each alphabet set in list_alphabet_set4
ehuffman_trees = [huffman(a_set, p) for p, a_set in zip(probs_extended_huffman, list_alphabet_set4)]

####################################

# Compute Error Correcting Compression Code

r = 5
# Huffman-Repetition Coding

chuffman_code = [huffman_encode(s, compute_codebook(a_set, tree))
                 for s, a_set, tree in zip(chunks, list_alphabet_set, huffman_trees)]
huffman_code = [rep_encode(h_code, r)
                for h_code in chuffman_code]

# Extended Huffman-Repetition Coding

cextended_huffman_code = [extended_huffman_encode(4, s, compute_codebook(ea_set, tree))
                          for s, tree, ea_set in zip(chunks, ehuffman_trees, list_alphabet_set4)]
extended_huffman_code = [rep_encode(eh_code, r) for eh_code in cextended_huffman_code]

# Arithmetic-Repetition Coding
# prob for arithmetic code is same as prob required for huffman

carithmetic_code = [generate_binary_code(s, a_set, p)
                    for s, a_set, p in zip(chunks, list_alphabet_set, probs_huffman)]
arithmetic_code = [rep_encode(a_code, r) for a_code in carithmetic_code]

# generate random error pattern with hamming weight d , such that non-zero entries are uniformly distributed

# Error pattern for huffman_code
error_pattern_huffman = generate_random_binary_string(reduce(lambda x, y: x + len(y), huffman_code, 0), d)

# Error pattern for extended_huffman_code
error_pattern_extended_huffman = generate_random_binary_string(
    reduce(lambda x, y: x + len(y), extended_huffman_code, 0), d)

# Error pattern for arithmetic_code
error_pattern_arithmetic = generate_random_binary_string(reduce(lambda x, y: x + len(y), arithmetic_code, 0), d)

# XOR the error pattern with encoded bits , call the obtained sequence y

# compute y for huffman_code
y_huffman = []
i1, j1 = 0, 0
n1 = len(error_pattern_huffman)
while i1 < n1:
    k1 = len(huffman_code[j1])
    y_huffman.append(xor_binary_strings(error_pattern_huffman[i1:i1 + k1], huffman_code[j1]))
    i1 += k1
    j1 += 1

# compute y for extended_huffman_code
y_extended_huffman = []
i2, j2 = 0, 0
n2 = len(error_pattern_extended_huffman)
while i2 < n2:
    k2 = len(extended_huffman_code[j2])
    y_extended_huffman.append(xor_binary_strings(error_pattern_extended_huffman[i2:i2 + k2], extended_huffman_code[j2]))
    i2 += k2
    j2 += 1

# compute y for arithmetic_code
y_arithmetic = []
i3, j3 = 0, 0
n3 = len(error_pattern_arithmetic)
while i3 < n3:
    k3 = len(arithmetic_code[j3])
    y_arithmetic.append(xor_binary_strings(error_pattern_arithmetic[i3:i3 + k3], arithmetic_code[j3]))
    i3 += k3
    j3 += 1

# using y retrieve the text file by decoding


# tuple of repetition error decoded file and number of errors corrected
huffman_rep_decode = [rep_decode(y_huffman_code, r) for y_huffman_code in y_huffman]

# Decompression Step
huffman_decoded = ""
huffman_corrected_errors = 0
for tree, e_decoded in zip(huffman_trees, huffman_rep_decode):
    huffman_decoded += huffman_decode(e_decoded[0], tree)
    huffman_corrected_errors += e_decoded[1]

# huffman_decoded is the text file received at the receiver end
# huffman_corrected_errors is the number of errors corrected


# tuple of repetition error decoded file and number of errors corrected
ehuffman_rep_decode = [rep_decode(y_ehuffman, r) for y_ehuffman in y_extended_huffman]

# Decompression Step
ehuffman_decoded = ""
ehuffman_corrected_errors = 0
for tree, e_decoded in zip(ehuffman_trees, ehuffman_rep_decode):
    ehuffman_decoded += huffman_decode(e_decoded[0], tree)
    ehuffman_corrected_errors += e_decoded[1]

# ehuffman_decoded is the text file received at the receiver end
# ehuffman_corrected_errors is the number of errors corrected


# tuple of repetition error decoded file and number of errors corrected
arith_rep_decode = [rep_decode(y_arith, r) for y_arith in y_arithmetic]

# Decompression Step
arith_decoded = ""
arith_corrected_errors = 0
for e_decoded, a_set, prob_model in zip(arith_rep_decode, list_alphabet_set, probs_huffman):
    arith_decoded += arith_decode(e_decoded[0], k, a_set, prob_model)
    arith_corrected_errors += e_decoded[1]

# arith_decoded is the text file received at the receiver end
# arith_corrected_errors is the number of errors corrected


print(f"For k = {k}, d = {d}, r = {r}")

len_message = len(message)

print("Number of corrected errors in Huffman ", huffman_corrected_errors)
print("Number of corrected errors in Extended Huffman ", ehuffman_corrected_errors)
print("Number of corrected errors in Arithmetic ", arith_corrected_errors)

print("% of modified characters in huffman coding", compare(message, huffman_decoded) / len_message * 100, "%")
print("% of modified characters in extended huffman coding", compare(message, ehuffman_decoded) / len_message * 100,
      "%")
print("% of modified characters in arithmetic coding", compare(message, arith_decoded) / len_message * 100, "%")
