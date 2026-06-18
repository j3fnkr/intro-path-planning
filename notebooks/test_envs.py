"""
Own test environments for path planning based on IP-4-0-Test-Environments.ipynb
Author: Jan Fenker
"""

import matplotlib.pyplot as plt

from shapely.geometry import Point, Polygon, LineString, LinearRing
from shapely import plotting
import numpy as np

from IPEnvironment import CollisionChecker


def nixflake():
    # setup a snowflake-like test environment for path planning
    nixflake = dict()

def get_rel_coordinates(points: list, new_zero_pos: tuple[float, float]):
    # takes the elements in the global cos and transforms them to points in new cos
    # returns list of points transformed relative to new_cos
    rel_edges = []
    for edge in flake_points:
        rel_edge_x = edge[0] - new_zero_pos[0]
        rel_edge_y = edge[1] - new_zero_pos[1]
        rel_edges.append((rel_edge_x, rel_edge_y))
    return rel_edges

def scale(points: list[tuple[float, float]], factor: float):
    # scale all points in list by factor
    scaled_points = []
    for p in points:
        new_x = p[0] * factor
        new_y = p[1] * factor
        scaled_points.append((new_x, new_y))
    return scaled_points

def rotate_polygon(points: list, radian: float, zero_pos: tuple = (1, 0)):
    rotated_points = []
    for p in points:
        new_x = p[0] * np.sin(radian) + p[1] * np.cos(radian)
        new_y = p[0] * np.cos(radian) - p[1] * np.sin(radian)
        rotated_points.append((new_x, new_y))

    return rotated_points

if __name__ == "__main__":

    environment = dict()
    flake_points = [(2, 9), (4, 9), (5.2, 6.8), (6.33, 9), (7.4, 9), (8, 8), (6.4, 4.8), (7.4, 2.75), (6.4, 0.75)]
    rel_cos = (2, 9)
    rel_edges = get_rel_coordinates(flake_points, rel_cos)
    print(rel_edges)
    # flake_points = scale(flake_points, 3)
    # environment["flake_base"] = Polygon(flake_points).buffer(.02)
    rotated = rotate_polygon(flake_points, np.pi/2)
    print(rotated)

    n_replicas = 6
    polygon_points = [flake_points]
    rotated = None
    for i in range(n_replicas):
        rotated = rotate_polygon(polygon_points[0], np.pi/3*i)
        environment[f"rotated_{i}"] = Polygon(rotated).buffer(.02)
        polygon_points.append(rotated)
    print(environment)
    # environment["base"] = LineString([(11,0),(11,18)]).buffer(0.5)

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(1,1,1)

    limits = [[-20.0, 27.0], [-10.0, 22.0]]
    coll_checker = CollisionChecker(environment, limits)
    limits = coll_checker.getEnvironmentLimits()
    ax.set_xlim(limits[0])
    ax.set_ylim(limits[1])
    ax.set_aspect("equal")
    ax.grid(True, linewidth=0.3)

    ax.scatter([2], [5], color="green", s=80, label="free point")
    ax.scatter([10], [10], color="orange", s=80, label="collision point")
    ax.legend()
    coll_checker.drawObstacles(ax)
    plt.show()
