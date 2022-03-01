import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import zlib
from functools import reduce

# Reading image form bmp format
image = Image.open("sample.bmp")
img = np.array(image).flatten()

# converting the bmp format image into binary string
m = ''.join(['{0:08b}'.format(num) for num in img])
print(len(m))

# compression using png encoder
new_string = bytearray(m, "ascii")
p = zlib.compress(new_string, level=9)

p_len = reduce(lambda x, y: x+len(bin(y)[2:]), p, 0)
print(p_len)

print("compression_ratio", len(m) / p_len)