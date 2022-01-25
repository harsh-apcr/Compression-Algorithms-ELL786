import heapq


class Letter:

    # symbol : symbol of an alphabet
    # freq : statistical freq of the symbol
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __str__(self):
        return self.symbol

    def get_left(self):
        return self.left

    def set_left(self, letter):
        self.left = letter

    def get_right(self):
        return self.right

    def set_right(self, letter):
        self.right = letter

    def is_leaf(self):
        return self.left is None and self.right is None


# returns coding tree
def huffman(alphabet, prob_model):
    letter_list = []
    n = len(alphabet)
    for i in range(n):
        letter_list.append(Letter(alphabet[i], prob_model[i]))

    heapq.heapify(letter_list)
    while len(letter_list) != 1:
        l1 = heapq.heappop(letter_list)
        l2 = heapq.heappop(letter_list)

        l3 = Letter(l1.symbol + l2.symbol, l1.freq + l2.freq)
        l3.set_left(l1)
        l3.set_right(l2)

        heapq.heappush(letter_list, l3)

    # len(letter_list) == 1
    return letter_list[0]


# generating codewords

def generate_codewords(prefix, coding_tree, letter_codeword_dict):
    if coding_tree.is_leaf():
        letter_codeword_dict[coding_tree.symbol] = prefix

    else:
        generate_codewords(prefix + '0', coding_tree.get_left(), letter_codeword_dict)
        generate_codewords(prefix + '1', coding_tree.get_right(), letter_codeword_dict)


def decode(s, coding_tree):
    # s is a binary string
    # coding tree must not be empty
    letter_node = coding_tree
    output = ""
    for c in s:
        if c == '0':
            letter_node = letter_node.get_left()
        else:
            letter_node = letter_node.get_right()
        if letter_node.is_leaf():
            output = output + letter_node.__str__()
            letter_node = coding_tree  # back to the root

    if letter_node != coding_tree:
        return False    # message is not decodable with given alphabet set
    return output



