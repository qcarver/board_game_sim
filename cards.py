"""
@file cards.py: this file deals with constructs used like 'cards' in the game
@brief It defines the Card and CardDeck classes
"""

import random
from resources import Resources, power, heat, freedom, order, imports, exports

class Card:

    def __init__(self, name, text, cost: Resources):
        self.name = name  # Name of the card
        self.text = text  # Description of the card's effect
        self.cost = cost # Dictionary of resource and quantity (e.g., {Resource.POWER: 2, Resource.HEAT: 1}) (e.g., [[Resource.POWER, 2], [Resource.HEAT, 1]])

    def __str__(self):
        resource_gauge = ""
        for resource, amount in self.cost.components.items():
            # Define the characters for the gauge
            gauge_chars = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
            
            # Calculate the number of full blocks and the remainder
            full_blocks = amount // 8
            remainder = amount % 8
            
            # Build the gauge string for this resource
            gauge_string = '█' * full_blocks
            if remainder > 0:
                gauge_string += gauge_chars[remainder - 1]
            
            # Concatenate the gauge with the resource color
            resource_gauge += f"{resource.markup()}{gauge_string}\033[0m"
    
        return f"{self.name}: {resource_gauge} "
    
    #def __str__(self):
    #    return ", ".join(
    #        f"{resource.markup()}{resource.name.lower().capitalize()}: {self.components[resource]:>4}{RESET}"
    #        for resource in ResourceType
    #    )

class CardDeck:
    def __init__(self, csv_file_path: str):
        """Initialize the CardDeck with card data from a CSV file."""
        self.deck = []
        with open(csv_file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                parts = line.strip().split(', ')
                try:
                    # The header line won't have integers on it, skip.
                    for part in parts[2:8]:
                        int(part)
                except ValueError:
                    # Skip the line if any of the parameters are not integers
                    continue
                try:
                    name = parts[0]
                    text = parts[1]
                    cost = (power * int(parts[2]) + heat * int(parts[3]) + 
                           freedom * int(parts[4]) + order * int(parts[5]) + 
                           imports * int(parts[6]) + exports * int(parts[7]))
                    self.deck.append(Card(name, text, cost))
                except IndexError:
                    # it's not the header line and it doesn't fit the data pattern
                    print(f"Error processing line {line_number}: {line.strip()}")
                    raise
        random.shuffle(self.deck)

    def draw_card(self) -> Card:
        return self.deck.pop() if self.deck else None
    
def play_card(card: Card, game_state) -> bool:
    """
    @brief This function plays the card selected by the player
    @param card: The card to be played
    @param game_state: The current state of the game
    @return: A boolean value to indicate if the card was played successfully
    """
    # Check if the player has enough resources to play the card
    if not game_state.has_enough_resources(card.cost):
        return False
    
    # Apply the card's effect to the game state
    card.apply_effect(game_state)
    
    # Deduct the resources used to play the card from the player's resources
    game_state.deduct_resources(card.cost)
    
    return True



