from abc import ABC, abstractmethod

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
            column_width (int): The width allocated for each column.
        """
        pass

    @abstractmethod
    def display_ascii_boxes(self, num_boxes: int = 36) -> None:
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
        
        # Print each pair of lines, left-justified within the specified width
        for left_line, right_line in zip(left_lines, right_lines):
            print(f"{left_line.ljust(column_width)}{right_line.ljust(column_width)}")

    def display_ascii_boxes(self, num_boxes: int = 36) -> None:
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

# --- Usage Example ---
if __name__ == '__main__':
    ui = ConsoleUI()
    ui.display_message("Welcome to the game!")
    response = ui.prompt_input("Enter your name: ")
    ui.display_message(f"Hello, {response}!")
    
    # Print two columns
    left_text = "Player State:\n- Health: 100\n- Resources: 50"
    right_text = "Opponent State:\n- Health: 80\n- Resources: 60"
    ui.print_two_columns(left_text, right_text, column_width=30)
    
    # Display an ASCII box layout
    ui.display_ascii_boxes(24)

