from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class Animator:
    """
    The `Animator` class creates an animation to illustrate the path followed by light, moved by the principle of
    least time given the medium interfaces.

    Attributes:
    -----------
    path : ndarray
        A numpy array that contains the data points in the path that light follows.
    velocities : Tuple [float, float]
        A tuple that contains the velocities of the light in the two media.
    plane_size : Tuple [float, float]
        A tuple that defines the dimensions of the 2D plane of the animation.
    total_frames : int
        The total number of frames in the animation.
    title : str
        The title of the animation.
    image_filename : str
        The file location for the optional image to be used as the marker for light in the animation.
    image_zoom : float
        The zoom factor to apply to the image defined by `image_filename`.

    Methods:
    --------
    __init__(self, path: np.ndarray, velocities: Tuple[float, float], plane_size: Tuple[float, float],
              total_frames: int = 200, title: str = "Animation of Light Path",
              image_filename: str = None, image_zoom: float = 0.5) -> None:
        Initializes the animation with provided parameters, default markers are used if no image is provided.
    init() -> Tuple:
        Initializes the markers and paths for the animation.
    animate(i: int) -> Tuple:
        Updates the markers and paths for the `i`th frame of the animation.
    generate_frames() -> List:
        Generates all frames for the animation, marking the position of light in each frame.
    run() -> None:
        Creates and runs the animation.
    """
    def __init__(self, path: np.ndarray, velocities: Tuple[float, float], plane_size: Tuple[float, float],
                 total_frames: int = 200, title: str = "Animation of Light Path", image_filename: str = None,
                 image_zoom: float = 0.5):
        self.path = path
        self.velocities = velocities
        self.plane_size = plane_size
        self.total_frames = total_frames
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')
        self.title = title
        self.use_image = False
        self.scat = None
        if image_filename:
            try:
                self.marker_image = mpimg.imread(image_filename)
                self.imagebox = AnnotationBbox(OffsetImage(self.marker_image, zoom=image_zoom), (0, 0), frameon=False)
                self.ax.add_artist(self.imagebox)
                self.imagebox.set_visible(False)
                self.use_image = True
            except FileNotFoundError:
                print(f"Error: File '{image_filename}' not found. Falling back to default marker.")
            except Exception as e:
                print(f"Error loading image '{image_filename}': {e}. Falling back to default marker.")

        if not self.use_image:
            self.scat = self.ax.scatter([], [], s=50, color='black')  # Default to black dot if no image

        self.frames = self.generate_frames()

    def init(self):
        self.line.set_data([], [])
        if not self.use_image:
            self.scat.set_offsets(np.empty((0, 2)))
        return self.line, self.scat if self.scat else self.imagebox

    def animate(self, i):
        """
        This function updates the marker and path of light for each frame 'i' of the animation.
        If a marker image is being used, it sets the image's location to the current frame's position.
        Otherwise, it updates the scatter plot (which is acting as the marker in this case).
        """
        frame = self.frames[i]
        x, y = frame
        self.line.set_data(self.path[:, 0], self.path[:, 1])
        if self.use_image:
            self.imagebox.xybox = (x, y)
            self.imagebox.set_visible(True)
        else:
            self.scat.set_offsets(np.c_[x, y])
        return self.line, self.scat if self.scat else self.imagebox

    def generate_frames(self):
        """
        This function generates all the frames for the animation. It does this by computing the distance of each
        segment of the path (from refraction interface) and determining how many frames should be spent on each
        segment proportional to its length. Then it computes the exact position of the marker (the light's position)
        on each of those frames.
        """
        frames = []
        path_lengths = np.sqrt(np.diff(self.path[:, 0]) ** 2 + np.diff(self.path[:, 1]) ** 2)
        total_length = np.sum(path_lengths)
        segment_frames = [int(self.total_frames * length / total_length) for length in path_lengths]
        for segment_index, num_frames in enumerate(segment_frames):
            for i in range(num_frames):
                t = i / num_frames
                x = np.interp(t, [0, 1], self.path[segment_index:segment_index + 2, 0])
                y = np.interp(t, [0, 1], self.path[segment_index:segment_index + 2, 1])
                frames.append((x, y))
        return frames

    def run(self):
        """
        This function actually runs (creates and displays) the animation. It sets up the axes of the graph, labels,
        and title, then creates the animation object using matplotlib's FuncAnimation. Finally, it shows the
        animation after setting up the legend.
        """
        self.ax.set_xlim(0, self.plane_size[0])
        self.ax.set_ylim(0, self.plane_size[1])
        self.ax.set_xlabel('X position')
        self.ax.set_ylabel('Y position')
        self.ax.set_title(self.title)
        self.ax.axhline(y=self.path[1][1], color='blue', linestyle='--', label='Material Interface')
        self.ax.plot(self.path[0][0], self.path[0][1], 'go', label='Start Point')
        self.ax.plot(self.path[-1][0], self.path[-1][1], 'ro', label='End Point')
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       frames=len(self.frames), interval=1000 / 30, blit=True)
        self.ax.legend()
        anim.save('animation.mp4', writer='ffmpeg', fps=30)
        plt.show()
