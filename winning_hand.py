"""
This file handels which player is the winner given an arbritary amount of players.
It does this by dtermining which player has the best hand, on ties it depends on who
has the highest card
"""


def printable_dict_of_winners(table, players):
    """
    Used to print out all the nessecary values for testing purposes.

    Inputs:
    table - an object of the Table class
    players - a list of all the players

    Output: None

    Runtime: O(p*xlog(x)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table and p is the number of players
    """

    value_to_meaning={
        10:'Royal Flush', 9: 'Straight Flush',
        8: 'Four of a kind', 7: 'Full house', 6: 'Flush', 5: 'Straight', 4: 'Three of a kind',
        3: 'Two Pair', 2: 'One pair', 1: 'Nothing'}

    pvalues = dict()
    for p in players:  # O(p)
        get_value(table, p)  # O(xlog(x))
        pvalues[p.get_ID()] = value_to_meaning[p.get_hand()]
    print(pvalues)


def winner(table, players, printing=True):
    """
    Determines the winner of the round.

    Inputs:
    table - an object of the Table class
    players - a list of all the players
    printing==True: - whether or not to print to the command terminal (used for testing)

    Output: The winner

    Runtime: O(p*xlog(x) + plog(p)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table and p is the number of players
    """
    values = dict()
    for p in players:  # O(p)
        get_value(table, p)  # O(xlog(x))
        values[p] = p.get_hand()
    if printing:
        printable_dict_of_winners(table, players)  # O(p*xlog(x))

    sorted_players = sorted(
        values.items(), key=lambda k: k[1], reverse=True)  # O(p*log(p))
    highest_score = sorted_players[0][1]
    winners = []

    for i in values.keys():  # O(p)
        if values[i] == highest_score:
            winners.append(i)

    if len(winners) > 1:
        winner = highest_card(winners)  # O(n)
        return winner[0]
    else:
        return winners[0]


def get_value(table, player):
    """
    Determine the value of the hand that a player has and stores it in the Player object

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: None

    Runtime: O(xlog(x)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    if has_royal_flush(table, player):  # O(n+m)
        player.set_hand(10)
    elif has_straight_flush(table, player):  # O(xlog(x))
        player.set_hand(9)
    elif has_four_of_a_kind(table, player):  # O(n+m)
        player.set_hand(8)
    elif has_full_house(table, player):  # O(n+m)
        player.set_hand(7)
    elif has_flush(table, player):  # O(n+m)
        player.set_hand(6)
    elif has_straight(table, player):  # O(xlog(x))
        player.set_hand(5)
    elif has_three_of_a_kind(table, player):  # O(n+m)
        player.set_hand(4)
    elif has_two_pair(table, player):  # O(n+m)
        player.set_hand(3)
    elif has_one_pair(table, player):  # O(n+m)
        player.set_hand(2)
    else:
        player.set_hand(1)


def has_royal_flush(table, player):
    """
    If the player has a flush over the interval [10,jack,queen,king,ace] it is considered
    a royal flush

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is a royal flush, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    return if_straight_is_flush([10, 11, 12, 13, 14], table, player)  #O(n+m)


def if_straight_is_flush(l, table, player):
    """
    If the player has a straight over an interval l this function determines if
    l contains a flush

    Inputs:
    table - an object of the Table class
    player - an object of the Player class
    l - a list that contains a straight

    Output: True if there is a straight flush, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    Hearts = 0
    Diamonds = 0
    Spades = 0
    Clubs = 0

    if 1 in l: # ace low flush
        l.append(14) 

    for c in table.get_cards():  # O(m)
        if c[0] in l:
            if c[1] == 'Hearts':
                Hearts += 1
            elif c[1] == 'Diamonds':
                Diamonds += 1
            elif c[1] == 'Spades':
                Spades += 1
            elif c[1] == 'Clubs':
                Clubs += 1
    for c in player.get_cards():  # O(n)
        if c[0] in l:
            if c[1] == 'Hearts':
                Hearts += 1
            elif c[1] == 'Diamonds':
                Diamonds += 1
            elif c[1] == 'Spades':
                Spades += 1
            elif c[1] == 'Clubs':
                Clubs += 1
    return Hearts >= 5 or Diamonds >= 5 or Spades >= 5 or Clubs >= 5


def has_straight_flush(table, player):
    """
    Determines if the player has a straight and a flush over the same interval

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is a straight and a flush over the same interval , False otherwise

    Runtime: O(xlog(x)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    total_cards_seen = set()
    for c in table.get_cards():  # O(m)
        total_cards_seen.add(c[0])
    for c in player.get_cards():  # O(n)
        total_cards_seen.add(c[0])

    if 14 in total_cards_seen:
        total_cards_seen.add(1) # adds a 1 if an ace is present, use to detect A,2,3,4,5 straights

    # For runtime purposes denote x=n+m
    sorted_cards_seen = list(sorted(total_cards_seen))  # O(xlog(x))
    straight = []
    temp = [sorted_cards_seen[0]]
    for i in range(0, len(sorted_cards_seen) - 1):  # O(x)
        if sorted_cards_seen[i + 1] == sorted_cards_seen[i] + 1:
            temp.append(sorted_cards_seen[i + 1])
        else:
            temp = [sorted_cards_seen[i + 1]]

        if len(temp) == 5:
            straight.append(temp)
            temp = temp[1:]
    if straight == []:
        return False
    for l in straight:  # at most O(7)=O(1)
        check = if_straight_is_flush(l, table, player)  # O(x)
        if check is True:
            return True
    return False


def has_four_of_a_kind(table, player):
    """
    Determines if the player has 4 cards of the same value

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast 4 cards of the same value, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    seen = repeated_cards(table, player)  # O(n+m)
    if max(seen.values()) >= 4:  # O(n+m)
        return True
    return False


def has_full_house(table, player):
    """
    Determines if the player has a 3 pair and a 2 pair

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is at least a 3 pair and a 2 pair, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    seen = repeated_cards(table, player)  # O(n+m)
    pairs = set()
    triples = set()

    for k in seen.keys():  # O(n+m)
        if seen[k] >= 2:
            pairs.add(k)
        if seen[k] >= 3:
            triples.add(k)

    if len(triples) > 1:
        return True
    elif len(triples) > 0:
        for p in pairs:
            if p not in triples:
                return True
    return False


def has_flush(table, player):
    """
    Determines if the player has 5 cards of the same suit

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast 5 cards of the same suit, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    Hearts = set()
    Diamonds = set()
    Spades = set()
    Clubs = set()
    for c in table.get_cards():  # O(m)
        if c[1] == 'Hearts':
            Hearts.add(c)
        elif c[1] == 'Diamonds':
            Diamonds.add(c)
        elif c[1] == 'Spades':
            Spades.add(c)
        elif c[1] == 'Clubs':
            Clubs.add(c)
    for c in player.get_cards():  # O(n)
        if c[1] == 'Hearts':
            Hearts.add(c)
        elif c[1] == 'Diamonds':
            Diamonds.add(c)
        elif c[1] == 'Spades':
            Spades.add(c)
        elif c[1] == 'Clubs':
            Clubs.add(c)
    if len(Hearts) >= 5 or len(Diamonds) >= 5 or len(Spades) >= 5 or len(
            Clubs) >= 5:
        return True
    return False


def has_straight(table, player):
    """
    Determines if the player has 5 cards in a row

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast 5 cards in a row, False otherwise

    Runtime: O(xlog(x)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    total_cards_seen = set()
    for c in table.get_cards():  # O(m)
        total_cards_seen.add(c[0])
    for c in player.get_cards():  # O(n)
        total_cards_seen.add(c[0])

    if 14 in total_cards_seen:
            total_cards_seen.add(1) # adds a 1 if an ace is present, use to detect A,2,3,4,5 straights 

    # For runtime purposes denote x=n+m
    sorted_cards_seen = list(sorted(total_cards_seen))  # O(xlog(x))
    counter = 0
    for i in range(len(sorted_cards_seen) - 1):  # O(x)
        if counter == 0:
            counter += 1
        if sorted_cards_seen[i + 1] == sorted_cards_seen[i] + 1:
            counter += 1
        else:
            counter = 0
        if counter >= 5:
            return True
    return False


def has_three_of_a_kind(table, player):
    """
    Determines if the player has 3 cards of the same value

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast 3 cards of the same value, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    seen = repeated_cards(table, player)  # O(n+m)
    if max(seen.values()) >= 3:  # O(n+m)
        return True
    return False


def has_two_pair(table, player):
    """
    Determines if the player has atleast two pairs

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast two pairs, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """

    seen = repeated_cards(table, player)  # O(n+m)
    pairs = set()

    for k in seen.keys():  # O(n+m)
        if seen[k] >= 2:
            pairs.add(k)

    if len(pairs) >= 2:
        return True
    else:
        return False


def has_one_pair(table, player):
    """
    Determines if the player has atleast one pair

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output: True if there is atleast one pair, False otherwise

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    seen = repeated_cards(table, player)  # O(n+m)
    if max(seen.values()) >= 2:
        return True
    return False


def repeated_cards(table, player):
    """
    Given a table and a player, determines if there are repeated cards

    Inputs:
    table - an object of the Table class
    player - an object of the Player class

    Output:
    seen - a dictionary with the keys being the cards seen and the values being
    how often each card is seen.

    Runtime: O(n+m) where n is the the number of cards that the player
    has and m is the number of cards on the table
    """
    seen = dict()
    for c in player.get_cards():
        seen.setdefault(c[0], 0)
        seen[c[0]] = seen[c[0]] + 1
    for c in table.get_cards():
        seen.setdefault(c[0], 0)
        seen[c[0]] = seen[c[0]] + 1
    return seen


def highest_card(players):
    """
    Given a list of players determines which player has the highest card

    Inputs: players - a list of players to check

    Output: Which player has the highest card

    Runtime: O(n) where n is the number of players
    """
    highest = 0
    for p in players:
        highest = max(highest, max(p.get_cards())[0])
    return [p for p in players if max(p.get_cards())[0] == highest]
