"""
@file cards.py: this file deals with constructs used like 'cards' in the game
@brief It defines the Card and CardDeck classes
"""

import random
from .money import Resources, power, heat, independence, order, imports, exports

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
            resource_gauge += f"{resource.markup()}{gauge_string}"
    
        return f"{self.name}: {resource_gauge.strip()}"
    
    #def __str__(self):
    #    return ", ".join(
    #        f"{resource.markup()}{resource.name.lower().capitalize()}: {self.components[resource]:>4}{RESET}"
    #        for resource in ResourceType
    #    )

class CardDeck:
    def __init__(self, card_data: list[str]):
        """Initialize the CardDeck with card data from a CSV array."""
        self.deck = []
        for line in card_data:
            parts = line.split(', ')
            name = parts[0]
            text = parts[1]
            cost = (power * int(parts[2]) + heat * int(parts[3]) + 
                   independence * int(parts[4]) + order * int(parts[5]) + 
                   imports * int(parts[6]) + exports * int(parts[7]))
            self.deck.append(Card(name, text, cost))
        random.shuffle(self.deck)

    def draw_card(self) -> Card:
        return self.deck.pop() if self.deck else None


