from experiment1 import text_to_binary, generate_random_binary_string, xor_binary_strings, binarystring_textfile
from huffman_coding import huffman, huffman_decode, compute_codebook, extended_huffman_encode
from repetition_code import rep_encode, rep_decode
from arithmetic_coding import generate_binary_code, arith_decode
from functools import reduce


def divide_str(s, m):
    parts = []
    i = 0
    n = len(s)
    while i < n:
        parts.append(s[i:i+m])
        i += m
    return parts


# specifically for 16 letter alphabet set consisting of binary string of length 4
def compute_prob(s):
    p0 = s.count('0')/len(s)
    p1 = s.count('1')/len(s)
    return [p0*p0*p0*p0,p0*p0*p0*p1,p0*p0*p1*p0,p0*p0*p1*p1,p0*p1*p0*p0,p0*p1*p0*p1,p0*p1*p1*p0,p0*p1*p1*p1,
            p1*p0*p0*p0,p1*p0*p0*p1,p1*p0*p1*p0,p1*p0*p1*p1,p1*p1*p0*p0,p1*p1*p0*p1,p1*p1*p1*p0,p1*p1*p1*p1]


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


file = open('message.txt', 'r')
message = file.read()
file.close()

k = 52  # must be a multiple of 4
r = 5   # repetition value for repetition code
d = 2000

# read the input file and convert it into a binary string
message_bin = text_to_binary(message)

# divide the input string into chunks of size k bits
chunks = divide_str(message_bin, k)

# Preparation for decompression

ehuffman_alphabet_set = ['0000','0001','0010','0011','0100','0101','0110','0111',
                         '1000','1001','1010','1011','1100','1101','1110','1111']

probs_ehuffman = [compute_prob(s) for s in chunks]
ehuffman_trees = [huffman(ehuffman_alphabet_set, p) for p in probs_ehuffman]

probs_arith = [[s.count('0')/len(s), s.count('1')/len(s)] for s in chunks]

# encode each chunk using huffman,extended huffman,arithmetic codes

chuffman_code = chunks
huffman_code = [rep_encode(h_code, r) for h_code in chuffman_code]

cextended_huffman_code = [extended_huffman_encode(4, s, compute_codebook(ehuffman_alphabet_set, tree)) for s, tree in zip(chunks, ehuffman_trees)]
extended_huffman_code = [rep_encode(eh_code, r) for eh_code in cextended_huffman_code]

carithmetic_code = [generate_binary_code(s, ['0', '1'], p) for s, p in zip(chunks, probs_arith)]
arithmetic_code = [rep_encode(a_code, r) for a_code in carithmetic_code]

# generating random error pattern with hamming weight d , such that non-zero entries are uniformly distributed

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
for e_decoded in huffman_rep_decode:
    huffman_decoded += e_decoded[0]  # huffman coding of a binary string is the string itself
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
for e_decoded, prob_model in zip(arith_rep_decode, probs_arith):
    arith_decoded += arith_decode(e_decoded[0], k, ['0', '1'], prob_model)
    arith_corrected_errors += e_decoded[1]

# arith_decoded is the text file received at the receiver end
# arith_corrected_errors is the number of errors corrected

# retrieving the text file

text_huffman = binarystring_textfile(huffman_decoded)
text_ehuffman = binarystring_textfile(ehuffman_decoded)
text_arithmetic = binarystring_textfile(arith_decoded)


print(f"For k = {k}, d = {d}, r = {r}")

len_message = len(message_bin)  # length of binary message

print("Compression ratio for Huffman Coding ", reduce(lambda a, b: a+len(b), chuffman_code, 0)/len_message)
print("Compression ratio for Extended Huffman Coding ", reduce(lambda a, b: a+len(b), cextended_huffman_code, 0)/len_message)
print("Compression ratio for Arithmetic Coding ", reduce(lambda a, b: a+len(b), carithmetic_code, 0)/len_message)

print("Number of corrected errors in Huffman ", huffman_corrected_errors)
print("Number of corrected errors in Extended Huffman ", ehuffman_corrected_errors)
print("Number of corrected errors in Arithmetic ", arith_corrected_errors)

len_tmessage = len(message)  # length of text message

print("% of modified characters in huffman coding", compare(message, text_huffman) / len_tmessage * 100, "%")
print("% of modified characters in extended huffman coding", compare(message, text_ehuffman) / len_tmessage * 100,
      "%")
print("% of modified characters in arithmetic coding", compare(message, text_arithmetic) / len_tmessage * 100, "%")
