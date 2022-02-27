import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import zlib

#Reading image form bmp format
image = Image.open("sample.bmp")
img = np.array(image).flatten()

#converting the bmp format image into binary string
m = ''.join(['{0:08b}'.format(num) for num in img])
print(len(m))

#compression using png encoder
new_string = bytearray(m,"ascii")
p = zlib.compress(new_string,level=9)
print(len(p))

print("compression_ratio",(len(m)-len(p))/len(m))
