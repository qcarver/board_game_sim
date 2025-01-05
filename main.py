import random

class Card:
    def __init__(self, name, text, cost):
        self.name = name  # Name of the card
        self.text = text  # Description of the card's effect
        self.cost = cost  # Dictionary of resource and quantity (e.g., {Resource.POWER: 2, Resource.HEAT: 1}) (e.g., [[Resource.POWER, 2], [Resource.HEAT, 1]])

    def __str__(self):
        return f"{self.name}"

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
        self.payout = {resource: 0 for resource in Resource}  # Track the player's previous payout

class CardDeck:
    def __init__(self, card_data):
        """Initialize the CardDeck with card data from a CSV array."""
        self.deck = []
        for line in card_data:
            parts = line.split(', ')
            name = parts[0]
            text = parts[1]
            cost = {
                Resource[parts[i].upper()]: int(parts[i + 1])
                for i in range(2, len(parts), 2)
            }
            self.deck.append(Card(name, text, cost))
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
        self.card_deck = CardDeck([
            "Power Boost, Increases power production, POWER, 2, ORDER, 1",
            "Heat Shield, Reduces heat damage, HEAT, 3, EXPORTS, 1",
            "Trade Expansion, Adds trade routes, IMPORTS, 2, INDEPENDENCE, 1, ORDER, 1"
        ])

    def draw_card(self,player):
        response = input(f"{player.name} (draw card)? [Y]: ") or "Y"
        if response.lower() == 'q':
            print("Game terminated by user.")
            exit()
        if response.upper() == "Y":
            card = self.card_deck.draw_card()
            if card:
                player.cards.append(card)
                print(f"{player.name} drew {card}.")
            else:
                print("The deck is empty!")
        else :
                print(f"{player.name} didn't draw a card.")

    def calculate_payout(self, player):
        # Reset previous payout
        player.payout = {resource: 0 for resource in Resource}
        for _, car in player.train_cars:
            car_payouts = TRADE_PAYOUT_MAP[car.car_type]
            for resource_name in car_payouts:
                resource_enum = Resource[resource_name.upper()]
                player.resources[resource_enum] += car.proficiency
                player.payout[resource_enum] += car.proficiency
        # Display detailed payout information
        receipt = player.name + "'s Payout" 
        for resource, amount in player.payout.items():
            if amount > 0:
                receipt += ", " + resource.name + "+" + str(amount) 
        print(f"{receipt}")

    def action_phase(self,player):
        """Handle the Action phase for a player."""
        print("Actions available:")
        for index, card in enumerate(player.cards, start=1):
            print(f"{index}. {card}")
        print("B. Barter")
        print("P. Pass")

        valid_input = False
        while not valid_input:
            action_input = input("Choose an action (1, 2, ..., B, P): ").strip().upper()

            if action_input.startswith("B"):
                print("Barter selected. Implement barter logic here.")
                valid_input = True
            elif action_input.startswith("P"):
                print(f"{player.name} passes the action phase.")
                valid_input = True
            else:
                try:
                    card_index = int(action_input) - 1
                    if 0 <= card_index < len(player.cards):
                        selected_card = player.cards[card_index]
                        print(f"Playing card: {selected_card}")
                        # Implement card action logic here
                        valid_input = True
                    else:
                        print("Invalid card selection.")
                except ValueError:
                    print("Invalid input. Please choose a valid action.")

    def run_game(self):
        for player in self.players:
            print(f"--- Round {self.round} ---")
            if self.round == 1: 
                player.name = input(f"What is {player.trade.name}'s name? [{player.name}]: ") or player.name
            for phase in ["Draw", "Payout", "Action"]:
                match phase:
                    case "Draw":
                        self.draw_card(player)
                    case "Payout":
                        self.calculate_payout(player)
                    case "Action":
                        self.action_phase(player)
                        # Increment the round after the last player's Action phase
                        if player == self.players[-1] :
                            self.round += 1  

# Run the game
game = Game()
game.run_game()
