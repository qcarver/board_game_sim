import random

class Card:
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit

    def __str__(self):
        return f"{self.name} of {self.suit}"

from enum import Enum

class Resource(Enum):
    POWER = 1
    HEAT = 2
    INDEPENDENCE = 3
    ORDER = 4
    IMPORTS = 5
    EXPORTS = 6

class Trade(Enum):
    SMELTER = 1
    LINEMAN = 2
    NAVVY = 3
    QUARRYMAN = 4
    TECHNICIAN = 5

class CarType(Enum):
    FORGE = 1
    TRACKLAYER = 2
    EARTHMOVER = 3
    EXCAVATOR = 4
    ENGINE = 5

class Car:
    def __init__(self, car_type, proficiency=1):
        self.car_type = car_type  # Enumerator for the car's type
        self.proficiency = proficiency  # Proficiency level between 1 and 3

class Player:
    def __init__(self, name, trade):
        self.name = name
        self.trade = trade  # Enumerator for the player's trade
        self.cards = []  # Player's card collection
        self.train_cars = [["Train1", Car(car_type=CAR_TYPE_MAP[trade], proficiency=1)]]  # Initial train and car based on trade
        self.resources = {resource: 0 for resource in Resource}  # Initialize all resource counts to 0
        self.previous_payout = {resource: 0 for resource in Resource}  # Track the player's previous payout
        self.name = name
        self.trade = trade  # Enumerator for the player's trade
        self.cards = []  # Player's card collection
        self.train_cars = [["Train1", Car(car_type=CAR_TYPE_MAP[trade], proficiency=1)]]  # Initial train and car based on trade
        self.resources = {resource: 0 for resource in Resource}  # Initialize all resource counts to 0
        self.name = name
        self.trade = trade  # Enumerator for the player's trade
        self.cards = []  # Player's card collection
        self.train_cars = [["Train1", Car(car_type=CAR_TYPE_MAP[trade], proficiency=1)]]  # Initial train and car based on trade

class CardDeck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        names = ["Nine", "Jack", "Queen", "King", "Ten", "Ace"]
        self.deck = [Card(name, suit) for name in names for suit in suits] * 2  # Pinochle deck has two of each card
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop() if self.deck else None

CAR_TYPE_MAP = {
    Trade.SMELTER: CarType.FORGE,
    Trade.LINEMAN: CarType.TRACKLAYER,
    Trade.NAVVY: CarType.EARTHMOVER,
    Trade.QUARRYMAN: CarType.EXCAVATOR,
    Trade.TECHNICIAN: CarType.ENGINE
}

TRADE_PAYOUT_MAP = {
    CarType.FORGE: ["Power", "Exports", "Order"],
    CarType.TRACKLAYER: ["Heat", "Exports", "Order"],
    CarType.EARTHMOVER: ["Power", "Independence", "Imports"],
    CarType.EXCAVATOR: ["Heat", "Independence", "Exports"],
    CarType.ENGINE: ["Power", "Imports", "Order"]
}

class Game:
    def __init__(self):
        self.round = 1  # Initialize the game round
        self.players = [
            Player("CPU1", Trade.SMELTER),
            Player("CPU2", Trade.LINEMAN),
            Player("CPU3", Trade.NAVVY),
            Player("CPU4", Trade.QUARRYMAN),
            Player("CPU5", Trade.TECHNICIAN),
        ]
        self.card_deck = CardDeck()

    def calculate_payout(self, player):
        # Reset previous payout
        player.previous_payout = {resource: 0 for resource in Resource}
        for _, car in player.train_cars:
            car_payouts = TRADE_PAYOUT_MAP[car.car_type]
            for resource_name in car_payouts:
                resource_enum = Resource[resource_name.upper()]
                player.resources[resource_enum] += car.proficiency
                player.previous_payout[resource_enum] += car.proficiency
        # Display detailed payout information
        print(f"{player.name}'s Payout:")
        for resource, amount in player.previous_payout.items():
            if amount > 0:
                print(f"  {resource.name}: +{amount}, Total: {player.resources[resource]}")

    def run_game(self):
        for player in self.players:
            print(f"--- Round {self.round} ---")
            if self.round == 1: 
                player.name = input(f"What is {player.trade.name}'s name? [{player.name}]: ") or player.name
            for phase in ["Draw", "Payout", "Action"]:
                if player == self.players[-1] and phase == "Action":
                    self.round += 1  # Increment the round after the last player's Action phase
                if phase == "Action":
                    # Display submenu with indexed cards, barter, and pass options
                    print("Actions available:")
                    for index, card in enumerate(player.cards, start=1):
                        print(f"{index}. {card}")
                    print("B. Barter")
                    print("P. Pass")
                response = input(f"{player.name} ({phase} phase)? [Y]: ") or "Y"
                if response.lower() == 'q':
                    print("Game terminated by user.")
                    exit()
                if response.upper() == "Y":
                    if phase == "Draw":
                            card = self.card_deck.draw_card()
                            if card:
                                player.cards.append(card)
                                print(f"{player.name} drew {card}.")
                            else:
                                print("The deck is empty!")
                    elif phase == "Payout":
                        self.calculate_payout(player)
                else:
                    print(f"{player.name} skipped {phase}             if self.round == 1: 
                player.name = input(f"What is {player.trade.name}'s name? [{player.name}]: ") or player.namephase.")

# Run the game
game = Game()
game.run_game()
