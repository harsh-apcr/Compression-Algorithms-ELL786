import numpy as np
import pywt
import matplotlib.image as image
import matplotlib.pyplot as plt
from PIL import Image as im


#Reading the input image-file of 512x512 and converting it into a matrix
img=image.imread('sample.gif')
print(img)

#calculating the averge energy of subband
def average_energy_subband(matrix):
    s=0
    m,n = matrix.shape
    for i in range(m):
        for j in range(m):
           s+=((matrix[i][j])*(matrix[i][j]))
    return np.sqrt(s/(m*m))

#pruning the matrix
def pruning(matrix,thresolds):
    m,n = matrix.shape
    for i in range(m):
        for j in range(m):
           if(matrix[i][j]<thresolds):
              matrix[i][j]=0
    return matrix

#setting matrix to zero
def set_to_zero(matrix):
    m,n = matrix.shape
    for i in range(m):
        for j in range(m):
            matrix[i][j]=0
    return matrix
    

#restoring top k elements of a matrix
def restore(matrix,k):
    m,n = matrix.shape
    p = np.zeros((m*m,3))
    for i in range(m):
        for j in range(m):
            p[j+i*m][0] = matrix[i][j] 
            p[j+i*m][1] = i
            p[j+i*m][2] = j
    p[p[:, 0].argsort()]
    for i in range(k,m*m):
        matrix[int(p[i][1])][int(p[i][2])] = 0
    return matrix


###################### for k =1 ###################3
'''coeffs = pywt.wavedec2(img, 'db1',level=1)
LL,(LH,HL,HH)= coeffs
 
   
ELL = average_energy_subband(LL) # comes out to be 194.95
ELH = average_energy_subband(LH) # comes out to be 12.58
EHL = average_energy_subband(HL) # comes out to be 15.89
EHH = average_energy_subband(HH) # comes out to be 7.09'''

#Setting thresolds values
'''#Setting thresolds as 194 , 12 , 15 , 7
LL = pruning(LL,194)
LH = pruning(LH,12)
HL = pruning(HL,15)
HH = pruning(HH,7)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic1.gif')
data.show()'''

#Now halfing thresolds 
'''LL = pruning(LL,194)
LH = pruning(LH,12)
HL = pruning(HL,15)
HH = pruning(HH,3.5)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic2.gif')
data.show()'''

'''LL = pruning(LL,194)
LH = pruning(LH,12)
HL = pruning(HL,7.5)
HH = pruning(HH,3.5)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic3.gif')
data.show()'''

'''LL = pruning(LL,194)
LH = pruning(LH,6)
HL = pruning(HL,7.5)
HH = pruning(HH,3.5)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic4.gif')
data.show()'''

#By changing thresolds of LH,HH,HL we will observe that there is not much changes in the image so we can prune these completely and varies the thresolds for LL
'''LL = pruning(LL,97)
LH = set_to_zero(LH)
HL = set_to_zero(HL)
HH = set_to_zero(HH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic5.gif')
data.show()'''

'''LL = pruning(LL,50)
LH = set_to_zero(LH)
HL = set_to_zero(HL)
HH = set_to_zero(HH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic6.gif')
data.show()'''

'''=LL = pruning(LL,40)
LH = set_to_zero(LH)
HL = set_to_zero(HL)
HH = set_to_zero(HH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic7.gif')
data.show()'''


'''LL = pruning(LL,30)
LH = set_to_zero(LH)
HL = set_to_zero(HL)
HH = set_to_zero(HH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic8.gif')
data.show()'''

'''LL = pruning(LL,10)
LH = set_to_zero(LH)
HL = set_to_zero(HL)
HH = set_to_zero(HH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic9.gif')
data.show()'''


###################### for k =2 ###################3
'''coeffs = pywt.wavedec2(img, 'db1',level=2)
LL,(LH,HL,HH),(LH1,HL1,HH1)= coeffs
 
   
ELL = average_energy_subband(LL)   # comes out to be 392.09
ELH = average_energy_subband(LH)   # comes out to be 31.4
EHL = average_energy_subband(HL)   # comes out to be 40.64
EHH = average_energy_subband(HH)   # comes out to be 18.74
ELH1 = average_energy_subband(LH1) # comes out to be 12.58
EHL1 = average_energy_subband(HL1) # comes out to be 15.89
EHH1 = average_energy_subband(HH1) # comes out to be 7.09'''


#Setting thresolds values
#Setting thresolds as 392,31,40,18,12,16,7
'''LL = pruning(LL,392)
LH = pruning(LH,31)
HL = pruning(HL,40)
HH = pruning(HH,18)
LH1 = pruning(LH1,12)
HL1 = pruning(HL1,16)
HH1 = pruning(HH1,7)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic10.gif')
data.show()'''

#Now halfing thresolds 
'''LL = pruning(LL,392/2)
LH = pruning(LH,31/2)
HL = pruning(HL,40/2)
HH = pruning(HH,18/2)
LH1 = pruning(LH1,12/2)
HL1 = pruning(HL1,16/2)
HH1 = pruning(HH1,7/2)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic11.gif')
data.show()'''

'''LL = pruning(LL,392/4)
LH = pruning(LH,31/4)
HL = pruning(HL,40/4)
HH = pruning(HH,18/4)
LH1 = pruning(LH1,12/4)
HL1 = pruning(HL1,16/4)
HH1 = pruning(HH1,7/4)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic12.gif')
data.show()

LL = pruning(LL,392/8)
LH = pruning(LH,31/8)
HL = pruning(HL,40/8)
HH = pruning(HH,18/8)
LH1 = pruning(LH1,12/8)
HL1 = pruning(HL1,16/8)
HH1 = pruning(HH1,7/8)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic13.gif')
data.show()

LL = pruning(LL,392/16)
LH = pruning(LH,31/16)
HL = pruning(HL,40/16)
HH = pruning(HH,18/16)
LH1 = pruning(LH1,12/16)
HL1 = pruning(HL1,16/16)
HH1 = pruning(HH1,7/16)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic14.gif')
data.show()'''

'''LL = pruning(LL,392/32)
LH = pruning(LH,31/32)
HL = pruning(HL,40/32)
HH = pruning(HH,18/32)
LH1 = pruning(LH1,12/32)
HL1 = pruning(HL1,16/32)
HH1 = pruning(HH1,7/32)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic15.gif')
data.show()'''

'''LL = pruning(LL,392/64)
LH = pruning(LH,31/64)
HL = pruning(HL,40/64)
HH = pruning(HH,18/64)
LH1 = pruning(LH1,12/64)
HL1 = pruning(HL1,16/64)
HH1 = pruning(HH1,7/64)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic16.gif')
data.show()'''

'''LL = pruning(LL,200)
HH =  set_to_zero(HH)
LH1 = set_to_zero(LH1)
HL1 = set_to_zero(HL1)
HH1 = set_to_zero(HH1)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic23.gif')
data.show()'''

'''LL = pruning(LL,100)
HH =  set_to_zero(HH)
LH1 = set_to_zero(LH1)
HL1 = set_to_zero(HL1)
HH1 = set_to_zero(HH1)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic24.gif')
data.show()'''


'''LL = pruning(LL,50)
HH =  set_to_zero(HH)
LH1 = set_to_zero(LH1)
HL1 = set_to_zero(HL1)
HH1 = set_to_zero(HH1)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic25.gif')
data.show()'''



'''LL = pruning(LL,25)
HH =  set_to_zero(HH)
LH1 = set_to_zero(LH1)
HL1 = set_to_zero(HL1)
HH1 = set_to_zero(HH1)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic26.gif')
data.show()'''



'''LL = pruning(LL,10)
HH =  set_to_zero(HH)
LH1 = set_to_zero(LH1)
HL1 = set_to_zero(HL1)
HH1 = set_to_zero(HH1)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy_pic27.gif')
data.show()'''


'''coeffs = pywt.wavedec2(img, 'db1',level=3)
LL,(LH,HL,HH),(LH1,HL1,HH1),(LH2,HL2,HH2)= coeffs
 
   
ELL = average_energy_subband(LL)   # comes out to be 797.89
ELH = average_energy_subband(LH)   # comes out to be 75.94
EHL = average_energy_subband(HL)   # comes out to be 98
EHH = average_energy_subband(HH)   # comes out to be 46.67
ELH1 = average_energy_subband(LH1) # comes out to be 31.4
EHL1 = average_energy_subband(HL1) # comes out to be 40.64
EHH1 = average_energy_subband(HH1) # comes out to be 18.7
ELH2 = average_energy_subband(LH2) # comes out to be 12.58
EHL2 = average_energy_subband(HL2) # comes out to be 15.89
EHH2 = average_energy_subband(HH2) # comes out to be 7.09

#Setting thresolds values
#Setting thresolds as 798,76,98,46,31,41,18,12,16,7
LL = pruning(LL,798)
LH = pruning(LH,76)
HL = pruning(HL,98)
HH = pruning(HH,46)
LH1 = pruning(LH1,31)
HL1 = pruning(HL1,41)
HH1 = pruning(HH1,18)
LH2 = pruning(HH2,12)
HL2 = pruning(HH2,16)
HH2 = pruning(HH2,7)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm1.gif')
data.show()'''

#Now halfing thresolds 
'''LL = pruning(LL,798/2)
LH = pruning(LH,76/2)
HL = pruning(HL,98/2)
HH = pruning(HH,46/2)
LH1 = pruning(LH1,31/2)
HL1 = pruning(HL1,41/2)
HH1 = pruning(HH1,18/2)
LH2 = pruning(HH2,12/2)
HL2 = pruning(HH2,16/2)
HH2 = pruning(HH2,7/2)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm2.gif')
data.show()'''

'''LL = pruning(LL,798/4)
LH = pruning(LH,76/4)
HL = pruning(HL,98/4)
HH = pruning(HH,46/4)
LH1 = pruning(LH1,31/4)
HL1 = pruning(HL1,41/4)
HH1 = pruning(HH1,18/4)
LH2 = pruning(HH2,12/4)
HL2 = pruning(HH2,16/4)
HH2 = pruning(HH2,7/4)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm3.gif')
data.show()'''

'''LL = pruning(LL,798/8)
LH = pruning(LH,76/8)
HL = pruning(HL,98/8)
HH = pruning(HH,46/8)
LH1 = pruning(LH1,31/8)
HL1 = pruning(HL1,41/8)
HH1 = pruning(HH1,18/8)
LH2 = pruning(HH2,12/8)
HL2 = pruning(HH2,16/8)
HH2 = pruning(HH2,7/8)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm4.gif')
data.show()'''

'''LL = pruning(LL,798/16)
LH = pruning(LH,76/16)
HL = pruning(HL,98/16)
HH = pruning(HH,46/16)
LH1 = pruning(LH1,31/16)
HL1 = pruning(HL1,41/16)
HH1 = pruning(HH1,18/16)
LH2 = pruning(HH2,12/16)
HL2 = pruning(HH2,16/16)
HH2 = pruning(HH2,7/16)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm5.gif')
data.show()'''

'''LL = pruning(LL,798/32)
LH = pruning(LH,76/32)
HL = pruning(HL,98/32)
HH = pruning(HH,46/32)
LH1 = pruning(LH1,31/32)
HL1 = pruning(HL1,41/32)
HH1 = pruning(HH1,18/32)
LH2 = pruning(HH2,12/32)
HL2 = pruning(HH2,16/32)
HH2 = pruning(HH2,7/32)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm6.gif')
data.show()'''

'''LL = pruning(LL,50)
#LH = pruning(LH,76)
#HL = pruning(HL,98)
#HH = pruning(HH,46)
#LH1 = pruning(LH1,31)
#HL1 = pruning(HL1,41)
HH1 = set_to_zero(HH1)
LH2 = set_to_zero(LH2)
HL2 = set_to_zero(HL2)
HH2 = set_to_zero(HH2)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm7.gif')
data.show()

LL = pruning(LL,30)
#LH = pruning(LH,76)
#HL = pruning(HL,98)
#HH = pruning(HH,46)
#LH1 = pruning(LH1,31)
#HL1 = pruning(HL1,41)
HH1 = set_to_zero(HH1)
LH2 = set_to_zero(LH2)
HL2 = set_to_zero(HL2)
HH2 = set_to_zero(HH2)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm8.gif')
data.show()'''

'''LL = pruning(LL,100)
#LH = pruning(LH,76)
#HL = pruning(HL,98)
#HH = pruning(HH,46)
#LH1 = pruning(LH1,31)
#HL1 = pruning(HL1,41)
HH1 = set_to_zero(HH1)
LH2 = set_to_zero(LH2)
HL2 = set_to_zero(HL2)
HH2 = set_to_zero(HH2)


matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dumm9.gif')
data.show()'''

'''coeffs = pywt.wavedec2(img, 'db1',level=1)
LL,(LH,HL,HH)= coeffs
 
   
ELL = average_energy_subband(LL) # comes out to be 194.95
ELH = average_energy_subband(LH) # comes out to be 12.58
EHL = average_energy_subband(HL) # comes out to be 15.89
EHH = average_energy_subband(HH) # comes out to be 7.09'''

'''HH = restore(HH,20000)



matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy1.gif')
data.show()'''


'''HH = set_to_zero(HH)
HL = restore(HL,20000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy2.gif')
data.show()'''


'''HH = set_to_zero(HH)
HL = restore(HL,10000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy3.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy4.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = restore(LH,40000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy5.gif')
data.show()'''


'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = restore(LH,20000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy6.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy7.gif')
data.show()'''


'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,40000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy8.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,50000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy9.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,60000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy10.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,62000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy11.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,63000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy12.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,64000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy13.gif')
data.show()'''

'''HH = set_to_zero(HH)
HL = set_to_zero(HL)
LH = set_to_zero(LH)
LL = restore(LL,65000)

matrix = pywt.waverec2(coeffs, 'db1')
data = im.fromarray(matrix)
data.save('dummy14.gif')
data.show()'''






      
    



