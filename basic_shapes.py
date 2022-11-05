import numpy as np
from OpenGL.GL import *

#Clase encargada de almacenar la posicion de los vertices en xyz,
#sus respectivos colores y las aristas de los triangulos que se forman.
class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData

    def verticalRotate(self, angle):
        for i in range(0, len(self.vertexData), 6):
            rad = abs(self.vertexData[i+1])
            sign = self.vertexData[i+1]/rad
            self.vertexData[i+1] = round(sign*rad*np.cos(angle), 1)
            self.vertexData[i+2] = round(sign*rad*np.sin(angle), 1)


a = [-0.5, 0.4, -0.4,   1.0, 0.0, 0.0,
      0.5, 0.4, -0.4,   0.0, 1.0, 0.0,
      0.5, 0.4, 0.4,    0.0, 0.0, 1.0, 
     -0.5, 0.4, 0.4,    1.0, 1.0, 1.0]

def createRainbowQuad():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 2,  1.0, 0.0, 0.0,
         0.5, -0.5, -2,  0.0, 1.0, 0.0,
         0.5,  0.5, -2,  0.0, 0.0, 1.0,
        -0.5,  0.5, 2,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)



#Crea un cubo con un lado entre 0 y 1
def createCube(lado): 
    vertexData = np.array([
        # positions        # colors
        -lado, -lado,  lado,  1.0, 0.0, 0.0,
         lado, -lado,  lado,  0.0, 1.0, 0.0,
         lado,  lado,  lado,  0.0, 0.0, 1.0,
        -lado,  lado,  lado,  1.0, 1.0, 1.0,
        -lado, -lado, -lado,  1.0, 0.0, 0.0,
         lado, -lado, -lado,  0.0, 1.0, 0.0,
         lado,  lado, -lado,  1.0, 0.0, 1.0,
        -lado,  lado, -lado,  1.0, 1.0, 1.0
    ], dtype=np.float32)
    indexData = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ])
    return Shape(vertexData, indexData)

#Crea una esfera con radio entre 0 y 1, y un número de puntos de circunferencia N.
def createSphere(radio, N):
    #Colores de la pelota de playa.
    colors = [[1,1,1], [0,0,1], [1,1,1], [1,0,0], [1,1,1], [1,1,0]]
    dAngulo = 2*np.pi/N
    vertexData = []
    indexData = []
    colorIndex = 0
    #Se va posicionando en el eje z.
    for i in range(0, N//2+1):
        #Va haciendo circunferencias con N puntos en el plano XY, variando su radio según z.
        for j in range(0, N):
            indice = (i*N)+j
            r, g, b = colors[colorIndex]
            vertexData += [radio*np.sin(i*dAngulo)*np.cos(j*dAngulo), radio*np.sin(i*dAngulo)*np.sin(j*dAngulo), radio*np.cos(i*dAngulo), r, g, b]
            colorIndex = int((j/N)*6) #Permite determinar el color de la pelota segun el angulo.
            if (i<N//2):
                indexData += [N*i+indice%N, N*i+(indice+1)%N, N*(i+1)+indice%N]
                indexData += [N*(i+1)+indice%N, N*(i+1)+(indice+1)%N, N*i+(indice+1)%N]
    return Shape(vertexData, indexData)