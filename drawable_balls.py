from OpenGL.GL import *
import transformations as tr
from basic_shapes import *
import constants as const
import math
from drawable_shapes import *

#Función encargada de aumentar o disminuir la velocidad de rotación de forma lineal dependiendo del
#punto x.
def linearRotateFunction(x):
    return 1 + const.M + 2*const.M*(x - const.ROTIT)/(const.ROTIT-1)

#Ball es la clase cuyo proposito consiste en servir como punto de referencia a la hora de mover la bola y aplicar
#diversos métodos para simular las interacciones de la bola con el entorno de manera medianamente realista.
class Ball:
    def __init__(self, pipeline, startPosition, velocity, radio):
        self.pipeline = pipeline #Pipeline usado por la bola.
        self.gpuShape = createGPUShape(pipeline, createSphere(radio, 100)) 
        self.position = np.array(startPosition, dtype=np.float64) #Posición en x,y,z de la bola. 
        self.velocity = np.array(velocity, dtype=np.float64) #Velocidad en x,y,z de la bola.
        self.radio = radio #Radio de la bola.
        self.angles = np.array([0,0,0], dtype=np.float64) #Ángulos inciales de la bola.
        #Lista de instrucciones de rotación que se va llenando luego de efectuar un choque.
        self.angleList = [] #de la forma [Angulos, iteraciones restantes]

    #Suma todos las instrucciones de ángulos con iteraciones restantes no nulas.
    def sumAngles(self):
        for angles in self.angleList:
            if (angles[1] > 0):
                self.angles+=angles[0]*linearRotateFunction(angles[1])
                angles[1] -= 1

    #Dibuja el gpuShape de la bola con su posicion relativa al centro de la misma
    #y la rotación que debe tener.
    def draw(self):
        self.sumAngles()
        draw(self.pipeline, self.gpuShape,
         [tr.translate(self.position[0], self.position[1], self.position[2]), 
         tr.rotationX(self.angles[0]), tr.rotationY(self.angles[1]), tr.rotationZ(self.angles[2])]) #.transformation)
      
    #Permite que la bola se mueva una posición usando su velocidad, una aceleración en z y delta de tiempo t.
    def move(self, t):
        self.velocity += np.array([0,0,-5*9.8/const.HEIGHT])*t
        self.position += self.velocity*t

    #Añade una nueva instrucción de ángulos para rotar a angleList.
    #Los ángulos de rotación se obtienen a partir de la normal de la superficie con la que están rotando
    #y la velocidad de la bola.
    def rotate(self, vNormal):
        angles = self.velocity - vNormal
        angles /= const.ROCE
        angleInstruction = [angles/const.ROTIT, const.ROTIT]
        append = True
        #pequeña optimización: revisa angleList por si hay alguna con 0 iteraciones restantes
        #y sobreescribe la nueva instrucción ahí.
        for i in range(len(self.angleList)):
            if self.angleList[i][1] == 0:
                self.angleList[i] = angleInstruction
                append = False
                break
        #si no hay ninguno que cumpla, se añade la instrucción al final de angleList.
        if append:
            self.angleList.append(angleInstruction)
        
    #Da el efecto de rebote, cambiando su rotación cada vez que la pelota toca el borde
    #de la ventana. Se ignora la instrucción de hacer 0 el rebote con el borde superior ya
    #que se ve menos realista 
    def rebote(self, axis, sign):
        self.velocity[axis] = sign*abs(self.velocity[axis])
        self.rotate(self.velocity[axis])
        
    #Aplica la operación de rebote sobre la bola cada vez que colisiona con uno de bordes.
    def collideWithBorders(self):
        for i in range(3):
            #choca con el borde positivo del eje i
            if self.position[i]+self.radio > const.CUBE_SIZE: 
                self.rebote(i, -1)
            #choca con el borde negativo del eje i
            if self.position[i]-self.radio < -const.CUBE_SIZE: 
                self.rebote(i, 1)
                                      
    #Limpia la gpuShape.
    def clear(self):
        self.gpuShape.clear()

#Obtiene una de las componentes de velocidad en xy a partir de la otra
#tal que el módulo sea V.
def getV(x):
    return math.sqrt(pow(const.V,2)-pow(x,2))

#BallSet es la clase contenedora de instancias de la clase Ball, dicha clase posee
#métodos para realizar acciones sobre y entre las bolas contenidas en el set.
class BallSet:
    def __init__(self, pipeline):
        self.balls = []
        self.pipeline = pipeline

    #Añade una bola de radio 0.3s con una posición y velocidad vx y vz específicas.
    def add(self, posición, vxz):
        self.balls.append(Ball(self.pipeline, posición, [vxz[0], getV(vxz[0]), vxz[1]], 0.3))
    
    #Dibuja las bolas.
    def draw(self):
        for ball in self.balls:
            ball.draw()

    #Mueve las bolas.
    def move(self, delta):
        for ball in self.balls:
            ball.move(delta)

    #Limpia las gpuShapes de las bolas.
    def clear(self):
        for ball in self.balls:
            ball.clear()

    #Retorna true si están colisionando, false si no.
    def areColliding(self, ball1, ball2):
        return ball1.radio + ball2.radio > np.linalg.norm(ball1.position-ball2.position)

    #Trata de mitigar el error en la variación de velocidades producto de los choques entre bolas.
    def fixCollide(self, ball1, ball2):
        dx, dy, dz = ball1.position - ball2.position
        dvx, dvy, dvz = ball1.velocity - ball2.velocity 
        A = pow(dvx,2) + pow(dvy,2) + pow(dvz,2)
        B = -2*(dx*dvx + dy*dvy + dz*dvz)
        C = pow(dx,2) + pow(dy,2) + pow(dz, 2) - 4*pow(ball1.radio, 2)
        epsilon = (-B + math.sqrt(pow(B,2) - 4*A*C))/(2*A)
        ball1.position -= ball1.velocity*epsilon
        ball2.position -= ball2.velocity*epsilon
          
    #Modifica las velocidades de dos bolas luego de colisionar entre sí.
    #https://exploratoria.github.io/exhibits/mechanics/elastic-collisions-in-3d/
    def rebote(self, ball1, ball2):
        deltaPos = ball1.position - ball2.position
        n = deltaPos/np.linalg.norm(deltaPos)
        vRelative = ball1.velocity - ball2.velocity
        vNormal = np.dot(vRelative, n) * n 
        ball1.velocity -= vNormal
        ball1.rotate(vNormal)
        ball2.velocity += vNormal
        ball2.rotate(-vNormal)

    #Revisa si alguna de las bolas colisiona con los bordes del cubo o con otra bola.
    def collide(self):
        for i in range(len(self.balls)):
            for j in range(i+1, len(self.balls)):
                if self.areColliding(self.balls[i], self.balls[j]):
                    self.fixCollide(self.balls[i], self.balls[j])
                    self.rebote(self.balls[i], self.balls[j])
            self.balls[i].collideWithBorders()    