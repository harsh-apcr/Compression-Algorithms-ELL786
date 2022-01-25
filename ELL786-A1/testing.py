import huffman_coding

tree = huffman_coding.huffman(['a', 'b', 'c', 'd', 'e'], [0.2, 0.4, 0.2, 0.1, 0.1])
code_words = {'a': '', 'b': '', 'c': '', 'd': '', 'e': ''}
huffman_coding.generate_codewords("", tree, code_words)
print(code_words)
print(huffman_coding.decode("1011110101010001010110101001011011011010111", tree))