import glfw
from OpenGL.GL import *
from easy_shaders import SimpleModelViewProjectionShaderProgram
from basic_shapes import *
import constants as const
from drawable_balls import *
from controller import *
from drawable_cubes import cubeEdges

def main():
 
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    window = glfw.create_window(const.WIDTH, const.HEIGHT, "Tarea 1 parte 2", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    #Keyboard events
    glfw.set_key_callback(window, on_key) 
    #Pipeline
    pipeline = SimpleModelViewProjectionShaderProgram()
    glUseProgram(pipeline.shaderProgram)
 
    #Figuras 3D
    #cubo = createGPUShape(pipeline, createCube(const.CUBE_SIZE))
    cubo = cubeEdges(pipeline, 0.01)
    #cubo.setEdges()
    bolas = BallSet(pipeline)
    bolas.add([0,0,0.3*const.CUBE_SIZE], [0.3, 0.0])
    bolas.add([0.2,0.2,0.2], [0.1, 0.4])

    #quad1 = createRainbowQuad()
    #quad1.verticalRotate(np.pi/4)
    #print(quad1.indexData)
    #print(quad1.vertexData)
    #quad = createGPUShape(pipeline, quad1)
    
    #Color del fondo
    glClearColor(229/255, 228/255, 226/255, 1.0)
    glEnable(GL_DEPTH_TEST)

    i = 0
    a = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        setView(pipeline)    
        cubo.draw()
        #Permite calcular la diferencia positiva delta entre 2 cuadros.
        if (i%2==0): #si i es par.
            b = glfw.get_time()
            delta = b-a
        else: #si i es impar.
            a = glfw.get_time()
            delta = a-b
        #draw(pipeline, quad, [tr.scale(1,1,1)])
        bolas.draw() #dibuja el logo.
        bolas.collide() #revisa si hay colisiones y actúa en caso de que las haya.
        bolas.move(delta) #mueve el logo.
        glfw.swap_buffers(window)
        i+=1

    cubo.clear()
    bolas.clear()
    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()