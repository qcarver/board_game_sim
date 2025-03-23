import re
from abc import ABC, abstractmethod
from wcwidth import wcswidth
from transaction import Transaction
from player import Player
from resources import Resources, ResourceType

class GameUI(ABC):
    @abstractmethod
    def display_message(self, message: str) -> None:
        """Display a message to the user."""
        pass

    @abstractmethod
    def prompt_input(self, prompt: str) -> str:
        """Prompt the user for input and return the response."""
        pass

    @abstractmethod
    def print_two_columns(self, left: str, right: str, column_width: int = 40) -> None:
        """
        Print two columns of text side by side.
        
        Args:
            left (str): Text for the left column.
            right (str): Text for the right column.
            column_width (int): Width of each column. Default is 40.
        """
        pass

    @abstractmethod
    def prompt_transaction_input(self) -> Transaction:
        """
        Prompt the user with the current state of the offering and receiving players.
        
        Args:
            offering_details (TransactionDetails): The details of the offering player.
            receiving_details (TransactionDetails): The details of the receiving player.
        """
        pass

    @abstractmethod
    def display_game_board(self, num_boxes: int = 36) -> None:
        """
        Display an ASCII box layout based on the specified number of boxes.
        
        Args:
            num_boxes (int): The number of boxes to render.
        """
        pass

# --- Example of a concrete Console UI implementation ---

class ConsoleUI(GameUI):
    def display_message(self, message: str) -> None:
        print(message)

    def prompt_input(self, prompt: str) -> str:
        return input(prompt)

    def print_two_columns(self, left: str, right: str, column_width: int = 40) -> None:
        # Split the input strings into lines
        left_lines = left.splitlines()
        right_lines = right.splitlines()
        max_rows = max(len(left_lines), len(right_lines))
        
        # Pad the shorter list with empty strings
        left_lines += [""] * (max_rows - len(left_lines))
        right_lines += [""] * (max_rows - len(right_lines))
        
        # Function to strip ANSI escape codes
        def strip_ansi_codes(text):
            ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', text)
        
        # Print each pair of lines, left-justified within the specified width
        for left_line, right_line in zip(left_lines, right_lines):
            stripped_left_line = strip_ansi_codes(left_line)
            left_printable_width = wcswidth(stripped_left_line)
            left_padding = column_width - left_printable_width
            print(f"{left_line}{' ' * left_padding}{right_line}")

    def prompt_transaction_input(self) -> Transaction:
        """
        Prompt the user with the current state of the offering and receiving players.
        """
        user_input = self._get_valid_transaction_input()
        offering_selection, receiving_selection = self._split_transaction_input(user_input)
        offering_bid = self._create_bid_from_selection(offering_selection)
        receiving_bid = self._create_bid_from_selection(receiving_selection)
        return Transaction(offering_bid, receiving_bid)

    def _get_valid_transaction_input(self) -> str:
        """
        Prompt the user for a valid transaction input and validate it against the pattern.
        """
        pattern = re.compile(r'^[0-5]:((\d+|[HPFOIE]\d+)(\+(\d+|[HPFOIE]\d+))*)?>[0-5]:((\d+|[HPFOIE]\d+)(\+(\d+|[HPFOIE]\d+))*)?$')
        while True:
            user_input = input("Enter your transaction (Eg: *your_id#*:1+H1+P2>*others_id#*:F1+I1): ")
            if pattern.match(user_input):
                return user_input
            else:
                print("Invalid input format. Try something like (player:card#+resource-quantity...>...): ")

    def _split_transaction_input(self, user_input: str) -> tuple:
        """
        Split the transaction input into offering and receiving selections.
        """
        offering_selection, receiving_selection = user_input.split('>')
        return offering_selection, receiving_selection

    def _create_bid_from_selection(self, selection: str) -> Transaction.Bid:
        """
        Create a Transaction.Bid object from a selection string.
        """
        player_id, items = selection.split(':')
        player = Player.get_player_by_id(int(player_id))
        bid = Transaction.Bid(player, Resources(), [])

        for item in items.split('+'):
            if item.isdigit():
                # Handle card offering
                card_index = int(item) - 1
                if 0 <= card_index < len(player.cards):
                    bid.cards.append(player.cards[card_index])
            else:
                # Handle resource offering
                resource_type = ResourceType.with_initial(item[0])
                quantity = int(item[1:])
                bid.resources += resource_type * quantity

        return bid

    def display_game_board(self, num_boxes: int = 36) -> None:
        if num_boxes < 1:
            return

        top_row = "┌"
        middle_rows = ["│" for _ in range(5)]
        bottom_row = "└"

        for i in range(num_boxes):
            if (i + 1) % 12 == 0:
                top_row += "▄▄┬" if i < num_boxes - 1 else "▄▄┐"
                for j in range(5):
                    middle_rows[j] += "  │"
                bottom_row += "▀▀┴" if i < num_boxes - 1 else "▀▀┘"
            else:
                top_row += "──┬" if i < num_boxes - 1 else "──┐"
                for j in range(5):
                    middle_rows[j] += "  │"
                bottom_row += "──┴" if i < num_boxes - 1 else "──┘"

        print(top_row)
        for row in middle_rows:
            print(row)
        print(bottom_row)
