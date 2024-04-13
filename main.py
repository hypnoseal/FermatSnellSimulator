from utils.config_loader import load_config
from simulation.simulator import PathSimulator
from visualization.animator import Animator

CONFIG_PATH = "config.yaml"

config = load_config(CONFIG_PATH)

speed_of_light = float(config["speed_of_light"])
material_velocity_1 = float(config["material"]["velocity_1"])
material_velocity_2 = float(config["material"]["velocity_2"])
point_a = (float(config["points"]["start_x"]), float(config["points"]["start_y"]))
point_b = (float(config["points"]["end_x"]), float(config["points"]["end_y"]))
interface_y = float(config["plane"]["interface_y"])
plane_size = (float(config["plane"]["size"]), float(config["plane"]["size"]))
frames = int(config["animation"]["frames"])
image = config["animation"]["image"]
image_zoom = float(config["animation"]["image_zoom"])
title = config["animation"]["title"]

simulator = PathSimulator(speed_of_light, material_velocity_1, material_velocity_2, point_a, point_b, interface_y,
                          plane_size)
animator = Animator(simulator.calculate_path(), (material_velocity_1, material_velocity_2), plane_size, frames,
                    title, image, image_zoom)
animator.run()
