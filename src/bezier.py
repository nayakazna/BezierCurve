import numpy as np
from numpy import ndarray

def de_casteljau(P0: ndarray, P1: ndarray, P2: ndarray, P3: ndarray, t: float) -> ndarray:
    """
    @brief De Casteljau's algorithm to calculate a point on a cubic Bézier curve.

    @param P0 The first control point (3D vector).
    @param P1 The second control point (3D vector).
    @param P2 The third control point (3D vector).
    @param P3 The fourth control point (3D vector).
    @param t A float between 0 and 1 representing the interpolation factor.

    @return A 3D point on the Bézier curve at the given parameter t.
    """
    if not all(isinstance(P, np.ndarray) and P.shape == (3,) for P in [P0, P1, P2, P3]):
        raise ValueError("Control points must be numpy arrays of shape (3,).")
    if not isinstance(t, float):
        raise TypeError("t must be a float.")

    # LERP between control points
    P01 = (1 - t) * P0 + t * P1
    P12 = (1 - t) * P1 + t * P2
    P23 = (1 - t) * P2 + t * P3

    # LERP between the LERPed control points
    P012 = (1 - t) * P01 + t * P12
    P123 = (1 - t) * P12 + t * P23

    # LERPPPPPPPPPPP between the LERPed LERPed control points to get the final point on the curve (yeahhhh)
    P0123 = (1 - t) * P012 + t * P123

    return P0123

def generate_bezier_curve(control_points: list[ndarray], num_points: int = 100) -> ndarray:
    """
    @brief Generate points on the cubic Bézier curve using de Casteljau's algorithm.

    @param control_points A list of four 3D numpy arrays representing the control points.
    @param num_points The number of points to generate along the Bézier curve (default is 100).

    @return A numpy array of shape (num_points, 3) containing the points on the Bézier curve.
    """
    if len(control_points) != 4 or not all(isinstance(P, np.ndarray) and P.shape == (3,) for P in control_points):
        raise ValueError("control_points must be a list of four 3D numpy arrays.")
    if not isinstance(num_points, int):
        raise TypeError("num_points must be an integer.")

    curve_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        curve_point = de_casteljau(control_points[0], control_points[1], control_points[2], control_points[3], t)
        curve_points.append(curve_point)
    return np.array(curve_points)
