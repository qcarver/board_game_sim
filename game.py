"""
@bref: This file contains the game logic for the game. It's the 'main'
@details: it also has functions which deal with more than one class
@author: qcarver@gmail.com
@license: this is a WIP, it is private, not for distribution
"""
import copy
#import pdb #pdb.set_trace() # to pause for debugging
from .player import Player, Trade, TRADE_PAYOUT_MAP
from .train import CarType, Car
from .cards import Card, CardDeck
from .money import Resources, power, heat, independence, order, imports, exports

class Game:
    def __init__(self):
        self.round = 1  # Initialize the game round
        self.players =  [
            Player("CPU1", Trade.SMELTER),
            Player("CPU2", Trade.BLACKSMITH),
            Player("CPU3", Trade.NAVVY),
            Player("CPU4", Trade.QUARRYMAN),
            Player("CPU5", Trade.MACHINIST)
        ]
        #name, text,            power, heat, independence, order, imports, exports,   fxn, param
        self.card_deck = CardDeck([
        "Stop Train, Everything that goes - stops, 0, 0, 2, 2, 1, 0, PyFxn, PyFxnParam", 
        "Decrease Speed, Whoah Big Fella!, 0, 0, 1, 0, 1, 0, PyFxn, PyFxnParam", 
        "Increase Speed, Increases power production, 2, 2, 1, 0, 1, 0, PyFxn, PyFxnParam", 
        "Heat Shield, Reduces heat damage, 0, 3, 1, 0, 0, 1, PyFxn, PyFxnParam", 
        "Increase Fe Yield, More efficient Iron Extraction from Ilmenite, 2, 0, 0, 1, 0, 1, PyFxn, PyFxnParam", 
        "Sheet-Metal Production, Some like it flat, 1, 1, 1, 1, 0, 1, PyFxn, PyFxnParam", 
        "Steel, The difference between Steel and Iron is a little bit of Carbon and a lot of know how!, 1, 1, 0, 1, 0, 1, PyFxn, PyFxnParam", 
        "Increase Ti Yield, More efficient Titanium Extraction from Ilmenite, 2, 0, 0, 1, 0, 1, PyFxn, PyFxnParam", 
        "Blockade, This is our hill.. these are our beans, 1, 0, 1, 0, 1, 0, PyFxn, PyFxnParam", 
        "Party, Workers Gone Wild,TRADE_PAYOUT_MAP,  0, 0, 0, 2, 1, 1, PyFxn, PyFxnParam", 
        "Bucket Buster, You can't shovel that, 1, 1, 1, 0, 1, 1, PyFxn, PyFxnParam", 
        "Solar Flare, Increases power production, 3, 0, 1, 0, 0, 1, PyFxn, PyFxnParam", 
        "Geothermal Vulcanism, Increases heat production, 3, 0, 1, 0, 0, 1, PyFxn, PyFxnParam", 
        "Rubble, Soil so loose you can pick it up with your bare hands.. well almost, 0, 1, 1, 0, 0, 1, PyFxn, PyFxnParam", 
        "Rocky Road, it's not just ice cream, 1, 0, 1, 0, 1, 0, PyFxn, PyFxnParam", 
        "Boulder, Like a rock but much bigger, 1, 1, 1, 0, 1, 1, PyFxn, PyFxnParam", 
        "Civil Service Day, Usually we aren't very civil, 0, 0, 0, 3, 0, 2, PyFxn, PyFxnParam", 
        "Rail Damage, Railways on Mercury, 0, 1, 0, 1, 0, 1, PyFxn, PyFxnParam"
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

    def has_resources(self, player, card: Card) -> bool:
        return (player.resources.components[power] >=        card.cost.components[power]        and
                player.resources.components[heat] >=         card.cost.components[heat]         and
                player.resources.components[independence] >= card.cost.components[independence] and
                player.resources.components[order] >=        card.cost.components[order]        and
                player.resources.components[imports] >=      card.cost.components[imports]      and
                player.resources.components[exports] >=      card.cost.components[exports]      )

    def calculate_payout(self, player):
        receipt = player.name + "'s Payout" 
        resources_before_payout = copy.deepcopy(player.resources)
        for car in player.train_cars:
            # player's Resources = payout : Resources Resources::__imul__ int
            player.resources += (TRADE_PAYOUT_MAP[car.car_type] * car.proficiency)

        # Display detailed payout information
        print(f"   {resources_before_payout}");
        print(f" + {player.resources - resources_before_payout}");
        print("-----------------------------------------")
        print(f" = {player.resources}")

    def action_phase(self,player):
        """Handle the Action phase for a player."""
        print("Actions available:")
        for index, card in enumerate(player.cards, start=1):
            # Assuming you have a function `has_resources(player, card)` that checks if the player has the necessary resources
            if self.has_resources(player, card):
                print(f"{index}. {card}")
            else:
                print(f"\033[9m{index}. {card}\033[0m")
        print("B. Barter")
        print("P. Pass")

        valid_input = False
        while not valid_input:
            action_input = input("Choose an action (1, 2, ..., B, P)[P]: ").strip().upper()
            if not action_input:
                action_input = "P"
            if action_input.startswith("B"):
                print("Barter selected. Implement barter logic here.")
                valid_input = True
            elif action_input.startswith("P"):
                print(f"{player.name} passes the action phase.")
                valid_input = True
            else:
                self.play_selected_card(player, action_input)

    def play_selected_card(self, player, action_input):
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
        while self.round <= 4:
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
            self.round += 1  

# Run the game
game = Game()
game.run_game()

