import OpenGL.GL as gl
from OpenGL.GLU import gluPerspective

def set_perspective_projection(fov: float, aspect_ratio: float, near: float, far: float) -> None:
    """
    @brief Set the perspective projection matrix.

    @param fov Field of view angle in degrees.
    @param aspect_ratio Aspect ratio of the viewport (width / height).
    @param near Distance to the near clipping plane.
    @param far Distance to the far clipping plane.

    @return None
    """
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gluPerspective(fov, aspect_ratio, near, far)
    gl.glMatrixMode(gl.GL_MODELVIEW)

def set_camera_view() -> None:
    """
    @brief Set the camera view for the 3D scene.

    @details Moves the camera back by translating the view along the negative z-axis.

    @return None
    """
    gl.glTranslatef(0.0, 0.0, -5.0)  # Move the camera back
