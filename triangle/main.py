
"""
Adapted from Chapter 13 of AM
https://github.com/makehumancommunity/gl-test-cases.git
https://realtech-vr.com/home/glview
"""

import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, 
                             QOpenGLWidget)
from PyQt5.QtGui import (QOpenGLVersionProfile, QOpenGLShaderProgram, QOpenGLShader)
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
        super().initializeGL()
        gl_context = self.context()
        version = QOpenGLVersionProfile()
        version.setVersion(2, 1)
        self.gl = gl_context.versionFunctions(version)
        print(self.gl)
        return 
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glDepthFunc(self.gl.GL_LESS)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

        self.program = QOpenGLShaderProgram()
        flag = self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'vertex_shader.glsl')
        if not flag:
            print("vertex shader did not load!")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'fragment_shader.glsl')
        if not flag:
            print("fragment shader did not load!")
        self.program.link()

    def paintGL(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec_()
 


    
