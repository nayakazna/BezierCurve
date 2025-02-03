import numpy as np
import glfw
import OpenGL.GL as gl
from OpenGL.GLU import gluPerspective, gluLookAt

class Camera:
    def __init__(self, position=None, target=None, up=None, fov=60.0, aspect_ratio=1.0, near=0.1, far=100.0):
        """
        @brief Constructor for the Camera class.

        @param position The position of the camera in 3D space.
        @param target The point the camera is looking at.
        @param up The up vector of the camera.
        @param fov Field of view angle in degrees.
        @param aspect_ratio Aspect ratio of the viewport (width / height).
        @param near Distance to the near clipping plane.
        @param far Distance to the far clipping plane.
        """
        self.position = np.array(position if position is not None else [0.0, 0.0, -5.0], dtype=np.float32)
        self.target = np.array(target if target is not None else [0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array(up if up is not None else [0.0, 1.0, 0.0], dtype=np.float32)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        self.sensitivity = 0.1

    ##### Methods #####
    def set_perspective_projection(self) -> None:
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(self.fov, self.aspect_ratio, self.near, self.far)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def set_camera_view(self) -> None:
        gl.glLoadIdentity()
        gluLookAt(*self.position, *self.target, *self.up)
    
    def update(self, window, speed=0.1) -> None:
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.move_forward(speed)
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.move_backward(speed)
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.move_left(speed)
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.move_right(speed)
        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            self.move_up(speed)
        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
            self.move_down(speed)
    
    def move_forward(self, speed=0.1) -> None:
        direction = (self.target - self.position)
        direction /= np.linalg.norm(direction)
        self.position += speed * direction
        self.target += speed * direction
    
    def move_backward(self, speed=0.1) -> None:
        direction = (self.target - self.position)
        direction /= np.linalg.norm(direction)
        self.position -= speed * direction
        self.target -= speed * direction
    
    def move_left(self, speed=0.1) -> None:
        direction = np.cross(self.up, self.target - self.position) # up x forward = left (aturan tangan kanan)
        direction /= np.linalg.norm(direction)
        self.position += speed * direction
        self.target += speed * direction
    
    def move_right(self, speed=0.1) -> None:
        direction = np.cross(self.target - self.position, self.up) # forward x up = right (aturan tangan kanan)
        direction /= np.linalg.norm(direction)
        self.position += speed * direction
        self.target += speed * direction
    
    def move_up(self, speed=0.1) -> None:
        self.position += self.up * speed
        self.target += self.up * speed
    
    def move_down(self, speed=0.1) -> None:
        self.position -= self.up * speed
        self.target -= self.up  * speed



