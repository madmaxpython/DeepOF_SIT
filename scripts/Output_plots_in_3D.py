#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:34:35 2024
Modified on Jun 19 19 15:13:04 2025

Code to generate 3D plots in Restrepo et al DPN.

####

@author: chemarestrepo, modified by @madmaxpython
"""

import pandas as pd
import plotly.graph_objs as go
from rich import palette
from scipy.stats import spearmanr


def three_dimension_plot(animal_df: pd.DataFrame,
                         palette: dict,
                         classification: str,
                         x_axis: str,
                         y_axis: str,
                         z_axis: str,
                         x_axis_label: str,
                         y_axis_label: str,
                         z_axis_label: str,
                         graph_title: str,
                         save: bool,
                         path: str,
                         camera_coordinates: dict = {"x": 1.2, "y": 1.9, "z": 0.0}
                         ):
    """
    :param animal_df: animal data to be plotted
    :param palette: color palette as a dict, each key is a group
    :param classification: type of classification to use
    :param x_axis: x-axis data
    :param y_axis: y-axis data
    :param z_axis: z-axis data
    :param x_axis_label: x-axis label
    :param y_axis_label: y-axis label
    :param z_axis_label: z-axis label
    :param graph_title: Graph title
    :param save: Save the plot as html and a png
    :param path: path to save the plot
    :param camera_coordinates: Camera coordinates to set the view when saving png
    """

    fig = go.Figure()

    for category in animal_df[classification].unique():
        print(category)

        fig.add_trace(go.Scatter3d(
            x=animal_df[animal_df[classification] == category][x_axis],
            y=animal_df[animal_df[classification] == category][y_axis],
            z=animal_df[animal_df[classification] == category][z_axis   ],
            mode='markers',
            marker=dict(
                size=6,
                color=palette[category],
            ),
            name=category
        ))

    # Set the layout of the figure
    fig.update_layout(
        title= graph_title,
        scene=dict(
            xaxis_title=x_axis_label,
            yaxis_title=y_axis_label,
            zaxis_title=z_axis_label)
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                backgroundcolor='white',
                gridcolor='lightgrey',
                zerolinecolor='lightgrey',
            ),
            yaxis=dict(
                backgroundcolor='white',
                gridcolor='lightgrey',
                dtick=0.2,
                zerolinecolor='lightgrey',
            ),
            zaxis=dict(
                backgroundcolor='white',
                gridcolor='lightgrey',
                zerolinecolor='lightgrey',
            ),
            bgcolor='white'  # removes the blue 3D "cube" background
        )
    )
    fig.update_layout(
        showlegend=False,  # Hides the legend
        title=None  # Removes the title
    )

    fig.update_layout(scene_camera=dict(
        eye=camera_coordinates  # custom camera position
    ))
    # Show figure
    fig.show()
    if save:
        fig.write_image(f"{path}.png", width=1000, height=1000, scale=6)
        fig.write_html(f"{path}.html")



if __name__ == '__main__':
    color = {
        'CSDS': {
            "Control": 'blue',
            "Stress": "orange"},
        'SIR_Classification': {
            "Control": "#332288",
            "Resilient": "#029542",
            "Susceptible": "#88ccee"}
    }

    animal_data = pd.read_csv(
        '/Users/max/Desktop/THESE/PROJECTS/jose_data/Article/Male_data.csv')


    animal_data = animal_data.astype({'Animal_ID': 'category',
                                              'CSDS': 'category',
                                              'SIR_Classification': 'category'})

    three_dimension_plot(animal_data,
                         color["SIR_Classification"],
                         "SIR_Classification",
                         "Distance_based_ratio_typeB",
                         'SIR_typeB',
                         'Index',
                         'Distance-based SIR TypeB',
                         'Time-based SIR TypeB',
                         'Social Engagement Index',
                         'test',
                         True,
                         '/Users/max/Desktop/THESE/PROJECTS/jose_data/Figure_article/3D_plot_Male')



