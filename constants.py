SIZE_IN_BYTES = 4
#Dimensiones de la ventana.
k = 80
WIDTH = 16*k
HEIGHT = 9*k
#Dimensiones del cubo.
CUBE_SIZE = 0.8
#Constante de velocidad en el plano xy.
V = 0.4*CUBE_SIZE
#Constante de roce para obtener la rotación total que será particionada en la lista de la clase Ball.
ROCE = 1 #No usar con 0.
#Iteraciones de inicio a fin para cada rotación.
ROTIT = 1000 #Otorga fluidez y realismo. (para pantalla de 60 hz, aumentar en caso de tener más)
#Variable de inclinacion para la velocidad de la rotación.
M = 0.9 #Entre 0 y 1. Con 0 es velocidad constante.