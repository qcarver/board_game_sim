import unittest
from cards import Card, CardDeck
from resources import Resources, power, heat, freedom, order, imports, exports

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        cost = Resources({power: 2, heat: 1})
        card = Card("Test Card", "This is a test card.", cost)
        self.assertEqual(card.name, "Test Card")
        self.assertEqual(card.text, "This is a test card.")
        self.assertEqual(card.cost, cost)

class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.csv_file_path = 'card_deck.csv'
        with open(self.csv_file_path, 'w') as file:
            file.write("Name, Text, Power, Heat, Freedom, Order, Imports, Exports\n")
            file.write("Test Card 1, Description 1, 2, 1, 0, 0, 0, 0\n")
            file.write("Test Card 2, Description 2, 0, 0, 1, 1, 1, 1\n")

    def test_card_deck_initialization(self):
        deck = CardDeck(self.csv_file_path)
        self.assertEqual(len(deck.deck), 2)

    def test_draw_card(self):
        deck = CardDeck(self.csv_file_path)
        card = deck.draw_card()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.deck), 1)

if __name__ == '__main__':
    unittest.main()
