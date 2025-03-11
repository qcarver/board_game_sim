"""
@file Transaction.py
@brief This file defines the Transaction class for handling resource transactions between players.
@details The Transaction class manages the exchange of resources and cards between players.
@version 0.1
"""

from resources import Resources
from player import Player
import pdb #pdb.set_trace() # to pause for debugging

class Transaction:
    """
    @class Transaction
    @brief Manages resource transactions between players.
    @details This class handles the exchange of resources and cards between players.
    """

    class Bid:
        """
        @class Bid
        @brief Contains the details of a bid from a player.
        @details This class holds the player, resources, and cards being offered or received.
        """
        def __init__(self, player: Player, resources: Resources, cards: list):
            """
            @brief Initialize the Bid with the player, resources, and cards.
            @param player The player making the bid.
            @param resources The resources included in the bid.
            @param cards The cards included in the bid.
            """
            self.player = player
            self.resources = resources
            self.cards = cards

    def __init__(self, offering_bid: 'Transaction.Bid', receiving_bid: 'Transaction.Bid'):
        """
        @brief Initialize the Transaction with the offering and receiving bids.
        @param offering_bid The bid from the offering player.
        @param receiving_bid The bid from the receiving player.
        """
        self.offering_bid = offering_bid
        self.receiving_bid = receiving_bid

    def accept(self):
        """
        @brief Accept the transaction and transfer resources and cards.
        """
        # Transfer resources from offering player to receiving player
        for resource_type, quantity in self.offering_bid.resources.components.items():
            self.receiving_bid.player.resources.components[resource_type] += quantity
            self.offering_bid.player.resources.components[resource_type] -= quantity

        # Transfer cards from offering player to receiving player
        for card in self.offering_bid.cards:
            self.receiving_bid.player.cards.append(card)
            self.offering_bid.player.cards.remove(card)

        # Transfer resources from receiving player to offering player
        for resource_type, quantity in self.receiving_bid.resources.components.items():
            self.offering_bid.player.resources.components[resource_type] += quantity
            self.receiving_bid.player.resources.components[resource_type] -= quantity

        # Transfer cards from receiving player to offering player
        for card in self.receiving_bid.cards:
            self.offering_bid.player.cards.append(card)
            self.receiving_bid.player.cards.remove(card)

        print(f"Transaction completed between {self.offering_bid.player.name} and {self.receiving_bid.player.name}.")