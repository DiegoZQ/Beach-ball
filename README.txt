La presente carpeta corresponde a la tarea 1 parte 2 del curso CC3501: "Modelación y Computación 
Gráfica para Ingenieros", dentro de la cual se encuentran todos los archivos necesarios para
correr lo pedido en el pdf de la tarea.

En el archivo basic_shapes se encuentran las 2 figuras utilizadas para la realización de esta tarea,
createCube que crea un cubo de colores rgb y createSphere que crea una esfera con colores de pelota de playa.
En drawable_shapes se encuentran 2 funciones que resumen varias intrucciones requeridas en drawable_cubes y 
drawable_balls. En drawable_cubes se encuentra la clase creadora del cubo con caras vacías necesario para contener
a las pelotas de playa; En drawable_balls se encuentra la clase Ball encargada de crear pelotas de playa, dibujarlas,
moverlas, rotarlas y hacer que interactúen con los bordes del cubo, también se encuenta la clase contenedora de Bolas
llamada BallSet encargada de controlar un conjunto de bolas de la clase Ball, además de sus interacciones entre bolas 
del mismo conjunto. En gpu_shape estan resumidas todas las funciones necesarias para crear gpuShapes y manipularlos
en 3 simples metodos, en easy_shaders estan los shaders necesarios para el dibujo en patalla de los gpuShapes, sus
respectivas transformaciones, además de permitir la vista de la cámara y las proyecciones. En controller está el 
controlador de la cámara, el cual está encargado de mover la cámara alrededor del cubo a partir del input del usuario.
En transformations están todas las matrices y operaciones de matrices requeridas para las transformaciones y las 
proyecciones. En constants están las constantes para la ventana, el roce, la fluides de las rotaciones, etc.
Y finalmente en main se encuentra la función encargada de utilizar todos los archivos .py mencionados anteriormente
para visualizar el resultado final de la tarea.

Punto creativo: El principal enfoque durante el desarrollo de esta tarea, fue el de simular los rebotes con rotaciones
bastante realistas sobre las pelotas de playa, dicho efecto de rotación luego de cada rebote con los bordes del cubo u 
otra pelota se logró mediante una lista de instrucciones llamada angleList definida en la clase Ball. Dicha lista determina 
la rotación que debe realizarse en cada iteración del while dentro del main durante una cierta cantidad de iteraciones definidas
como ROTIT en constants. Dicha rotación incialmente era constante para cada iteración de la rotación, pero luego se definió una 
función capaz de variar de manera lineal la rotación, haciendo que incialmente rote más y vaya disminuyendo gradualmente hasta ser nula, 
dando así el efecto de que se detiene debido al roce con aire. Además de esto, se incluyo la posibilidad de hacer zoom al cubo
con las flechas de arriba y abajo, y se decidió permitir choques perfectamente inelásticos con la cara superior del cubo en conjunto con
una aceleración de gravedad arbitraria, todo esto con el fin de tener mejores resultados a mi criterio. 

Autor: Diego Zúñiga.