"""
@file money.py: this file deals with constructs used like 'money' in the game
@brief It defines the Resources class and ResourceType enum and type shorthand 
@details Resources are a collection of quantities of ResourceTypes. The latter
is a fancy enumeration and can only be used to reference a single instance of
one ResourceType. Some arithmetic operations are overloaded to make it easier
to work with Resources like you might with money. All mathematical operations
are computed element-wise (by contained ResourceTypes) and return a new
Resources object.
@version 0.1
"""
import operator
from enum import Enum

class ResourceType(Enum):
    """
    @brief ResourceType is an enumeration of the different types of resources
    @details It's used to reference an instance of a type of resource. 
    Note ez shorthands are: power, heat, independence, order, imports, exports
    """ 
    POWER = 1
    HEAT = 2
    INDEPENDENCE = 3
    ORDER = 4
    IMPORTS = 5
    EXPORTS = 6

    #Eg: resources = ResourcesType.POWER * 2
    def __mul__(self, quantity):
        return Resources((quantity, self))

    #Eg: rmul just uses mul as its delegate 
    def __rmul__(self, quantity):
        return self.__mul__(quantity)    

# Shorthand references
power = ResourceType.POWER
heat = ResourceType.HEAT
independence = ResourceType.INDEPENDENCE
order = ResourceType.ORDER
imports = ResourceType.IMPORTS
exports = ResourceType.EXPORTS

"""
@brief Resources is a collection of quantities of ResourceTypes 
@details +, -, *, +=,are overloaded to make finances more ituative 
"""
class Resources:
    def __init__(self, *args):
        # Initialize all resource counts to 0
        self.components = {resource: 0 for resource in ResourceType}
        
        # Update the resources with the provided arguments
        for quantity, resource in args:
            if resource in self.components:
                self.components[resource] += quantity

    def __add__(self, other):
        if isinstance(other, Resources):
            new_resources = Resources()
            for resource in ResourceType:
                new_resources.components[resource] = self.components[resource] + other.components[resource]
            return new_resources
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Resources):
            new_resources = Resources()
            for resource in ResourceType:
                new_resources.components[resource] = self.components[resource] - other.components[resource]
            return new_resources
        return NotImplemented

    #Eg: resources = ResourcesType * 2 #doubles the amount of everything in resource
    def __mul__(self, quantity):
        if isinstance(self, Resources) and isinstance(quantity, int):
            new_resources = Resources()
            for resource in ResourceType:
                new_resources.components[resource] = self.components[resource] * quantity
            return new_resources
        return Resources((quantity, self))

    #Eg: rmul just uses mul as its delegate 
    def __rmul__(self, quantity):
        return self.__mul__(quantity)    
    
    def __iadd__(self, other):
        #pdb.set_trace()
        if isinstance(other, Resources):
            for resource in ResourceType:
                self.components[resource] += other.components[resource]
        elif isinstance(other, ResourceType):
            self.components[other] += 1
        else:
            return NotImplemented
        return self

    def compare(self, other, op):
        ops = {
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge
        }
        return all(ops[op](self.components[resource], other.components[resource]) for resource in self.components)

    def __lt__(self, other):
        return self.compare(other, '<')

    def __le__(self, other):
        return self.compare(other, '<=')

    def __eq__(self, other):
        return self.compare(other, '==')

    def __ne__(self, other):
        return self.compare(other, '!=')

    def __gt__(self, other):
        return self.compare(other, '>')

    def __ge__(self, other):
        return self.compare(other, '>=')
    
    def __str__(self):
        # ANSI escape codes for colors
        DARK_YELLOW = "\033[33m"
        DARK_ORANGE = "\033[38;5;208m"
        DARK_PINK = "\033[38;5;197m"
        CORPORATE_BLUE = "\033[34m"
        FORREST_GREEN = "\033[32m"
        MEDIUM_DARK_GRAY = "\033[38;5;240m"
        RESET = "\033[0m"

        return (
            f"{DARK_YELLOW}Power: {self.components[ResourceType.POWER]:>4}{RESET}, "
            f"{DARK_ORANGE}Heat: {self.components[ResourceType.HEAT]:>4}{RESET}, "
            f"{DARK_PINK}Independence: {self.components[ResourceType.INDEPENDENCE]:>4}{RESET}, "
            f"{CORPORATE_BLUE}Order: {self.components[ResourceType.ORDER]:>4}{RESET}, "
            f"{FORREST_GREEN}Imports: {self.components[ResourceType.IMPORTS]:>4}{RESET}, "
            f"{MEDIUM_DARK_GRAY}Exports: {self.components[ResourceType.EXPORTS]:>4}{RESET}"
        )
