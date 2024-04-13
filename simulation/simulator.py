import math
from typing import Tuple
import numpy as np
from scipy.optimize import minimize


class PathSimulator:
    """
    This is the `PathSimulator` class for simulating light refraction according to Fermat's Principle and Snell's Law.

    It uses numpy for complex numerical computations and provides an interface for setting up simulation parameters
    and performing the actual computation.

    Attributes
    ----------
    refractive_index_1 : float
        This is the refractive index for medium 1. A higher index means that light travels slower in the medium.
    refractive_index_2 : float
        This is the refractive index for medium 2. A higher index means that light travels slower in the medium.
    point_a : tuple
        Coordinates (x, y) for point A, where the light ray starts.
    point_b : tuple
        Coordinates (x, y) for point B, where the light ray should end
    interface_y : float
        The y-coordinate of the horizontal boundary between the two media.
    plane_size : tuple
        Size (width, height) of the entire simulation plane.
    speed_of_light : float
        Specifies the speed of light in vacuum.

    Methods
    -------
    __init__(self, refractive_index_1, refractive_index_2, point_a, point_b, interface_y=0):
    Initializes the simulator with given refractive indices, points A and B, and interface coordinate.

    calculate_distance_and_incidence_angle(self, x): For a given x-coordinate on the interface, calculates the
    distance and incidence angle for the light ray traveling from point A, reflecting off the interface at this
    x-coordinate, and then reaching point B.

    time_to_travel(self, x): For a given x-coordinate on the interface, calculates the time for a light ray to travel
    from point A, reflect off the interface at this x-coordinate, and then reach point B.

    calculate_optimal_path(self): Calculates and returns the x-coordinate on the interface that minimizes the travel
    time for the light ray.

    calculate_path(self, x): Given the x-coordinate on the interface where the light ray reflects, this method
    calculates the entire path of the light ray from point A, via the reflection point, to point B. Returns the path
    as a list of points (x, y).
    """

    # Constructor to initialize the simulation parameters.
    def __init__(self, speed_of_light: float, material_velocity_1: float, material_velocity_2: float,
                 point_a: Tuple[float, float], point_b: Tuple[float, float],
                 interface_y: float, plane_size: Tuple[float, float]):
        # Speed of light in vacuum (meters/second)
        self.speed_of_light = speed_of_light
        # Calculate refractive indices for the two materials
        self.refractive_index_1 = self.speed_of_light / material_velocity_1
        self.refractive_index_2 = self.speed_of_light / material_velocity_2
        # Start and end points of the light path as tuples
        self.point_a = point_a
        self.point_b = point_b
        # y-coordinate where the two mediums meet (the material boundary)
        self.interface_y = interface_y
        # Dimensions of the 2D simulation plane as a tuple
        self.plane_size = plane_size

    # Calculate the Euclidean distance from point A to the interface and the incidence angle.
    def calculate_distance_and_incidence_angle(self, x_interface):
        """
        Given an x_coordinate on the interface, this method computes the distance and incidence angle from point A to
        the interface. Physics Concept: The incidence angle is the angle that the incoming ray makes with the surface
        normal (the line perpendicular to the surface at the point of incidence).
        """
        # Calculate horizontal and vertical differences
        dx = x_interface - self.point_a[0]
        dy = self.interface_y - self.point_a[1]
        # Calculate distance using Pythagorean theorem
        distance_1 = np.sqrt(dx ** 2 + dy ** 2)
        # Incidence angle based on the arctangent of opposite over adjacent side
        incidence_angle = math.atan2(dy, dx)  # Right-triangle opposite/adjacent
        return distance_1, incidence_angle

    # Compute the total time taken for light to travel through both mediums.
    def time_to_travel(self, x_interface):
        """
        This method determines the total time taken for the light beam to travel the specified path. Physics Concept:
        The total travel time is the sum of the time spent in each medium, calculated as distance divided by speed (
        speed here is the speed of light adjusted by the refractive index)
        """
        distance_1, incidence_angle = self.calculate_distance_and_incidence_angle(x_interface)

        # Calculate distances in each medium
        segment_1 = distance_1  # Total distance from A to interface
        segment_2 = np.sqrt((self.point_b[0] - x_interface) ** 2 + (self.point_b[1] - self.interface_y) ** 2)

        # Compute time spent in each medium, considering the respective speeds
        time_material_1 = segment_1 / self.speed_of_light * self.refractive_index_1
        time_material_2 = segment_2 / self.speed_of_light * self.refractive_index_2

        return time_material_1 + time_material_2

    # Determine the x-coordinate at the interface that minimizes the travel time.
    def calculate_optimal_path(self):
        """
        This function uses an optimization algorithm to find the x-coordinate on the interface that results in the
        least time of travel. Physics Concept: Fermat's Principle aka the principle of least time states that the
        path taken by a ray between two given points is the path that requires the least time.
        """
        # Calculate the minimum and maximum x values from point A and point B and define the bounds for the optimizer
        # based on the coordinates of points A and B
        min_x = min(self.point_a[0], self.point_b[0])
        max_x = max(self.point_a[0], self.point_b[0])

        # Define the bounds for the optimizer to use
        bounds_x = [(min_x, max_x)]

        # Set the initial guess for the optimizer as the x-coordinate of point A
        x0 = self.point_a[0]

        # Use a minimization technique from SciPy to find the optimal path that minimizes the time of travel
        res = minimize(self.time_to_travel, x0, method='L-BFGS-B', bounds=bounds_x,
                       options={'xatol': 1e-10, 'disp': True})

        return res.x[0]

    # Calculate the full path of light from point A to B through the interface.
    def calculate_path(self):
        """
        With the optimal reflection x_coordinate determined, the complete path of the ray can be computed. Physics
        Concept: Snell's Law is the foundation for this method. Snell's Law relates the incidence angle,
        the refraction angle, and the refractive indices of the two media.
        """
        # Find the optimal interface x-coordinate
        x_interface_optimal = self.calculate_optimal_path()

        # Compute distance and incidence angle at this interface point
        distance_1, incidence_angle = self.calculate_distance_and_incidence_angle(x_interface_optimal)

        # Calculate refraction angle
        sine_incidence = math.sin(incidence_angle)
        sine_refraction = (self.refractive_index_1 / self.refractive_index_2) * sine_incidence
        sine_refraction = np.clip(sine_refraction, -1, 1)
        refraction_angle = math.asin(sine_refraction)

        # Calculate the x,y coordinates for the incidence point
        x_incidence = self.point_a[0] + distance_1 * math.cos(incidence_angle)
        y_incidence = self.point_a[1] + distance_1 * math.sin(incidence_angle)

        # Calculate the second segment distance in the second material
        segment_2 = np.sqrt((self.point_b[0] - x_interface_optimal) ** 2 + (self.point_b[1] - self.interface_y) ** 2)

        # Determine the direction of the refracted path
        if self.point_b[0] != x_interface_optimal:
            slope = (self.point_b[1] - self.interface_y) / (self.point_b[0] - x_interface_optimal)
            angle_to_horizontal = math.atan(slope)
        else:
            # Handle the vertical case
            angle_to_horizontal = math.pi / 2 * np.sign(self.point_b[1] - self.interface_y)

        # Calculate the x,y coordinates for the refraction point based on the direction after refraction
        x_refraction = x_interface_optimal + segment_2 * math.cos(angle_to_horizontal)
        y_refraction = self.interface_y + segment_2 * math.sin(angle_to_horizontal)

        # Define the path segments for visual representation or further analysis
        path_segment_1 = np.array([self.point_a, [x_incidence, self.interface_y]])
        path_segment_2 = np.array([[x_refraction, y_refraction], self.point_b])

        return np.concatenate((path_segment_1, path_segment_2), axis=0)
