# Fermat-Snell Light Path Simulation

Welcome to the Fermat-Snell Light Path Simulation project. This project simulates a light ray's path through two different media based on Fermat's principle of least time and Snell's law of refraction.

## Description 

The project consists of two primary Python files, `simulator.py` and `animator.py`, which incorporate important principles of optics to predict and visualize how light behaves at the interface of two material mediums.

## Inspiration for Default Configuration

The default configuration of my Fermat-Snell Light Path Simulation is inspired by a fascinating observation about ant behavior, specifically how ants choose their paths. A 2013 article on Phys.org describes an experiment suggesting that ants appear to adhere to Fermat's Principle of Least Time when selecting their routes. This principle, traditionally associated with the behavior of light, states that the path taken between two points by a system is the one that can be traversed in the least time.

This study provides a cross-disciplinary link between biology and physics, demonstrating nature's inherent efficiency, which is mirrored in optical phenomena. In my simulation, I adopt this principle by setting up scenarios where light rays, analogous to ants, navigate through different mediums—each with distinct refractive indices—aiming to find the quickest path from point A to point B.

For more information on the experiment and its implications, visit the following link: [Ants and Fermat's Principle](https://phys.org/news/2013-04-ants-fermat-principle.html). This research not only inspires the setup of my simulation but also validates the broader applicability of Fermat's Principle beyond traditional physics.

### Simulation Details

While the default configuration of this simulation draws inspiration from "Ants and Fermat's Principle", the actual code is fundamentally designed to simulate the behavior of light passing through various mediums. This ensures that the simulation can be readily reconfigured to focus purely on optical physics, aligning with traditional applications of Fermat's Principle and Snell's Law.

By adjusting the parameters such as refractive indices and medium boundaries, users can explore a wide range of scenarios in optical physics. This flexibility allows the simulation to serve as an educational tool or a research aid for studying light behavior in complex environments. The core algorithm adapts seamlessly between biological analogies and strict physical simulations, showcasing the universality and adaptability of the underlying principles.

## Physics Concepts Utilized

This simulation project fundamentally relies on two main physical principles: Fermat's Principle (or the principle of least time) and Snell's Law.

### Fermat's Principle

Fermat's Principle, also known as the principle of least time, states that the path taken between two points by a ray of light is the one that can be traversed in the least time. This principle is pivotal in predicting how light behaves as it transitions through different media. In the simulation, we apply Fermat's Principle to calculate the path of light from point A to point B, which includes passing through an interface of varying refractive indices.

Mathematically, Fermat's Principle is represented by the equation:

![equation](https://latex.codecogs.com/gif.latex?%5Cdelta%20%5Cleft%28%20%5Cfrac%7B1%7D%7Bv%7D%20%5Cright%29%20%5Cint_%7BA%7D%5E%7BB%7D%20ds%20%3D%200)

Here:
- *A* and *B* are the starting and ending points of the path, respectively,
- *v* is the speed of light in the respective media, indicating how the optical density affects the light's speed,
- *ds* represents an infinitesimal segment along the path of light.

The integral calculates the total travel time, and the principle seeks a path where this value is stationary, typically a minimum.

### Snell's Law

Snell's law, also known as the law of refraction, is used to describe the relationship between the angles of incidence and refraction when light passes from one medium into another. It is crucial for determining the path light takes when it crosses the boundary from one medium to another.

Mathematically, Snell's Law is expressed as:

![equation2](https://latex.codecogs.com/gif.latex?%5Cinline%20n_1%20%5Csin%20%5Ctheta_1%20%3D%20n_2%20%5Csin%20%5Ctheta_2)

Here:
- *n1* and *n2* are the refractive indices of the first and second media, respectively,
- *θ1* is the angle of incidence, the angle between the incident ray and the normal to the surface at the point of interest,
- *θ2* is the angle of refraction, the angle between the refracted ray and the normal.

This project implements these two fundamental principles to simulate the behavior of light as it travels through two different media and predict how it refracts at the boundary.

## Architecture

### simulator.py

The `simulator.py` file contains the `PathSimulator` class that uses concepts from physics, such as Fermat's principle and Snell's law, to compute the path that light would follow from one point to another through the interface of two materials with different refractive indices.

The parameters required include:
- Speed of light: The universal speed of light in vacuum.
- Material_velocity_1 and Material_velocity_2: These represent the speed of light in the first and second medium, respectively, which are crucial for understanding how the light's speed changes due to the optical densities of the materials.
- Point_a and Point_b: The coordinates of the points between which the light's path is traced.
- Interface_y: This parameter represents the y-coordinate of the boundary between the two different mediums. It acts as the critical juncture at which the light's path is calculated for refraction based on Snell's law.

The `simulator.py` file structures these principles within the `PathSimulator` class and provides an interface for setting up simulation parameters and performing the actual computation.

- `__init__`: This constructor method initializes the simulator with the following parameters:
  - speed_of_light: The speed of light in vacuum.
  - material_velocity_1: The velocity of light in the first medium.
  - material_velocity_2: The velocity of light in the second medium.
  - point_a: The starting point of the light ray.
  - point_b: The ending point of the light ray.
  - interface_y: The y-coordinate of the interface between the two mediums.
  - plane_size: The size of the 2D simulation plane.

- `calculate_distance_and_incidence_angle`: For an x-coordinate at the interface, this method calculates the Euclidean distance and incidence angle from point A to the interface. Incidence angle is the angle the incoming ray makes with the surface normal.

- `time_to_travel`: For an x-coordinate at the interface, it calculates the time for a light ray to travel from point A, reflect off the interface at this x-coordinate, and then reach point B.

- `calculate_optimal_path`: It calculates the optimal path for the light ray to minimize the traveling time. This is done by performing a binary search for the optimal x-coordinate (with maximum iterations and threshold as stopping criteria), and uses the time_to_travel method for its calculation.

- `calculate_path`: Given the x-coordinate on the interface where the light ray reflects, this method calculates the entire path of the light ray from point A, via the reflection point, to point B. Returns the path as a list of points (x, y).

This `PathSimulator` class is the key component of our simulation architecture for modeling light path simulation through different media.

### animator.py

The `animator.py` file contains the `Animator` class that creates an animation illustrating the path of the light ray. This class uses Matplotlib's animation functionality to create and display a dynamic 2D plot.

Simulated path, media velocities, plane size, total number of frames for animation, optional image file and zoom factor are required as parameters for the `Animator` class.

Small methods inside the `Animator` class initializes and updates markers and paths for animation, generates frames and runs the animation.

## Getting Started 

These instructions will help you set up and run the project on your local machine:

### Prerequisites

You will need the following Python packages, which can be installed using the `requirements.txt` file.

To install the packages, run the following command:

`pip install -r requirements.txt`

### Customizing the Simulation Parameters

Modifying the config.yaml file allows for customizing the simulation. Below is a breakdown of the parameters and how to modify them:

- Plane: defines the dimensions of the simulation area. size refers to the entire area's size, and interface_y indicates the y-coordinate where the change in media occurs.
- Points: defines the coordinates of the start and end points for the light path. start_x and start_y denote the starting point's coordinates, whereas end_x and end_y represent the end point's coordinates.
- speed_of_light: is a numerical value representing the speed of light.
- Material: customizes the velocity of light within two different mediums. velocity_1 is the speed of light in the first medium, and velocity_2 is in the second medium.
- Animation: controls the output visual. frames define the animation's length, image sets the icon and should be a png, image_zoom changes the size of the image, and title sets the animation's caption.

### Running the Project

To run the project:

1. Clone the repository to your local machine.
2. Navigate to the location of the files in the terminal.
3. Run the main Python file with the command `python main.py`.

## Contributing

As this is a learning project, contributions in the form of suggestions, bug reports, or pull requests are welcome.

## License

This project is licensed under the MIT License, details of which can be found in `LICENSE.md`.