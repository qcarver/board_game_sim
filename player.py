"""
@author: qcarver@gmail.com  
@brief: Player class and enumerators, relations between player and train objects
@license: this is a WIP, it is private, not for distribution
"""
from enum import Enum
from .money import Resources, power, heat, independence, order, imports, exports
from .train import Car, CarType

class Trade(Enum):
    QUARRYMAN = 1
    SMELTER = 2
    BLACKSMITH = 3
    MACHINIST = 4
    NAVVY = 5 

CAR_TYPE_MAP = {
    Trade.QUARRYMAN: CarType.EXCAVATOR,
    Trade.SMELTER: CarType.FOUNDARY,
    Trade.BLACKSMITH: CarType.FORGE,
    Trade.MACHINIST: CarType.ENGINE,
    Trade.NAVVY: CarType.TRACKLAYER
}

TRADE_PAYOUT_MAP = {    #CCWR:2,        RESOURCE:4,     CCR:2
    CarType.EXCAVATOR:  Resources((2,heat),         (4,independence), (2,imports)),
    CarType.ENGINE:     Resources((2,independence), (4,imports),      (2,power)),
    CarType.FOUNDARY:   Resources((2,imports),      (4,power),        (2,order)),
    CarType.TRACKLAYER: Resources((2,power),        (4,order),        (2,exports)),
    CarType.FORGE:      Resources((2,order),        (4,exports),      (2,heat))
}

class Player:
    def __init__(self, name, trade):
        self.name = name
        self.trade = trade  # Enumerator for the player's trade
        self.cards = []  # Player's card collection
        self.train_cars = [Car(car_type=CAR_TYPE_MAP[trade], proficiency=1)]  # Initial train and car based on trade
        self.resources = Resources()  # Initialize the player's resources to 0

