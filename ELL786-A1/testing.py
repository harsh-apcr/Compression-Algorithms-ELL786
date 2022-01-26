import huffman_coding, arithmetic_coding
import math
tree = huffman_coding.huffman(['a', 'b', 'c', 'd', 'e'], [0.2, 0.4, 0.2, 0.1, 0.1])
code_words = {'a': '', 'b': '', 'c': '', 'd': '', 'e': ''}
huffman_coding.generate_codewords("", tree, code_words)
print(code_words)
print(huffman_coding.decode("1011110101010001010110101001011011011010111", tree))

message = "aabacbababacabcabca"
code = arithmetic_coding.generate_binary_code(message, ['a', 'b', 'c'], [0.8, 0.02, 0.18])
print(code)

decipher = arithmetic_coding.arith_decode(code, len(message), ['a', 'b', 'c'], [0.8, 0.02, 0.18])
print(decipher)
print(decipher == message)


