from drawable_shapes import *
import constants as const
from basic_shapes import createCube
import numpy as np

#Cube edges corresponde a la clase creadora de todos los lados de un cubo.
#Usada como base para las pelotas que rebotan.
class cubeEdges:
    #Crea un cubeEdges con un pipeline, el grosor y sus gpuEdges.
    def __init__(self, pipeline, thickness):
        self.pipeline = pipeline
        self.thickness = thickness
        self.gpuEdges = [] #gpuShapes-transformations.
        self.setEdges()

    #Coloca un gpuEdge dados los ejes normalizados (+-1) y un escalamiento.
    def setEdge(self, axis, scale):
        gpuShape = createGPUShape(self.pipeline, createCube(self.thickness))
        #constante de translación
        tc = const.CUBE_SIZE + self.thickness
        axis = np.array(axis)
        translation = axis*tc
        transformations = [tr.translate(translation[0], translation[1], translation[2]), tr.scale(scale[0], scale[1], scale[2])]
        self.gpuEdges.append([gpuShape, transformations])
    
    #Setea los 8 lados del cubo en sus posiciones respectivas.
    def setEdges(self):
        edgeLen = const.CUBE_SIZE/self.thickness
        #lados de x en el plano xy.
        for i in [-1,1]:
            for j in [-1,1]:
                self.setEdge([i,0,j], [1,edgeLen,1])
        #lados de y en el plano xy.
        for i in [-1,1]:
            for j in [-1,1]:
                self.setEdge([0,i,j], [edgeLen,1,1])
        #lados de z en el plano zy.
        for i in [-1,1]:
            for j in [-1,1]:
                self.setEdge([i,j,0], [1,1,edgeLen])

    #Dibuja el cubo.
    def draw(self):
        for gpuEdge in self.gpuEdges:
            draw(self.pipeline, gpuEdge[0], gpuEdge[1])
        
    #Limpia las gpuShapes del cubo.
    def clear(self):
        for gpuEdge in self.gpuEdges:
            gpuEdge[0].clear()