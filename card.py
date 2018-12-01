"""
This file handels the Classes Deck, Player, Table, and Bot.
"""

from random import randint  # Used for shuffling and popping off random cards
import bot


class Deck:
    """
    Deck Class:
    This class handels a deck of cards and ensures it holds all of a deck's
    properties. The deck will resemble an actual deck of playing cards.
    """

    def __init__(self):
        """
        Creates a deck of cards.

        Input: self - the object on which this meathod is done on

        Output: None

        Runtime: O(n*m) where n is the number of the card(2,3,...,ace) and m is
        the different suits (Hearts,...)
        """
        self._cards = []
        for i in range(13):
            for name in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
                self._cards.append((i + 2, name))

    def print_cards(self):
        """
        Prints out a deck of cards.

        Input: self - the object on which this meathod is done on

        Output: None

        Runtime: O(1)
        """
        print('Length of deck: ', len(self._cards))
        print('Cards in deck: ', self._cards)

    def get_cards(self):
        """
        Recieves all the cards in a deck.

        Input: self - the object on which this meathod is done on

        Output: A list of all the cards the deck contains.

        Runtime: O(1)
        """
        return self._cards

    def shuffle(self):
        """
        Shuffles all the cards in a deck.

        Input: self - the object on which this meathod is done on

        Output: None.

        Runtime: O(n) where n is the total number of cards in the deck
        """
        new_cards = []
        size = len(self._cards)
        for i in range(size - 1, -1, -1):
            new_cards.append(self._cards.pop(randint(0, i)))
        self._cards = new_cards

    def remove_random_card(self):
        """
        Pops off a random card in the deck.

        Input: self - the object on which this meathod is done on

        Output: the card that is removed.

        Runtime: O(n) where n is the number of cards in the deck
        """
        if len(self._cards) == 0:
            print('Deck is empty')
            return
        index = randint(0, len(self._cards) - 1)
        random_card = self._cards[index]
        self._cards.remove(random_card)  # O(n)
        return random_card

    def remove_top_card(self):
        """
        Pops off the top card in the deck.

        Input: self - the object on which this meathod is done on

        Output: the card that is removed.

        Runtime: O(1)
        """
        if len(self._cards) == 0:
            print('Deck is empty')
            return
        return self._cards.pop(0)

    def remove_card(self, current):
        """
        Pops off a specified card in the deck.

        Input: self - the object on which this meathod is done on

        Output: the card that is removed.

        Runtime: O(n) where n is the number of cards the deck has
        """
        if len(self._cards) == 0:
            print('Deck is empty')
            return
        return self._cards.remove(current)  # O(n)

    def deal(self, players, cards_per_player):
        """
        Given a list of all the player objects the deck deals a specified number
        of cards to each player

        Inputs:
        self - the object on which this meathod is done on
        players - a list of all the player objects that we will deal cards to
        cards_per_player - the number of cards to be dealt to each player

        Output: None.

        Runtime: O(n*m*x) where n is the cards_per_player and m is the number of
        players and x is the number of cards in the deck
        """
        assert cards_per_player * len(players) <= len(self._cards)
        for i in range(cards_per_player):
            for p in players:
                card = self.remove_top_card()  # O(x)
                p.add_card(card)

    def collect(self, players):
        """
        Collects all the cards from the players and puts them back in the deck

        Input:
        self - the object on which this meathod is done on
        players - a list of all the player objects that we will collect the cards
        from

        Output: None.

        Runtime: O(n*m) where n is the number of cards each player has and m is
        the number of players
        """
        for p in players:
            while len(p.get_cards()) > 0:
                self._cards.append(p.pop_card())

    def have_all_cards(self):
        """
        Determines if all the cards are in the deck.

        Input: self - the object on which this meathod is done on

        Output: whether or not the deck of cards contains evrey card.

        Runtime: O(n) where n is the number of cards in the deck
        """
        cards = set()
        for c in self._cards:
            cards.add(c)
        if len(cards) == 52:
            return True
        else:
            return False

    def push_to_table(self, table, number_of_cards):
        """
        Pushes a specified number of cards to the table

        Input:
        self - the object on which this meathod is done on
        table - the table object which we will be pushing cards too
        number_of_cards - the number of cards to be pushed to the table

        Output: None.

        Runtime: O(n*m) where n is the number of cards we would like to push to
        the table and m is the number of cards in the deck
        """
        for i in range(number_of_cards):
            table.add_card(self.remove_top_card())  # O(m)

    def __str__(self):
        """
        Used to print the Deck

        Input: self - the object on which this meathod is done on

        Output: A string of what to print

        Runtime: O(1)
        """
        return 'Deck of cards'


class Player:
    """
    Player Class:
    This class handels a Player object that has cards, chips,
    and ID to identify it. The Player class acts as a base for both the Bot and
    Table classes
    """

    def __init__(self, ID, cards=None):
        """
        Creates a Player object and initializes its ID and if given a list of
        cards it will give those cards to the player object and gives the player
        2000 chips.

        Input:
        self - the object on which this meathod is done on
        ID - The identification of the player
        cards=None - The cards that the player starts out with, initialized to
        the empty list.

        Output: None

        Runtime: O(1)
        """
        if cards == None:
            self._cards = []
        else:
            self._cards = cards
        self._ID = ID

        self._hand = -1

        # Total starting chips is 2000
        self._chips = 2000

    def get_hand(self):
        """
        Recieves the hand (Royal Flush(10),...,Two Pair(2), One Pair(1)) the player has.

        Input: self - the object on which this meathod is done on

        Output: The hand the player has.

        Runtime: O(1)
        """
        return self._hand

    def set_hand(self, hand):
        """
        Sets the hand (Royal Flush(10),...,Two Pair(2), One Pair(1)) the player has.

        Input:
        self - the object on which this meathod is done on.
        hand - the hand we will set the players hand at.

        Output: None.

        Runtime: O(1)
        """
        self._hand = hand

    def get_ID(self):
        """
        Recieves the ID the player has.

        Input: self - the object on which this meathod is done on

        Output: The ID of the player.

        Runtime: O(1)
        """
        return self._ID

    def get_cards(self):
        """
        Recieves all the cards the player has.

        Input: self - the object on which this meathod is done on

        Output: A list of all the cards the player has.

        Runtime: O(1)
        """
        return self._cards

    def print_cards(self):
        """
        Prints all the cards the player has.

        Input: self - the object on which this meathod is done on

        Output: None.

        Runtime: O(1)
        """
        print(self, '\b:\t', end='')
        print('Cards : {}\n'.format(self._cards))

    def add_card(self, card):
        """
        Gives a card to the player.

        Input:
        self - the object on which this meathod is done on
        card - the card to be added

        Output: None

        Runtime: O(1)
        """
        self._cards.append(card)

    def remove_card(self, card):
        """
        Removes a card from the player.

        Input:
        self - the object on which this meathod is done on
        card - the card to be removed

        Output: None

        Runtime: O(n) where n is the number of cards the player has
        """
        if card not in self._cards:
            print('you dont have that card')
        self._cards.remove(card)  # O(n)

    def pop_card(self):
        """
        Pops a card from the player.

        Input:
        self - the object on which this meathod is done on

        Output: The card Popped off

        Runtime: O(1)
        """
        try:
            return self._cards.pop(0)
        except:
            print('No cards left')

    def __str__(self):
        """
        Used to print the Player

        Input: self - the object on which this meathod is done on

        Output: A string of what to print

        Runtime: O(1)
        """
        return 'Player'

    def get_chips(self):
        """
        Get the number of chips the player has

        Input: self - the object on which this meathod is done on

        Output: The number of chips the player has

        Runtime: O(1)
        """
        return self._chips

    def remove_chips(self, value):
        """
        Remove a certain number of chips from the player

        Input: self - the object on which this meathod is done on
        value - the number of chips to be removed

        Output: None

        Runtime: O(1)
        """
        self._chips -= value

    def add_chips(self, value):
        """
        Add a certain number of chips to the player

        Input: self - the object on which this meathod is done on
        value - the number of chips to be added

        Output: None

        Runtime: O(1)
        """
        self._chips += value


class Table(Player):
    """
    Table Class:
    This class is the child of the Player class and holds all the same properties
    """

    def __init__(self, cards=None):
        """
        Creates a Table object and initializes it by calling the initilization
        of the Player class. Then we assign its chips to be 0

        Input:
        self - the object on which this meathod is done on
        cards=None - The cards that the table starts out with, initialized to
        the empty list.

        Output: None

        Runtime: O(1)
        """
        super().__init__('t', cards)  # O(1)
        self._chips = 0

    def __str__(self):
        """
        Used to print the Table

        Input: self - the object on which this meathod is done on

        Output: A string of what to print

        Runtime: O(1)
        """
        return 'Table'

    def give_pot(self, player):
        """
        Gives a player all the Tables chips

        Input:
        self - the object on which this meathod is done on
        player - a player to whom the chips will be given to

        Output: None

        Runtime: O(1)
        """
        player.add_chips(self._chips)
        self.remove_chips(self._chips)


class Bot(Player):
    """
    Bot Class:
    This class is the child of the Player class and holds all the same properties
    """

    def __init__(self, cards=None):
        """
        Creates a Bot object and initializes it by calling the initilization
        of the Player class.

        Input:
        self - the object on which this method is done on
        cards=None - The cards that the table starts out with, initialized to
        the empty list.

        Output: None

        Runtime: O(1)
        """
        super().__init__('b', cards)

    def __str__(self):
        """
        Used to print the Bot

        Input: self - the object on which this meathod is done on

        Output: A string of what to print

        Runtime: O(1)
        """
        return 'Bot'

    def bet(self, current_call, table, can_raise=True):
        return bot.bot_bet(current_call, self, table, can_raise)
