"""
Own test environments for path planning based on IP-4-0-Test-Environments.ipynb
Author: Jan Fenker
"""

import matplotlib.pyplot as plt

from shapely.geometry import Point, Polygon, LineString, LinearRing
from shapely import plotting

from IPEnvironment import CollisionChecker


def nixflake():
    # setup a snowflake-like test environment for path planning
    nixflake = dict()



if __name__ == "__main__":

    environment = dict()
    environment["flake_base"] = Polygon([(4, 15), (6, 15), (9, 10), (12, 14), (13, 15), (14, 14), (11, 10), (14, 5), (12, 3)]).buffer(.2)
    # environment["base"] = LineString([(11,0),(11,18)]).buffer(0.5)

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(1,1,1)

    limits = [[-0.0, 27.0], [-5.0, 22.0]]
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