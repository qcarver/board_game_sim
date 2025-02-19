"""
@bref: This file contains the game logic for the game. It's the 'main'
@details: it also has functions which deal with more than one class
@author: qcarver@gmail.com
@license: this is a WIP, it is private, not for distribution
"""
import copy
#import pdb #pdb.set_trace() # to pause for debugging
from player import Player, Trade, TRADE_PAYOUT_MAP
from train import CarType, Car
from cards import Card, CardDeck
from resources import Resources, power, heat, freedom, order, imports, exports

# Game.py
import copy
from ui import GameUI  # Import our UI abstraction
from player import Player, Trade, TRADE_PAYOUT_MAP
from train import CarType, Car 
from cards import Card, CardDeck 
from resources import Resources, power, heat, freedom, order, imports, exports
from transaction import Transaction

players =  []

class Game:
    def __init__(self, ui: GameUI):
        self.ui = ui  # Injected UI dependency
        self.round = 1  # Initialize game round
        
        self.players =  [
            Player("CPU1", Trade.SMELTER),
            Player("CPU2", Trade.BLACKSMITH),
            Player("CPU3", Trade.NAVVY),
            Player("CPU4", Trade.QUARRYMAN),
            Player("CPU5", Trade.MACHINIST)
        ]
        # Initialize card deck using CSV-style card data
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
    
    def draw_card(self, player):
        response = self.ui.prompt_input(f"{player.name} (draw card)? [Y]: ") or "Y"
        if response.lower() == 'q':
            self.ui.display_message("Game terminated by user.")
            exit()
        if response.upper() == "Y":
            card = self.card_deck.draw_card()
            if card:
                player.cards.append(card)
                self.ui.display_message(f"{player.name} drew {card}.")
            else:
                self.ui.display_message("The deck is empty!")
        else:
            self.ui.display_message(f"{player.name} didn't draw a card.")

    def calculate_payout(self, player):
        resources_before_payout = copy.deepcopy(player.resources)
        for car in player.train_cars:
            player.resources += (TRADE_PAYOUT_MAP[car.car_type] * car.proficiency)

        self.ui.display_message(f"   {resources_before_payout}")
        self.ui.display_message(f" + {player.resources - resources_before_payout}")
        self.ui.display_message("-----------------------------------------")
        self.ui.display_message(f" = {player.resources}")

    def transact(self, player):
        success = False
        transaction = self.ui.prompt_transaction_input()
        if transaction:
            transaction.accept()
            self.ui.display_message("Transaction successful.")
            success = True
        else:
            self.ui.display_message("Transaction failed.")
        return success

    def action_phase(self, player):
        self.ui.display_message("Actions available:")
        for index, card in enumerate(player.cards, start=1):
            if card.cost <= player.resources:
                self.ui.display_message(f"{index}. {card}")
            else:
                # For simplicity, we show the same message; you can customize this styling if needed.
                self.ui.display_message(f"{index}. {card} [Cannot afford]")
        self.ui.display_message("T. Transact")
        self.ui.display_message("P. Pass")

        valid_input = False
        while not valid_input:
            action_input = self.ui.prompt_input("Choose an action (1, 2, ..., T, P)[P]: ").strip().upper()
            if not action_input:
                action_input = "P"
            if action_input.startswith("T"):
                transaction_successful = self.transact(player)
                valid_input = transaction_successful
            elif action_input.startswith("P"):
                self.ui.display_message(f"{player.name} passes the action phase.")
                valid_input = True
            elif action_input == "q":
                self.ui.display_message("Game terminated by user.")
                exit()
            else:
                self.play_selected_card(player, action_input)

    def play_selected_card(self, player, action_input):
        try:
            card_index = int(action_input) - 1
            if 0 <= card_index < len(player.cards):
                selected_card = player.cards[card_index]
                if selected_card.cost <= player.resources:
                    self.ui.display_message(f"Playing card: {selected_card}")
                    # Implement card action logic here
                else:
                    self.ui.display_message("Not enough resources to play card")
            else:
                self.ui.display_message("Invalid card selection.")
        except ValueError:
            self.ui.display_message("Invalid input. Please choose a valid action.")

    def run_game(self):
        while self.round <= 4:
            for player in self.players:
                self.ui.display_message(f"--- Round {self.round} ---")
                if self.round == 1: 
                    new_name = self.ui.prompt_input(f"What is {player.trade.name}'s name? [{player.name}]: ")
                    if new_name:
                        player.name = new_name
                for phase in ["Draw", "Payout", "Action"]:
                    if phase == "Draw":
                        self.draw_card(player)
                    elif phase == "Payout":
                        self.calculate_payout(player)
                    elif phase == "Action":
                        self.action_phase(player)
            self.round += 1  
            self.ui.display_game_board()  # Use default value of 36 boxes

