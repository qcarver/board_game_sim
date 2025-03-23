"""
@Author: qcarver@gmail.com
@brief: This file contains the classes and enumerators for the game's train and car objects.
"""

from enum import Enum

class CarType(Enum):
    EXCAVATOR = 1
    FOUNDARY = 2
    FORGE = 3
    ENGINE = 4
    TRACKLAYER = 5

class Car:
    def __init__(self, car_type : CarType, speed: int = 1):
        self.car_type = car_type  # Enumerator for the car's type
        self.speed = speed  # speed between 1 and 5