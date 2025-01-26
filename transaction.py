"""
@file Transaction.py
@brief This file defines the Transaction class for handling resource transactions between players.
@details The Transaction class manages the exchange of resources and cards between players.
@version 0.1
"""

from .resources import ResourceType, Resources
from .player import Player
import re
import pdb #pdb.set_trace() # to pause for debugging


class Transaction:
    """
    @class Transaction
    @brief Manages resource transactions between players.
    @details This class handles the exchange of resources and cards between players.
    """

    class TransactionDetails:
        """
        @class TransactionDetails
        @brief Contains the details of a player's transaction.
        @details This class holds the resources and cards being offered or received by a player.
        """
        def __init__(self, player: Player):
            """
            @brief Initialize the TransactionDetails with the player.
            @param player The player involved in the transaction.
            """
            self.player = player
            self.resources = Resources()
            self.cards = []

        def offer_resources(self, resource_type, quantity):
            """
            @brief Offer resources for the transaction.
            @param resource_type The type of resource being offered.
            @param quantity The quantity of the resource being offered.
            """
            if self.player.resources.components[resource_type] >= quantity:
                self.resources.components[resource_type] += quantity
                self.player.resources.components[resource_type] -= quantity
            else:
                print(f"Not enough {resource_type.name} to offer.")

        def offer_card(self, card):
            """
            @brief Offer a card for the transaction.
            @param card The card being offered.
            """
            if card in self.player.cards:
                self.cards.append(card)
                self.player.cards.remove(card)
            else:
                print(f"{self.player.name} does not have the card {card.name}.")

    def __init__(self, offering_player: Player, receiving_player: Player):
        """
        @brief Initialize the Transaction with the offering and receiving players.
        @param offering_player The player offering resources or cards.
        @param receiving_player The player receiving resources or cards.
        """
        self.offering_details = self.TransactionDetails(offering_player)
        self.receiving_details = self.TransactionDetails(receiving_player)

    def accept(self):
        """
        @brief Accept the transaction and transfer resources and cards.
        """
        for resource_type, quantity in self.offering_details.resources.components.items():
            self.receiving_details.player.resources.components[resource_type] += quantity

        for card in self.offering_details.cards:
            self.receiving_details.player.cards.append(card)

        for resource_type, quantity in self.receiving_details.resources.components.items():
            self.offering_details.player.resources.components[resource_type] += quantity

        for card in self.receiving_details.cards:
            self.offering_details.player.cards.append(card)

        offerred_items = []

        for resource_type, quantity in self.offering_details.resources.components.items():
            if quantity > 0:
                offerred_items.append(f"{quantity} {resource_type.name}")

        for card in self.offering_details.cards:
            offerred_items.append(f"card {card.name}")

        offerred_items_str = ", ".join(offerred_items)

        received_items = []

        for resource_type, quantity in self.receiving_details.resources.components.items():
            if quantity > 0:
                received_items.append(f"{quantity} {resource_type.name}")

        for card in self.receiving_details.cards:
            received_items.append(f"card {card.name}")

        received_items_str = ", ".join(received_items)

        print(f"Transaction between {self.offering_details.player.name} for {offerred_items_str} "
              f"and {self.receiving_details.player.name} for {received_items_str} completed.")

    def cancel(self):
        """
        @brief Cancel the transaction and return resources and cards to the offering player.
        """
        for resource_type, quantity in self.offering_details.resources.components.items():
            self.offering_details.player.resources.components[resource_type] += quantity

        for card in self.offering_details.cards:
            self.offering_details.player.cards.append(card)

        for resource_type, quantity in self.receiving_details.resources.components.items():
            self.receiving_details.player.resources.components[resource_type] += quantity

        for card in self.receiving_details.cards:
            self.receiving_details.player.cards.append(card)

        print(f"Transaction canceled between {self.offering_details.player.name} and {self.receiving_details.player.name}.")

class TransactionUI:
    """
    @class TransactionUI
    @brief Manages the user interface for transactions.
    @details This class handles the console-based user interface for transactions between players.
    """
    def __init__(self, offering_player, receiving_player):
        """
        @brief Initialize the TransactionUI with the names of the offering and receiving players.
        @param offering_player The object representing the player initiating the transaction. 
        @param receiving_player_name The object representing the player who is the transactant. 
        """
        self.offering_player = offering_player
        self.receiving_player = receiving_player
        self.transaction = Transaction(offering_player, receiving_player)



    def print_two_columns(self, left_column, right_column, column_width: int = 40):
        """
        Prints two columns of data side by side, left-justified.
        
        Args:
            left_column (list): List of strings for the left column.
            right_column (list): List of strings for the right column.
            column_width (int): Width allocated to each column.
        """
        # Determine the maximum number of rows
        left_rows = left_column.count("\n") + 1
        right_rows = right_column.count("\n") + 1   
        max_rows = max(left_rows, right_rows)
        
        # Pad shorter column with empty strings
        left_column = left_column + "\n" * (max_rows - left_rows)
        right_column = right_column + "\n" *  (max_rows - right_rows)
        
        # Print each row with left-justified columns
        left_lines = left_column.split('\n')
        right_lines = right_column.split('\n')
        for left, right in zip(left_lines, right_lines):
            print(f"{left.ljust(column_width)}{right.ljust(column_width)}")

    def prompt(self):
        """
        @brief Prompt the user with the current state of the offering and receiving players.
        """
        self.print_two_columns(self.offering_player.__str__(), self.receiving_player.__str__()) 

        pattern = re.compile(r'^[0-5]:((\d+|[HEFOI]\d+)(\+(\d+|[HEFOI]\d+))*)?>[0-5]:((\d+|[HEFOI]\d+)(\+(\d+|[HEFOI]\d+))*)?$')
        
        while True:
            user_input = input("Enter your transaction (Eg: {offering_player.id}:1+H1+P2>{receiving_player.id}:F1+I1)")
            if pattern.match(user_input):
                break
            else:
                print(f"Invalid input format. Try something like (player:card#+resource-quantity...>...): ")

        offering_selection, receiving_selection = user_input.split('>')
        offering_player_index, offering_items = offering_selection.split(':')
        receiving_player_index, receiving_items = receiving_selection.split(':')
        
        #print(f"Offering player selected index: {offering_player_index} with items: {offering_items}")
        #print(f"Receiving player selected index: {receiving_player_index} with items: {receiving_items}")

        # Process offering items
        for item in offering_items.split('+'):
            if item.isdigit():
                # Handle card offering
                card_index = int(item) - 1
                if 0 <= card_index < len(self.offering_player.cards):
                    self.transaction.offering_details.offer_card(self.offering_player.cards[card_index])
            else:
                # Handle resource offering
                resource_type = ResourceType.with_initial(item[0])
                quantity = int(item[1:])
                self.transaction.offering_details.offer_resources(resource_type, quantity)
        
        # Process receiving items
        for item in receiving_items.split('+'):
            if item.isdigit():
                # Handle card offering
                card_index = int(item) - 1
                if 0 <= card_index < len(self.receiving_player.cards):
                    self.transaction.receiving_details.offer_card(self.receiving_player.cards[card_index])
            else:
                # Handle resource offering
                resource_type = ResourceType[item[0]]
                quantity = int(item[1:])
                self.transaction.receiving_details.offer_resources(resource_type, quantity)
        
        # Accept the transaction
        self.transaction.accept()
        return True