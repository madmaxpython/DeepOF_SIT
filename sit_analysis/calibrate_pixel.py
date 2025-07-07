import argparse
import random
from typing import Tuple

import cv2
import matplotlib.pyplot as plt
from numpy import sqrt


class LineBuilder:
    """Helper to let user draw exactly 2 points on matplotlib plot by clicking."""

    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self.draw)
        self.keypress = line.figure.canvas.mpl_connect('key_press_event', self.key)

    def draw(self, event):
        if len(self.xs) < 2:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)
            self.line.figure.canvas.draw()

    def key(self, event):
        if event.key == 'q':
            plt.close('all')
        if event.key == 'a':
            self.line.set_data([], [])
            self.ys, self.xs = [], []
            self.line.figure.canvas.draw()

    def get_points(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Return the two points selected by user."""
        if len(self.xs) == 2 and len(self.ys) == 2:
            return (self.xs[0], self.ys[0]), (self.xs[1], self.ys[1])
        else:
            raise ValueError("Exactly two points must be selected")


def plot_random_frame(video_path: str) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Display a random video frame and let user click two points to measure distance."""
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    random_frame_idx = random.randint(0, frame_count - 1)
    video.set(cv2.CAP_PROP_POS_FRAMES, random_frame_idx)
    ret, frame = video.read()
    video.release()

    if not ret:
        raise RuntimeError(f"Failed to read frame from video: {video_path}")

    fig, ax = plt.subplots()
    ax.invert_yaxis()
    fig.canvas.manager.set_window_title('Calibration Step')

    ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    line, = ax.plot([], [], marker='o', color='red', linestyle='-', linewidth=2)
    line_builder = LineBuilder(line)

    plt.title('Select two points for calibration (q to quit, a to reset)')
    plt.show()

    return line_builder.get_points()


def calibrate_pixel_size(video_path: str, known_distance_cm: float = None) -> float:
    """Calibrate pixel size based on user-selected points and known real-world distance."""
    p1, p2 = plot_random_frame(video_path)
    dist_px = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    if known_distance_cm is None:
        known_distance_cm = float(input("Enter the known distance in cm between the two points: "))

    pixel_size_cm = known_distance_cm / dist_px
    return pixel_size_cm


def main():
    parser = argparse.ArgumentParser(description="Calibrate pixel size from a video.")
    parser.add_argument("--video_path", type=str, help="Path to the video file")
    parser.add_argument("--distance", type=float, default=None,
                        help="Known distance in cm between two points (optional)")
    args = parser.parse_args()

    pixel_size = calibrate_pixel_size(args.video_path, args.distance)
    print(f"Pixel size: {pixel_size:.6f} cm/pixel")


if __name__ == "__main__":
    main()
