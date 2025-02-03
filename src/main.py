#################### Bézier Curve Visualization ####################
########## Dependencies ##########
import glfw
import imgui
import numpy as np
from display import Camera
from utils import setup_opengl, setup_camera, initialize_control_points, initialize_transformations, handle_window_resize, handle_imgui_controls, render_bezier_curve

########## Main Function ##########
def main() -> None:
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)

    window = glfw.create_window(800, 600, "Bezier Curve", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return

    # Setup
    renderer = setup_opengl(window)
    camera = setup_camera()
    control_points = initialize_control_points()
    transformations = initialize_transformations()

    width, height = glfw.get_window_size(window)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()
        camera.update(window)
        camera.set_camera_view()

        width, height = handle_window_resize(window, width, height)

        control_points, transformations = handle_imgui_controls(control_points, transformations)

        render_bezier_curve(control_points, transformations)

        imgui.render()
        renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    renderer.shutdown()
    imgui.destroy_context()
    glfw.terminate()

if __name__ == "__main__":
    main()
