"""
Own test environments for path planning based on IP-4-0-Test-Environments.ipynb
Author: Jan Fenker
"""

from os import wait
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

from numpy.char import center
from shapely.geometry import Point, Polygon, LineString, LinearRing
from shapely import buffer, plotting
import numpy as np

from IPBenchmark import Benchmark 
from IPEnvironment import CollisionChecker


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


def nixflake() -> dict():
    # setup a snowflake-like test environment for path planning

    environment = dict()
    flake_points = [(2, 9), (4, 9), (5.2, 6.8), (6.33, 9), (7.4, 9), (8, 8), (6.4, 4.8), (7.4, 2.75), (6.4, 0.75)]

    # TODO: make env more adaptable (currently snowflake centered around [0,0]
    # rel_cos = (2, 9)
    # rel_edges = get_rel_coordinates(flake_points, rel_cos)
    # print(rel_edges)
    # flake_points = scale(flake_points, 3)
    # environment["flake_base"] = Polygon(flake_points).buffer(.02)

    scaled_flake_points = scale(flake_points, 1.8)
    rotated = rotate_polygon(scaled_flake_points, np.pi/2.91)

    n_replicas = 6
    polygon_points = [rotated]
    rotated = None
    for i in range(n_replicas):
        rotated = rotate_polygon(polygon_points[0], np.pi/3*i)
        environment[f"rotated_{i}"] = Polygon(rotated).buffer(.02)
        polygon_points.append(rotated)

    return environment

def construct_square(edge_length, center=[0.0, 0.0], buffer_rate=0.02) -> Polygon:
    # constructs a square polygon based on a given center and edge length
    half_edge = edge_length / 2

    corner_l_up = [0, 0] # init empty left upper corner
    corner_l_up[0] = center[0] - half_edge
    corner_l_up[1] = center[1] + half_edge

    corner_r_up = [0, 0] # init empty point
    corner_r_up[0] = center[0] + half_edge
    corner_r_up[1] = center[1] + half_edge

    corner_l_lo = [0, 0] # init empty point
    corner_l_lo[0] = center[0] - half_edge
    corner_l_lo[1] = center[1] - half_edge

    corner_r_lo = [0, 0] # init empty point
    corner_r_lo[0] = center[0] + half_edge
    corner_r_lo[1] = center[1] - half_edge

    pol = Polygon([corner_l_up, corner_r_up, corner_r_lo, corner_l_lo])
    return pol

def castle_env() -> dict():
    # initiates a castle environment with collision objects for path planning
    castle_env = dict()
    towers = []
    towers.append(construct_square(edge_length=4, center=[8.0, 24.0], buffer_rate=0.05))
    towers.append(construct_square(edge_length=4, center=[22.0, 24.0], buffer_rate=0.05))
    towers.append(construct_square(edge_length=4, center=[22.0, 8.0], buffer_rate=0.05))
    towers.append(construct_square(edge_length=4, center=[8.0, 8.0], buffer_rate=0.05))
    for idx, tower in enumerate(towers):
        castle_env[f"tower_{idx}"] = tower
    walls = []
    walls.append(LineString([(8.0, 21.0),(8.0, 11.0)]).buffer(1.1))
    walls.append(LineString([(11.0, 24.0),(19.0, 24.0)]).buffer(1.1))
    walls.append(LineString([(22.0, 21.0),(22.0, 11.0)]).buffer(1.1))
    walls.append(LineString([(11.0, 8.0),(13.0, 8.0)]).buffer(1.1))
    walls.append(LineString([(17.0, 8.0),(19.0, 8.0)]).buffer(1.1))
    for idx, wall in enumerate(walls):
        castle_env[f"wall_{idx}"] = wall
    castle_env[f"fountain"] = Point(15, 15).buffer(2.0)

    return castle_env

if __name__ == "__main__":

    benchList = list()

    # environment["base"] = LineString([(11,0),(11,18)]).buffer(0.5)

    # prepare first environment
    flake_env = nixflake()
    description = "Test environment with a circular snowflake like shape with small paths to escape"
    limits = [[-22.0, 28.0], [-22.0, 22.0]]
    start = [0,0]
    end = [24, -2.]
    benchList.append(Benchmark("Nixflake", CollisionChecker(flake_env, limits), [start], [end], description, 2))

    # prepare second environemnt
    castle_env = castle_env()
    limits = [[0.0, 32.0], [0.0, 32.0]]
    start = [15.0, 20.0]
    end = [15.0, 28.0]
    description = "Test environment where the path planner needs to find a way out of a garded castle"
    benchList.append(Benchmark("CastleEscape", CollisionChecker(castle_env, limits), [start], [end], description, 3))
    
    # plot the created environments
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    plot_id = 0
    limits = benchList[plot_id].collisionChecker.getEnvironmentLimits()
    axes[0].set_xlim(limits[0])
    axes[0].set_ylim(limits[1])
    axes[0].set_aspect("equal")
    axes[0].grid(True, linewidth=0.3)

    start = benchList[plot_id].startList[0]
    end = benchList[plot_id].goalList[0]

    axes[0].scatter([start[0]], [start[1]], color="green", s=80, label="start")
    axes[0].scatter([end[0]], [end[1]], color="orange", s=80, label="goal")
    axes[0].legend()
    benchList[plot_id].collisionChecker.drawObstacles(axes[0])
    axes[0].set_title(f"Environment {benchList[plot_id].name}")

    plot_id = 1
    limits = benchList[plot_id].collisionChecker.getEnvironmentLimits()
    axes[1].set_xlim(limits[0])
    axes[1].set_ylim(limits[1])
    axes[1].set_aspect("equal")
    axes[1].grid(True, linewidth=0.3)

    start = benchList[plot_id].startList[0]
    end = benchList[plot_id].goalList[0]

    axes[1].scatter([start[0]], [start[1]], color="green", s=80, label="start")
    axes[1].scatter([end[0]], [end[1]], color="orange", s=80, label="goal")
    axes[1].legend()
    benchList[plot_id].collisionChecker.drawObstacles(axes[1])
    axes[1].set_title(f"Environment {benchList[plot_id].name}")

    plt.tight_layout()
    plt.show()

