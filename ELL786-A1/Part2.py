import numpy as np
import pywt
import matplotlib.image as image
import matplotlib.pyplot as plt
from PIL import Image as im


#Reading the input image-file of 512x512 and converting it into a matrix
img=image.imread('sample.gif')
print(img)


#Discrete_wavelet_transform function return the coeffs
#img is the input image
#k is the level of decomposition
def Discrete_wavelet_transform(img,k=3):
    coeffs = pywt.wavedec2(img, 'bior1.3',level=k)
    #LL,(LH,LV,LD)= coeffs
    return coeffs
    

'''for i in  range(258):
    for j in range(258):
        if(LL[i][j]<200):
            LL[i][j]=0
            
for i in  range(258):
    for j in range(258):
        if(LH[i][j]<0):
            LH[i][j]=0'''
                        
    
    
#Inverse_Discrete_wavelet_transform function returns image after compression
def Inverse_Discrete_wavelet_transform(coeffs):

    matrix = pywt.waverec2(coeffs, 'bior1.3')
    data = im.fromarray(matrix)
    data.save('dummy_pic.gif')
    data.show()

c = Discrete_wavelet_transform(img,k=3)
print(c)
print(c[0])
print(c[1][0])
print(c[1][1])
print(c[1][2])
print(c[2][0])
print(c[2][1])
print(c[2][2])
print(c[3][0])
print(c[3][1])
print(c[3][2])




Inverse_Discrete_wavelet_transform(Discrete_wavelet_transform(img,k=1))

'''fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()

pywt.idwt2(coeffs2, 'haar')'''
