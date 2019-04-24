from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import io
import random
import math
import cv2
import numpy as np

class Simulator:
    ex = 0.0
    ey = 1.5
    ez = 0.0
    cx = 0.0
    cy = 1.5
    cz = 1.0
    obstacles = []
    simulator = None
    callback = None

    def __init__(self, func):
        Simulator.simulator = self
        Simulator.callback = func
        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
        glutInitWindowSize(176, 176)     # window size
        glutInitWindowPosition(100, 100) # window position
        glutCreateWindow(b"EV3 camera")      # show window
        glutDisplayFunc(display)         # draw callback function
        glutReshapeFunc(reshape)         # resize callback function
        glutMouseFunc(save)
        glutTimerFunc(100, timer_func, None)
        init(176, 176)
        glutMainLoop()

    def resetEnv(self):
        init(176, 176)

    def simulate(self, action=2):
        moveCamera(action)
        return isCrashed()

    def getState(self):
        return getCameraImage()

def init(width, height):
    """ initialize """
    glClearColor(0.7, 0.7, 0.7, 1.0)
    glEnable(GL_DEPTH_TEST) # enable shading
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    ## set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 50.0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    ## init camera
    Simulator.ex = 0.0
    Simulator.ey = 1.5
    Simulator.ez = 0.0
    Simulator.cx = 0.0
    Simulator.cy = 1.5
    Simulator.cz = 0.5

    ## init obstacles
    ## Random Setting
    # Simulator.obstacles = []
    # for i in range(2500):
    #     randomX = 200 - random.random()*400
    #     randomZ = 200 - random.random()*400
    #     while randomX**2 < 100 and randomZ**2 < 100:
    #         randomX = 200 - random.random()*400
    #         randomZ = 200 - random.random()*400
    #     Simulator.obstacles.append((randomX, randomZ))

    ## Like Lane
    Simulator.obstacles = []
    X = 0
    Z = 0
    bias = 0
    for i in range(201):
        if i%15 == 0:
            if i == 0:
                bias = 0
            else:
                bias = 0.3 - random.random()*0.6
        X = X + bias
        Z = i
        Simulator.obstacles.append((X - 3, Z))
        Simulator.obstacles.append((X + 3, Z))

def getCameraImage():
    glReadBuffer(GL_FRONT)
    pix_buff = glReadPixels(0, 0, 176, 176, GL_BGR, GL_FLOAT)
    pix_buff = pix_buff * 255
    jpg_buff = np.zeros(pix_buff.shape)

    for h in range(176):
        jpg_buff[h] = pix_buff[-(h+1)]

    # cv2.imwrite('opengl_image.jpg', jpg_buff)

    is_success, buffer = cv2.imencode('.jpg', jpg_buff)
    jpg_bin = io.BytesIO(buffer)
    return jpg_bin

def moveCamera(action):
    angle = 0
    if action == 0: # LEFT
        angle = -2
    elif action == 1: # left
        angle = -1
    elif action == 2: # center
        angle = 0
    elif action == 3: # right
        angle = 1
    elif action == 4: # RIGHT
        angle = 2

    rotateCamera(angle)
    moveForward()
    glutPostRedisplay()

def rotateCamera(angle):
    # cos -sin
    # sin  cos
    currentCameraAngleX = Simulator.cx - Simulator.ex
    currentCameraAngleZ = Simulator.cz - Simulator.ez

    radian = math.radians(angle)
    newCameraAngleX = math.cos(radian)*currentCameraAngleX - math.sin(radian)*currentCameraAngleZ
    newCameraAngleZ = math.sin(radian)*currentCameraAngleX + math.cos(radian)*currentCameraAngleZ

    Simulator.cx = Simulator.ex + newCameraAngleX
    Simulator.cz = Simulator.ez + newCameraAngleZ

def moveForward():
    forwardVectorX = Simulator.cx - Simulator.ex
    forwardVectorZ = Simulator.cz - Simulator.ez

    Simulator.ex = Simulator.ex + forwardVectorX
    Simulator.ez = Simulator.ez + forwardVectorZ
    Simulator.cx = Simulator.cx + forwardVectorX
    Simulator.cz = Simulator.cz + forwardVectorZ

def isCrashed():
    for (x, z) in Simulator.obstacles:
        distance = (Simulator.ex-x)**2 + (Simulator.ez-z)**2
        if distance < 1:
            return True

    if Simulator.ex**2 > 40000 or Simulator.ez**2 > 40000:
        return True

    return False

def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    ##set camera
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 1.0])

    gluLookAt(Simulator.ex, Simulator.ey, Simulator.ez, Simulator.cx, Simulator.cy, Simulator.cz, 0.0, 1.0, 0.0)

    draw_ground()
    draw_obstacles()

    glFlush()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 50.0)

def save(button, state, x, y):
    if state == GLUT_DOWN:
        glReadBuffer(GL_FRONT)
        pix_buff = glReadPixels(0, 0, 176, 176, GL_BGR, GL_FLOAT)
        pix_buff = pix_buff * 255
        jpg_buff = np.zeros(pix_buff.shape)

        for h in range(176):
            jpg_buff[h] = pix_buff[-(h+1)]

        cv2.imwrite('opengl_image.jpg', jpg_buff)

def timer_func(value):
    Simulator.callback()
    glutTimerFunc(50, timer_func, None)

def draw_ground():
    """ draw ground on a x-z plane for (-100, 100) """
    scope = 200

    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.3, 0.3, 0.3, 1.0))

    glBegin(GL_QUADS)

    for i in range(0, scope*2, 5):
        for j in range(0, scope*2, 5):
            x = scope - i
            z = scope - j
            glNormal3f(0.0, 1.0, 0.0)
            glVertex3f(x, 0.0, z)
            glVertex3f(x, 0.0, z+5.0)
            glVertex3f(x+5.0, 0.0, z+5.0)
            glVertex3f(x+5.0, 0.0, z)
    glEnd()

    glPopMatrix()

def draw_obstacles():
    for (x, z) in Simulator.obstacles:
        draw_obstacle(x, z)

def draw_obstacle(x=0.0, z=0.0):
    """ draw obstacle on (x, y=0, z) """
    vertex = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0],
        [0.0, 3.0, 0.0],
        [1.0, 3.0, 0.0],
        [1.0, 3.0, 1.0],
        [0.0, 3.0, 1.0]
    ]

    surface = [
        [0, 1, 2, 3],
        [4, 7, 6, 5],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [0, 3, 7, 4]
    ]

    normal = [
        [0.0, -1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0]
    ]

    glPushMatrix()
    glTranslatef(x-0.5, 0.01, z-0.5)

    glBegin(GL_QUADS)
    for i in range(6):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0))

        glNormal3f(normal[i][0], normal[i][1], normal[i][2])
        glVertex3f(vertex[surface[i][0]][0], vertex[surface[i][0]][1], vertex[surface[i][0]][2])
        glVertex3f(vertex[surface[i][1]][0], vertex[surface[i][1]][1], vertex[surface[i][1]][2])
        glVertex3f(vertex[surface[i][2]][0], vertex[surface[i][2]][1], vertex[surface[i][2]][2])
        glVertex3f(vertex[surface[i][3]][0], vertex[surface[i][3]][1], vertex[surface[i][3]][2])
    glEnd()
    glPopMatrix()

def tmp_func():
    is_crashed = Simulator.simulator.simulate(2)
    if is_crashed:
        Simulator.simulator.resetEnv()

if __name__ == '__main__':
    Simulator(tmp_func)
