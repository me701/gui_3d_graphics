
"""
Adapted from Chapter 13 of AM
https://github.com/makehumancommunity/gl-test-cases.git
https://realtech-vr.com/home/glview
"""

import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, 
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

    def paintGL(self):
        
        ## Drawing our first shape
        self.gl.glClearColor(0.1, 0, 0.2, 1) # solid bg color (.1,0,.2) with 100% fill (no transparency)
        self.gl.glClear(
            self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT
        )
        self.program.bind()

        front_vertices = [ 
            QVector3D(0.0, 1.0, 0.0),  # peak
            QVector3D(-1.0, 0.0, 0.0), # bottom left
            QVector3D(1.0, 0.0, 0.0)   # bottom right
        ]

        # Qt uses 0-255 for RGB, but OpenGL scales that to 0-1 for each channel.
        gl_colors = (
            QVector3D(81/255, 40/255, 136/255), # color 1
            QVector3D(209/255, 209/255, 209/255), # color2
            QVector3D(167/255, 167/255, 167/255), # color 3
        )

        self.program.setUniformValue(self.matrix_location, self.view_matrix)

        #self.program.setAttributeValue(self.color_location, gl_colors[0])

        self.program.enableAttributeArray(self.vertex_location)
        self.program.setAttributeArray(self.vertex_location, front_vertices)
        self.program.enableAttributeArray(self.color_location)
        self.program.setAttributeArray(self.color_location, gl_colors)

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
                front_vertices[index1]
            ]
        side_colors = [
            QVector3D(255/255, 255/255, 255/255), 
            QVector3D(0/255, 0/255, 0/255),
            QVector3D(167/255, 167/255, 167/255),
            QVector3D(0, 0, 0)
        ] * 3
        self.program.setAttributeArray(self.color_location, gl_colors)
        self.program.setAttributeArray(self.vertex_location, side_vertices)
        self.gl.glDrawArrays(self.gl.GL_QUADS, 0, len(side_vertices))
        self.program.disableAttributeArray(self.vertex_location)
        self.program.disableAttributeArray(self.color_location)
        self.program.release()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GlWidget()
    print('lala')
    window.show()
    app.exec_()
 


    
