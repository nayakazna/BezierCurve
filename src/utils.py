########## Dependencies ##########
import glfw
import OpenGL.GL as gl
import imgui
import numpy as np
from imgui.integrations.glfw import GlfwRenderer
from display import Camera
from transformations import apply_transformations
from bezier import generate_bezier_curve

########## Helper Functions ##########
##### OpenGL Setup #####
def setup_opengl(window: glfw._GLFWwindow):
    glfw.make_context_current(window)
    imgui.create_context()
    renderer = GlfwRenderer(window)
    gl.glEnable(gl.GL_DEPTH_TEST)
    return renderer

##### Camera Setup #####
def setup_camera() -> Camera:
    camera = Camera()
    camera.set_perspective_projection()
    return camera

def initialize_control_points() -> np.ndarray:
    return np.array([
        [-2.0, -2.0, 3.0],
        [-1.0, 2.0, 0.0],
        [1.0, -1.0, -4.0],
        [2.0, 1.0, 1.0]
    ], dtype=float)

def initialize_transformations():
    return {
        "scale_x": 1.0, "scale_y": 1.0, "scale_z": 1.0,
        "rotation_x": 0.0, "rotation_y": 0.0, "rotation_z": 0.0,
        "reflection_axis": "None",
        "translate_x": 0.0, "translate_y": 0.0, "translate_z": 0.0,
        "shear_xy": 0.0, "shear_xz": 0.0, "shear_yx": 0.0, 
        "shear_yz": 0.0, "shear_zx": 0.0, "shear_zy": 0.0
    }

########## Handle Resizing ##########
def handle_window_resize(window: glfw._GLFWwindow, width: int, height: int):
    """Handle window resizing."""
    new_width, new_height = glfw.get_window_size(window)
    if new_width != width or new_height != height:
        width, height = new_width, new_height
        gl.glViewport(0, 0, width, height)
    return width, height

########## Handle IMGUI Controls ##########
def handle_imgui_controls(control_points: np.ndarray, transformations: dict) -> dict:
    reflection_axis = transformations['reflection_axis']
    scale_x, scale_y, scale_z = transformations['scale_x'], transformations['scale_y'], transformations['scale_z']
    rotation_x, rotation_y, rotation_z = transformations['rotation_x'], transformations['rotation_y'], transformations['rotation_z']
    translate_x, translate_y, translate_z = transformations['translate_x'], transformations['translate_y'], transformations['translate_z']
    shear_xy, shear_xz, shear_yx = transformations['shear_xy'], transformations['shear_xz'], transformations['shear_yx']
    shear_yz, shear_zx, shear_zy = transformations['shear_yz'], transformations['shear_zx'], transformations['shear_zy']

    imgui.new_frame()

    # Control points input
    imgui.set_next_window_size(300, 400)
    imgui.set_next_window_position(10, 10)
    imgui.begin("Control Points")
    for i in range(4):
        imgui.text(f"Control Point {i + 1}:")
        _, control_points[i][0] = imgui.input_float(f"X_{i+1}", control_points[i][0], step=0.1, format="%.1f")
        _, control_points[i][1] = imgui.input_float(f"Y_{i+1}", control_points[i][1], step=0.1, format="%.1f")
        _, control_points[i][2] = imgui.input_float(f"Z_{i+1}", control_points[i][2], step=0.1, format="%.1f")
    imgui.separator()
    imgui.end()

    # Transformation inputs
    imgui.set_next_window_size(300, 450)
    imgui.set_next_window_position(10, 450)
    imgui.begin("Transformation")
    
    # Reflection
    imgui.text("Reflection Axis:")
    if imgui.radio_button("None", reflection_axis == "None"):
        reflection_axis = "None"
    if imgui.radio_button("Reflect X", reflection_axis == "X"):
        reflection_axis = "X"
    if imgui.radio_button("Reflect Y", reflection_axis == "Y"):
        reflection_axis = "Y"
    if imgui.radio_button("Reflect Z", reflection_axis == "Z"):
        reflection_axis = "Z"
    imgui.separator()

    # Dilation
    imgui.text("Dilation:")
    _, scale_x = imgui.slider_float("Scale X", scale_x, 0.1, 5.0)
    _, scale_y = imgui.slider_float("Scale Y", scale_y, 0.1, 5.0)
    _, scale_z = imgui.slider_float("Scale Z", scale_z, 0.1, 5.0)
    imgui.separator()

    # Rotation
    imgui.text("Rotation (X, Y, Z axes):")
    # These sliders automatically convert degrees to radians
    _, rotation_x = imgui.slider_angle("Rotation X", rotation_x, 0.0, 360.0)
    _, rotation_y = imgui.slider_angle("Rotation Y", rotation_y, 0.0, 360.0)
    _, rotation_z = imgui.slider_angle("Rotation Z", rotation_z, 0.0, 360.0)
    imgui.separator()

    # Translation
    imgui.text("Translation:")
    _, translate_x = imgui.slider_float("Translate X", translate_x, -5.0, 5.0)
    _, translate_y = imgui.slider_float("Translate Y", translate_y, -5.0, 5.0)
    _, translate_z = imgui.slider_float("Translate Z", translate_z, -5.0, 5.0)
    imgui.separator()

    # Shearing
    imgui.text("Shearing:")
    _, shear_xy = imgui.slider_float("Shear XY", shear_xy, -1.0, 1.0)
    _, shear_xz = imgui.slider_float("Shear XZ", shear_xz, -1.0, 1.0)
    _, shear_yx = imgui.slider_float("Shear YX", shear_yx, -1.0, 1.0)
    _, shear_yz = imgui.slider_float("Shear YZ", shear_yz, -1.0, 1.0)
    _, shear_zx = imgui.slider_float("Shear ZX", shear_zx, -1.0, 1.0)
    _, shear_zy = imgui.slider_float("Shear ZY", shear_zy, -1.0, 1.0)
    imgui.separator()
    
    imgui.end()
    
    transformations = {
        "reflection_axis": reflection_axis,
        "scale_x": scale_x, "scale_y": scale_y, "scale_z": scale_z,
        "rotation_x": rotation_x, "rotation_y": rotation_y, "rotation_z": rotation_z,
        "translate_x": translate_x, "translate_y": translate_y, "translate_z": translate_z,
        "shear_xy": shear_xy, "shear_xz": shear_xz, "shear_yx": shear_yx,
        "shear_yz": shear_yz, "shear_zx": shear_zx, "shear_zy": shear_zy
    }

    return control_points, transformations


def render_bezier_curve(control_points: np.ndarray, transformations: dict):
    transformed_points = apply_transformations(
        control_points,
        transformations['reflection_axis'],
        transformations['scale_x'],
        transformations['scale_y'],
        transformations['scale_z'],
        transformations['rotation_x'],
        transformations['rotation_y'],
        transformations['rotation_z'],
        transformations['translate_x'],
        transformations['translate_y'],
        transformations['translate_z'],
        transformations['shear_xy'],
        transformations['shear_xz'],
        transformations['shear_yx'],
        transformations['shear_yz'],
        transformations['shear_zx'],
        transformations['shear_zy']
    )

    curve_points = generate_bezier_curve(transformed_points)

    # Clear buffer and set background color
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.2, 0.3, 0.3, 1.0)

    # Draw the Bézier curve
    gl.glLineWidth(5.0)
    gl.glColor3f(0.0, 1.0, 0.0)
    gl.glBegin(gl.GL_LINE_STRIP)
    for point in curve_points:
        gl.glVertex3f(point[0], point[1], point[2])
    gl.glEnd()

    # Draw the control points
    gl.glPointSize(10.0)
    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glBegin(gl.GL_POINTS)
    for point in transformed_points:
        gl.glVertex3f(point[0], point[1], point[2])
    gl.glEnd()

    # Draw the weight lines (optional)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3f(transformed_points[0][0], transformed_points[0][1], transformed_points[0][2])
    gl.glVertex3f(transformed_points[1][0], transformed_points[1][1], transformed_points[1][2])
    gl.glEnd()
    
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3f(transformed_points[2][0], transformed_points[2][1], transformed_points[2][2])
    gl.glVertex3f(transformed_points[3][0], transformed_points[3][1], transformed_points[3][2])
    gl.glEnd()