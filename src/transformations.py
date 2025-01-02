import numpy as np
from numpy import ndarray

def apply_transformations(
    points: ndarray,
    reflection_axis: str,
    scale_x: float,
    scale_y: float,
    scale_z: float,
    rotation_x_angle: float,
    rotation_y_angle: float,
    rotation_z_angle: float,
    translate_x: float,
    translate_y: float,
    translate_z: float,
    shear_xy: float = 0.0,
    shear_xz: float = 0.0,
    shear_yx: float = 0.0,
    shear_yz: float = 0.0,
    shear_zx: float = 0.0,
    shear_zy: float = 0.0
) -> ndarray:
    """
    @brief Apply reflection, scaling, rotation, translation, and shear to control points.

    @param points A numpy array of shape (n, 3) containing the points to be transformed.
    @param reflection_axis A string specifying the axis of reflection ("x", "y", "z", or "None").
    @param scale_x Scale factor along the x-axis.
    @param scale_y Scale factor along the y-axis.
    @param scale_z Scale factor along the z-axis.
    @param rotation_x_angle Rotation angle around the x-axis in degrees.
    @param rotation_y_angle Rotation angle around the y-axis in degrees.
    @param rotation_z_angle Rotation angle around the z-axis in degrees.
    @param translate_x Translation distance along the x-axis.
    @param translate_y Translation distance along the y-axis.
    @param translate_z Translation distance along the z-axis.
    @param shear_xy Shear factor in the xy-plane.
    @param shear_xz Shear factor in the xz-plane.
    @param shear_yx Shear factor in the yx-plane.
    @param shear_yz Shear factor in the yz-plane.
    @param shear_zx Shear factor in the zx-plane.
    @param shear_zy Shear factor in the zy-plane.

    @return A numpy array of shape (n, 3) containing the transformed points.
    """
    if reflection_axis != "None":
        points = np.array([reflection(p, reflection_axis.lower()) for p in points])

    points = np.array([scaling(p, scale_x, scale_y, scale_z) for p in points])

    rotation_x_quat = create_axis_quaternion('x', rotation_x_angle)
    rotation_y_quat = create_axis_quaternion('y', rotation_y_angle)
    rotation_z_quat = create_axis_quaternion('z', rotation_z_angle)

    points = np.array([rotate(p, rotation_x_quat) for p in points])
    points = np.array([rotate(p, rotation_y_quat) for p in points])
    points = np.array([rotate(p, rotation_z_quat) for p in points])

    points = np.array([shear(p, shear_xy, shear_xz, shear_yx, shear_yz, shear_zx, shear_zy) for p in points])

    points = np.array([p + np.array([translate_x, translate_y, translate_z]) for p in points])
    return points

def reflection(v: ndarray, axis: str) -> ndarray:
    """
    @brief Reflect a 3D vector across a specified axis.

    @param v A 3D numpy array representing the vector.
    @param axis A string specifying the axis of reflection ("x", "y", or "z").

    @return A reflected 3D numpy array.
    """
    if axis == 'x':
        return np.array([-v[0], v[1], v[2]])
    elif axis == 'y':
        return np.array([v[0], -v[1], v[2]])
    elif axis == 'z':
        return np.array([v[0], v[1], -v[2]])
    else:
        raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

def scaling(v: ndarray, kx: float, ky: float, kz: float) -> ndarray:
    """
    @brief Scale a 3D vector by specified factors along the x, y, and z axes.

    @param v A 3D numpy array representing the vector to scale.
    @param kx Scale factor along the x-axis.
    @param ky Scale factor along the y-axis.
    @param kz Scale factor along the z-axis.

    @return A scaled 3D numpy array.
    """
    return np.array([v[0] * kx, v[1] * ky, v[2] * kz])

def shear(v: ndarray, xy: float, xz: float, yx: float, yz: float, zx: float, zy: float) -> ndarray:
    """
    @brief Apply shear transformation to a 3D vector.

    @param v A 3D numpy array representing the vector to shear.
    @param xy Shear factor in the xy-plane.
    @param xz Shear factor in the xz-plane.
    @param yx Shear factor in the yx-plane.
    @param yz Shear factor in the yz-plane.
    @param zx Shear factor in the zx-plane.
    @param zy Shear factor in the zy-plane.

    @return A sheared 3D numpy array.
    """
    shear_matrix = np.array([
        [1, xy, xz],
        [yx, 1, yz],
        [zx, zy, 1]
    ])
    return shear_matrix @ v

def create_axis_quaternion(axis: str, angle_deg: float) -> ndarray:
    """
    @brief Create a quaternion from an axis of rotation and an angle.

    @param axis A string specifying the axis of rotation ("x", "y", or "z").
    @param angle_deg The rotation angle in degrees.

    @return A numpy array representing the quaternion.
    """
    angle_rad = np.radians(angle_deg)
    half_angle = angle_rad / 2
    s = np.sin(half_angle)
    c = np.cos(half_angle)

    if axis == 'x':
        return np.array([c, s, 0.0, 0.0])
    elif axis == 'y':
        return np.array([c, 0.0, s, 0.0])
    elif axis == 'z':
        return np.array([c, 0.0, 0.0, s])
    else:
        raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

def rotate(point: ndarray, quaternion: ndarray) -> ndarray:
    """
    @brief Rotate a point using a quaternion.

    @param point A 3D numpy array representing the point to rotate.
    @param quaternion A numpy array representing the quaternion.

    @return A rotated 3D numpy array.
    """
    point_quat = np.array([0.0, *point])
    quat_conj = np.array([quaternion[0], -quaternion[1], -quaternion[2], -quaternion[3]])
    result_quat = quaternion_multiply(quaternion_multiply(quaternion, point_quat), quat_conj)
    return result_quat[1:]

def quaternion_multiply(q1: ndarray, q2: ndarray) -> ndarray:
    """
    @brief Multiply two quaternions.

    @param q1 A numpy array representing the first quaternion.
    @param q2 A numpy array representing the second quaternion.

    @return A numpy array representing the product of the two quaternions.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    ])
