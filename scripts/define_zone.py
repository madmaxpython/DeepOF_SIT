#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:36:12 2024

Script to select SIZ corners
based on code from DeepOF package for arena definition

@author: chemarestrepo and modify by madmaxpython

"""
import os
import numpy as np

import cv2
from dask_image.imread import imread

import deepof.data

base_path = ''

my_deepof_project = deepof.data.load_project(os.path.join(base_path,'CSDS_DeepOF'))

my_deepof_project.load_exp_conditions(os.path.join(base_path,"Data/test_conditions.csv"))

video_list = my_deepof_project._videos

def get_SIZ_areas(video_list):

	SIZ_area_params = []

	for i, video_path in enumerate(video_list):

		SIZ_area_corners, h, w = extract_polygonal_arena_coordinates(
			os.path.join(my_deepof_project._project_path, my_deepof_project._project_name, "Videos", video_path),
			i,
			video_list,
			)

		cur_SIZ_area_params = SIZ_area_corners

		SIZ_area_params.append(cur_SIZ_area_params)

	return SIZ_area_params


def retrieve_SIZ_corners_from_image(
    frame: np.ndarray, cur_vid: int, videos: list
): 
    """Open a window and wait for the user to click on all corners of the polygonal arena.

    The user should click on the corners in sequential order.

    Args:
        frame (np.ndarray): Frame to display.
        arena_type (str): Type of arena to be used. Must be one of the following: "circular-manual", "polygon-manual".
        cur_vid (int): Index of the current video in the list of videos.
        videos (list): List of videos to be processed.

    Returns:
        corners (np.ndarray): nx2 array containing the x-y coordinates of all n corners.

    """
    SIZ_corners = []

    def click_on_corners(event, x, y, flags, param):
        # Callback function to store the coordinates of the clicked points
        nonlocal SIZ_corners, frame

        if event == cv2.EVENT_LBUTTONDOWN:
            SIZ_corners.append((x, y))

    # Resize frame to a standard size
    frame = frame.copy()

    # Create a window and display the image
    cv2.startWindowThread()

    while True:
        frame_copy = frame.copy()

        cv2.imshow(
            "Select SIZ corners - (q: exit / d: delete{}) - {}/{} processed".format(
                (" / p: propagate last to all remaining videos" if cur_vid > 0 else ""),
                cur_vid,
                len(videos),
            ),
            frame_copy,
        )

        cv2.setMouseCallback(
            "Select SIZ corners - (q: exit / d: delete{}) - {}/{} processed".format(
                (" / p: propagate last to all remaining videos" if cur_vid > 0 else ""),
                cur_vid,
                len(videos),
            ),
            click_on_corners,
        )

        # Display already selected corners
        if len(SIZ_corners) > 0:
            for c, corner in enumerate(SIZ_corners):
                cv2.circle(frame_copy, (corner[0], corner[1]), 4, (40, 86, 236), -1)
                # Display lines between the corners
                if len(SIZ_corners) > 1 and c > 0:
                    if len(SIZ_corners) < 5:
                        cv2.line(
                            frame_copy,
                            (SIZ_corners[c - 1][0], SIZ_corners[c - 1][1]),
                            (SIZ_corners[c][0], SIZ_corners[c][1]),
                            (40, 86, 236),
                            2,
                        )

        # Close the polygon
        if len(SIZ_corners) > 2:
            if len(SIZ_corners) < 5:
                cv2.line(
                    frame_copy,
                    (SIZ_corners[0][0], SIZ_corners[0][1]),
                    (SIZ_corners[-1][0], SIZ_corners[-1][1]),
                    (40, 86, 236),
                    2,
                )


        cv2.imshow(
            "Select SIZ corners - (q: exit / d: delete{}) - {}/{} processed".format(
                (" / p: propagate last to all remaining videos" if cur_vid > 0 else ""),
                cur_vid,
                len(videos),
            ),
            frame_copy,
        )

        # Remove last added coordinate if user presses 'd'
        if cv2.waitKey(1) & 0xFF == ord("d"):
            SIZ_corners = SIZ_corners[:-1]

        # Exit is user presses 'q'
        if len(SIZ_corners) > 2:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Exit and copy all coordinates if user presses 'c'
        if cur_vid > 0 and cv2.waitKey(1) & 0xFF == ord("p"):
            SIZ_corners = None
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)

    # Return the corners
    return SIZ_corners


def extract_polygonal_arena_coordinates(
    video_path: str, video_index: int, videos: list
):
    """Read a random frame from the selected video, and opens an interactive GUI to let the user delineate the arena manually.

    Args:
        video_path (str): Path to the video file.
        arena_type (str): Type of arena to be used: "polygonal-manual".
        video_index (int): Index of the current video in the list of videos.
        videos (list): List of videos to be processed.

    Returns:
        np.ndarray: nx2 array containing the x-y coordinates of all n corners of the polygonal arena.
        int: Height of the video.
        int: Width of the video.

    """
    current_video = imread(video_path)
    current_frame = np.random.choice(current_video.shape[0])

    # Get and return the corners of the SIZ
    try:
        import google.colab

        arena_corners = retrieve_SIZ_corners_from_colab(
            current_video[current_frame].compute(),
            video_index,
            videos,
        )

    except ImportError:
        arena_corners = retrieve_SIZ_corners_from_image(
            current_video[current_frame].compute(),
            video_index,
            videos,
        )
    return arena_corners, current_video.shape[2], current_video.shape[1]


# Execute main get_SIZ_areas() using my_deepof_project._videos
coord = get_SIZ_areas(video_list)

type_coord = 'SIZ'

if type_coord == 'SIZ':
    with open(os.path.join(base_path,"Data/SIZ_params.txt"), "w") as f:
        f.write("[\n")
        for sublist in coord:
            f.write(f"{sublist},\n")
        f.write("]\n")

if type_coord == 'arena':
    with open(os.path.join(base_path,"Data/arena_params_bodygraph14.txt"), "w") as f:
        for sublist in coord:
            f.write(f"{sublist}\n")