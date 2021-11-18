
"""
Adapted from Chapter 13 of AM.  In the code, use of "##" for comments
indicates a section heading from the chapter followed by the code
presented in that section.

https://github.com/makehumancommunity/gl-test-cases.git
https://realtech-vr.com/home/glview
"""

import sys

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QWidget, QMainWindow, QVBoxLayout, 
                             QOpenGLWidget)
from PyQt5.QtGui import (QOpenGLVersionProfile, QOpenGLShaderProgram, QOpenGLShader,
                         QMatrix4x4, QVector3D, QColor)
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        widget = QWidget()
        layout = QVBoxLayout()
        oglw = GlWidget()
        layout.addWidget(oglw)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        ## Animating and controlling OpenGL drawings
        btn_layout = QHBoxLayout()
        widget.layout().addLayout(btn_layout)
        for direction in ('none', 'left', 'right', 'up', 'down'):
            button = QPushButton(direction, autoExclusive=True, checkable=True, 
                                 clicked=getattr(oglw, f'spin_{direction}'))
            btn_layout.addWidget(button)
        zoom_layout = QHBoxLayout()
        widget.layout().addLayout(zoom_layout)
        zoom_in = QPushButton('zoom in', clicked=oglw.zoom_in)
        zoom_layout.addWidget(zoom_in)
        zoom_out = QPushButton('zoom out', clicked=oglw.zoom_out)
        zoom_layout.addWidget(zoom_out)
      

class GlWidget(QOpenGLWidget):
    """ A widget to display our OpenGL drawing.
    """
    
    def initializeGL(self):

        ## First steps with OpenGLWidget
        super().initializeGL()
        gl_context = self.context()
        version = QOpenGLVersionProfile()
        version.setVersion(2, 1)
        self.gl = gl_context.versionFunctions(version)

        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glDepthFunc(self.gl.GL_LESS)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

        ## Creating a program
        self.program = QOpenGLShaderProgram()
        flag = self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'vertex_shader.glsl')
        if not flag:
            print("vertex shader did not load!")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'fragment_shader.glsl')
        if not flag:
            print("fragment shader did not load!")
        self.program.link()

        ## Accessing our variables
        self.vertex_location = self.program.attributeLocation('vertex')
        self.matrix_location = self.program.uniformLocation('matrix')
        self.color_location = self.program.attributeLocation('color_attr')

        ## Configuring a projection matrix
        self.view_matrix = QMatrix4x4()
        self.view_matrix.perspective(
            45, # angle
            self.width()/self.height(), # aspect ratio
            0.1,  # near clipping plane
            100.0 # far clipping plane            
        )
 
        self.view_matrix.translate(0, 0, -5) # back up as the viewer (z axis is into the screen)

        ## Animating in OpenGL
        self.rotation = [0, 0, 0, 0]

    def qcolor_to_glvec(self, qcolor):
        return QVector3D(qcolor.red()/255, qcolor.green()/255, qcolor.blue()/255)

    def paintGL(self):
        
        ## Drawing our first shape
        self.gl.glClearColor(0.0, 0, 0.0, 1) # solid bg color (0,0,0)=black with 100% fill (no transparency)
        self.gl.glClear(
            self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT
        )
        self.program.bind()

        front_vertices = [ 
            QVector3D(0.0, 1.0, 0.0),  # peak
            QVector3D(-1.0, 0.0, 0.0), # bottom left
            QVector3D(1.0, 0.0, 0.0)   # bottom right
        ]

        # Define some colors
        purple_k = QVector3D(81/255,  40/255, 136/255)
        lgray_k = QVector3D(226/255,  227/255, 228/255)
        dgray_k = QVector3D(167/255,  169/255, 172/255)

        red =  self.qcolor_to_glvec(QColor('red'))
        orange = self.qcolor_to_glvec(QColor('orange'))
        yellow = self.qcolor_to_glvec(QColor('yellow'))
        purple = self.qcolor_to_glvec(QColor('purple'))
        blue = self.qcolor_to_glvec(QColor('blue'))
        cyan = self.qcolor_to_glvec(QColor('cyan'))
        magenta = self.qcolor_to_glvec(QColor('magenta'))

        # Qt uses 0-255 for RGB, but OpenGL scales that to 0-1 for each channel.
        front_colors = (purple_k, lgray_k, dgray_k)

        self.program.setUniformValue(self.matrix_location, self.view_matrix)

        #self.program.setAttributeValue(self.color_location, gl_colors[0])

        self.program.enableAttributeArray(self.vertex_location)
        self.program.setAttributeArray(self.vertex_location, front_vertices)
        self.program.enableAttributeArray(self.color_location)
        self.program.setAttributeArray(self.color_location, front_colors)

        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

        # Creating a 3D object
        back_vertices = [ 
            QVector3D(x.toVector2D(), -0.5)
            for x in front_vertices
        ]
        self.program.setAttributeArray(
            self.vertex_location, reversed(back_vertices)
        )
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)
        sides = [(0, 1), (1, 2), (2, 0)]
        side_vertices = list()
        for index1, index2 in sides:
            side_vertices += [
                front_vertices[index1],
                back_vertices[index1],
                back_vertices[index2],
                front_vertices[index2]
            ]

        side_colors = [blue, purple, cyan, magenta] * 3
        self.program.setAttributeArray(self.color_location, side_colors)
        self.program.setAttributeArray(self.vertex_location, side_vertices)
        self.gl.glDrawArrays(self.gl.GL_QUADS, 0, len(side_vertices))
        self.program.disableAttributeArray(self.vertex_location)
        self.program.disableAttributeArray(self.color_location)
        self.program.release()

        self.view_matrix.rotate(*self.rotation)

        self.update()
    
    def spin_none(self):
        self.rotation = [0, 0, 0, 0]

    def spin_left(self):
        self.rotation = [-1, 0, 1, 0]

    def spin_right(self):
        self.rotation = [1, 0, 1, 0]

    def spin_up(self):
        self.rotation = [1, 1, 0, 0]

    def spin_down(self):
        self.rotation = [-1, -1, 0, 0]

    def zoom_in(self):
        self.view_matrix.scale(1.1, 1.1, 1.1)

    def zoom_out(self):
        self.view_matrix.scale(1/1.1, 1/1.1, 1/1.1)
       
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
 


    
