#################### Bézier Curve Visualization ####################
########## Dependencies ##########
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import numpy as np
from transformations import (
    reflection, scaling, shear, create_axis_quaternion, rotate, apply_transformations
)
from bezier import generate_bezier_curve
from display import set_perspective_projection, set_camera_view

########## Main Function ##########
def main() -> None:
    """Main function to run the Bézier Curve visualization application."""
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)

    window: glfw._GLFWwindow | None = glfw.create_window(800, 600, "Bezier Curve", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return

    ########## OpenGL Setup ##########
    glfw.make_context_current(window)

    imgui.create_context()
    renderer = GlfwRenderer(window)

    width, height = glfw.get_window_size(window)
    set_perspective_projection(60.0, width / float(height), 0.1, 100.0)
    set_camera_view()

    gl.glEnable(gl.GL_DEPTH_TEST)

    ########## CONTROL POINTS ##########
    control_points: np.ndarray = np.array([
        [-2.0, -2.0, 3.0],
        [-1.0, 2.0, 0.0],
        [1.0, -1.0, -4.0],
        [2.0, 1.0, 1.0]
    ], dtype=float)

    ########## TRANSFORMATION VARIABLES ##########
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    rotation_x: float = 0.0
    rotation_y: float = 0.0
    rotation_z: float = 0.0
    reflection_axis: str = "None"
    translate_x: float = 0.0
    translate_y: float = 0.0
    translate_z: float = 0.0
    shear_xy: float = 0.0
    shear_xz: float = 0.0
    shear_yx: float = 0.0
    shear_yz: float = 0.0
    shear_zx: float = 0.0
    shear_zy: float = 0.0

    ########## MAIN LOOP ########
    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()

        ########## WINDOW RESIZING ##########
        new_width, new_height = glfw.get_window_size(window)
        if new_width != width or new_height != height:
            width, height = new_width, new_height
            gl.glViewport(0, 0, width, height)

        ########## IMGUI CONTROL PANEL ##########
        imgui.new_frame()

        ######## CONTROL POINTS ########
        imgui.set_next_window_size(300, 400)
        imgui.set_next_window_position(10, 500)
        imgui.begin("Control Points")
        
        ##### INPUT FIELD #####
        for i in range(4):
            imgui.text(f"Control Point {i + 1}:")
            _, control_points[i][0] = imgui.input_float(f"X_{i+1}", control_points[i][0], step=0.1, format="%.1f")
            _, control_points[i][1] = imgui.input_float(f"Y_{i+1}", control_points[i][1], step=0.1, format="%.1f")
            _, control_points[i][2] = imgui.input_float(f"Z_{i+1}", control_points[i][2], step=0.1, format="%.1f")
        imgui.separator()
        imgui.end()

        ######## TRANSFORMATION ########
        imgui.set_next_window_size(300, 450)
        imgui.set_next_window_position(10, 10)
        imgui.begin("Transformation")

        ##### REFLECTION #####
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

        ##### SCALING #####
        imgui.text("Scaling:")
        _, scale_x = imgui.slider_float("Scale X", scale_x, 0.1, 5.0)
        _, scale_y = imgui.slider_float("Scale Y", scale_y, 0.1, 5.0)
        _, scale_z = imgui.slider_float("Scale Z", scale_z, 0.1, 5.0)
        imgui.separator()

        ##### ROTATION #####
        imgui.text("Rotation (X, Y, Z axes):")
        # These sliders automatically convert degrees to radians
        _, rotation_x = imgui.slider_angle("Rotation X", rotation_x, 0.0, 360.0)
        _, rotation_y = imgui.slider_angle("Rotation Y", rotation_y, 0.0, 360.0)
        _, rotation_z = imgui.slider_angle("Rotation Z", rotation_z, 0.0, 360.0)
        imgui.separator()

        ##### TRANSLATION #####
        imgui.text("Translation:")
        _, translate_x = imgui.slider_float("Translate X", translate_x, -5.0, 5.0)
        _, translate_y = imgui.slider_float("Translate Y", translate_y, -5.0, 5.0)
        _, translate_z = imgui.slider_float("Translate Z", translate_z, -5.0, 5.0)
        imgui.separator()

        ##### SHEARING #####
        imgui.text("Shearing:")
        _, shear_xy = imgui.slider_float("Shear XY", shear_xy, -1.0, 1.0)
        _, shear_xz = imgui.slider_float("Shear XZ", shear_xz, -1.0, 1.0)
        _, shear_yx = imgui.slider_float("Shear YX", shear_yx, -1.0, 1.0)
        _, shear_yz = imgui.slider_float("Shear YZ", shear_yz, -1.0, 1.0)
        _, shear_zx = imgui.slider_float("Shear ZX", shear_zx, -1.0, 1.0)
        _, shear_zy = imgui.slider_float("Shear ZY", shear_zy, -1.0, 1.0)
        imgui.separator()

        imgui.end()

        ########## RENDERING ##########
        ##### TRANSFORM CONTROL POINTS #####
        transformed_points: np.ndarray = apply_transformations(
            control_points,
            reflection_axis,
            scale_x,
            scale_y,
            scale_z,
            rotation_x,
            rotation_y,
            rotation_z,
            translate_x,
            translate_y,
            translate_z,
            shear_xy,
            shear_xz,
            shear_yx,
            shear_yz,
            shear_zx,
            shear_zy
        )


        # ##### LIGHTING ##### (Optional)
        # # Setup lighting
        # gl.glEnable(gl.GL_LIGHTING)
        # gl.glEnable(gl.GL_LIGHT0)  # Add a light source
        
        # # Set light properties
        # light_pos = [1.0, 1.0, 1.0, 0.0]  # Light position
        # light_color = [1.0, 1.0, 1.0, 1.0]  # White light
        # gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_pos)
        # gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, light_color)

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        
        ##### BÉZIER CURVE #####
        # Generate all points on the Bézier curve
        curve_points: np.ndarray = generate_bezier_curve(transformed_points)
        
        # Setup for renderin
        
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

        # Draw the weight lines
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(transformed_points[0][0], transformed_points[0][1], transformed_points[0][2])
        gl.glVertex3f(transformed_points[1][0], transformed_points[1][1], transformed_points[1][2])
        gl.glEnd()
        
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(transformed_points[2][0], transformed_points[2][1], transformed_points[2][2])
        gl.glVertex3f(transformed_points[3][0], transformed_points[3][1], transformed_points[3][2])
        gl.glEnd()

        ##### IMGUI WINDOW #####
        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    ########## CLEANUP ##########
    renderer.shutdown()
    imgui.destroy_context()
    glfw.terminate()

if __name__ == "__main__":
    main()
