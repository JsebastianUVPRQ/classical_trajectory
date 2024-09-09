# Formalmente, una convolución se define como una integral 
# de la forma: 
# integral de -infinito a infinito de f(t)*g(t- \tau) d(\tau\)
# En latex:  \left ( f * g \right )_{(t)} \overset{\underset{\mathrm{def}}{}}{\approx} \int_{-\infty }^{\infty} f(\tau) g(t - \tau) dr 

'''
pseudocodigo:
for each image row in input image:
    for each pixel in image row:
        set accumulator to zero
        for each kernel row in kernel:
            for each element in kernel row:
                if element position  corresponding to pixel position then
                    multiply element value  corresponding to pixel value
                    add result to accumulator
                endif
                    
        set output image pixel to accumulator
''' 
        
# Ahora traduzcamos este pseudocodigo a python

import numpy as np
import cv2

def convolucion(img, kernel):
    alto = img.shape[0]
    ancho = img.shape[1]
    
    altoKernel = kernel.shape[0]
    anchoKernel = kernel.shape[1]

    # bucles
    for x in range(ancho):
        for y in range(alto):
            suma = 0
            for i in range(altoKernel):
                for j in range(anchoKernel):
                    if y + i - 1 >= 0 and x + j - 1 >= 0:
                        try:
                            suma += img[y + i - 1, x + j - 1] * kernel[i, j]
                        except:
                            pass
            img[y, x] = suma
    return img

# creemos una imagen de pixeles random para ejemplificar
imagen_ejemplo = np.random.randint(0, 255, (5, 5))
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
imagen_procesada = convolucion(imagen_ejemplo, kernel)
print(imagen_procesada)

# imagen = cv2.imread('images/imagen.jpg', 0)
