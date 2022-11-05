from gpu_shape import GPUShape
from OpenGL.GL import *
import transformations as tr

#Crea un gpuShape a partir de un pipeline y un shape.
def createGPUShape(pipeline, shape):
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertexData, shape.indexData)
    return gpuShape

#Dibuja un gpuShape usando transformaciones y un pipeline.
def draw(pipeline, gpuShape, transformations):
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,
        tr.matmul(transformations)
    )
    pipeline.drawCall(gpuShape)