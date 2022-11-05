import numpy as np
import transformations as tr
import glfw
from OpenGL.GL import *
import constants as const

#Dado un vector, retorna su transpuesto.
def transpose(vector):
    #Si es horizontal, retorna uno vertical con un 1 al final para 
    #que sea compatible con las transformaciones tr.
    if (len(vector) == 1): 
        newVector = [[], [], [], [1]]
        for i in range(3):
            newVector[i].append(vector[0][i])
    else:
        newVector = [[]]
        for i in range(3):
            newVector[0].append(vector[i][0])
    return newVector

#Crea un controlador para la cámara con una posición viewPos y up cam.
class Controller:
    def __init__(self):
        self.viewPos = np.array([[4, 0, 0.5]])
        self.cam = np.array([0, 0, 1])
        self.zoom = 60
    
    #Rota la posición de la cámara con respecto al origen.
    def rotate(self, angle):
        self.viewPos = transpose(tr.matmul([tr.rotationZ(angle), transpose(self.viewPos)]))

    #Acerca o aleja la posición de la cámara una cierta cantidad.
    def doZoom(self, quantity):
        self.zoom += quantity

controller = Controller()

#Setea la posición de la cámara a partir de lo almacenado en el controlador.
def setView(pipeline):
    view = tr.lookAt(
            controller.viewPos[0],
            np.array([0,0,0]),
            controller.cam
        )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    projection = tr.perspective(controller.zoom, float(const.WIDTH)/float(const.HEIGHT), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
#Función para recibir el input del teclado y realizar determinadas acciones.
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    #Rotación en 2pi/15 si se presiona la flecha izquierda.
    if key == glfw.KEY_LEFT:
        controller.rotate(2*np.pi/15)

    #Rotación en -2pi/15 si se presiona la flecha izquierda.
    elif key == glfw.KEY_RIGHT:
        controller.rotate(-2*np.pi/15)

    #Cambia el zoom en -10 si se presiona la flecha de arriba.
    elif key == glfw.KEY_UP:
        if controller.zoom == 10:
            print("Maximum zoom!")
        else:
            controller.doZoom(-10)

    #Cambia el zoom en 10 si se presiona la flecha de abajo.
    elif key == glfw.KEY_DOWN:
        if controller.zoom == 170:
            print("Minimum zoom!")
        else:
            controller.doZoom(10)

    else:
        print('Unknown key')