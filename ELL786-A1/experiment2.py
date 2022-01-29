from experiment1 import text_to_binary, generate_random_binary_string, xor_binary_strings, binarystring_textfile
from huffman_coding import huffman, huffman_decode, compute_codebook, extended_huffman_encode
from repetition_code import rep_encode, rep_decode
from arithmetic_coding import generate_binary_code, arith_decode
from functools import reduce


def divide_str(s, k):
    parts = []
    i = 0
    n = len(s)
    while i < n:
        parts.append(s[i:i + k])
        i += k
    return parts


# specifically for 16 letter alphabet set consisting of binary string of length 4
def compute_prob(s):
    p0 = s.count('0') / len(s)
    p1 = s.count('1') / len(s)
    return [p0 * p0 * p0 * p0, p0 * p0 * p0 * p1, p0 * p0 * p1 * p0, p0 * p0 * p1 * p1, p0 * p1 * p0 * p0,
            p0 * p1 * p0 * p1, p0 * p1 * p1 * p0, p0 * p1 * p1 * p1,
            p1 * p0 * p0 * p0, p1 * p0 * p0 * p1, p1 * p0 * p1 * p0, p1 * p0 * p1 * p1, p1 * p1 * p0 * p0,
            p1 * p1 * p0 * p1, p1 * p1 * p1 * p0, p1 * p1 * p1 * p1]


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

# read the input file and convert it into a binary string
message_bin = text_to_binary(message)

# divide the input string into chunks of size k bits
chunks = divide_str(message_bin, 16)  # k = 16

# encode each chunk using huffman,extended huffman,arithmetic codes
huffman_code = [rep_encode(s, 5) for s in chunks]

###
alphabet_set = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
                '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']

probs_huffman = [compute_prob(s) for s in chunks]
probs_arith = [[s.count('0') / len(s), s.count('1') / len(s)] for s in chunks]

huffman_trees = [huffman(alphabet_set, p) for p in probs_huffman]   # for extended huffman
###

extended_huffman_code = [rep_encode(extended_huffman_encode(4, s, compute_codebook(alphabet_set, tree)), 5) for s, tree
                         in zip(chunks, huffman_trees)]

arithmetic_code = [rep_encode(generate_binary_code(s, ['0', '1'], p), 9) for s, p in zip(chunks, probs_arith)]

# generate random error pattern with hamming weight d , such that non-zero entries are uniformly distributed

# d = 10
error_pattern_huffman = generate_random_binary_string(reduce(lambda x, y: x + len(y), huffman_code, 0), 10)

error_pattern_extended_huffman = generate_random_binary_string(
    reduce(lambda x, y: x + len(y), extended_huffman_code, 0), 10)

error_pattern_arithmetic = generate_random_binary_string(reduce(lambda x, y: x + len(y), arithmetic_code, 0), 10)

# XOR the error pattern with encoded bits , call the obtained sequence y

y_huffman = xor_binary_strings(error_pattern_huffman, reduce(lambda x, y: x + y, huffman_code, ""))

y_extended_huffman = xor_binary_strings(error_pattern_extended_huffman,
                                        reduce(lambda x, y: x + y, extended_huffman_code, ""))

y_arithmetic = xor_binary_strings(error_pattern_arithmetic, reduce(lambda x, y: x + y, arithmetic_code, ""))

# using y retrieve the text file by decoding
huffman_rep_decode, huffman_error_corrected = rep_decode(y_huffman, 5)
huffman_decoded = reduce(lambda x, y: x + y, divide_str(huffman_rep_decode, 16), "")
# huffman_decode(y) = y (y is a binary string)

# extended_huffman_rep_decode, extended_huffman_error_corrected = rep_decode(y_extended_huffman, 5)
# extended_huffman_decoded = reduce(lambda x, y: x + huffman_decode(*y),
#                                   zip(divide_str(extended_huffman_rep_decode, 16), huffman_trees), "")

arithmetic_rep_decode, arithmetic_error_corrected = rep_decode(y_arithmetic, 9)
arithmetic_decoded = reduce(lambda x, y: x + arith_decode(y[0], len(y[1]), ['0', '1'], y[2]),
                            zip(divide_str(arithmetic_rep_decode, 16), chunks, probs_arith), "")

# Number of error corrected / detected


message_huffman = binarystring_textfile(huffman_decoded)
# message_extended_huffman = binarystring_textfile(extended_huffman_decoded)
message_arithmetic = binarystring_textfile(arithmetic_decoded)

print(arithmetic_code)
