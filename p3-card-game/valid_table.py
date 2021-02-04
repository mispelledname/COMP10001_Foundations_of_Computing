# dictionary of card values with their corresponding point values
VALUES = {
               'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
               '8': 8, '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13
               }

# dictionary of card suits and their corresponding colours where 0 denotes 
# black while 1 denotes red
SUITS = {'D': 0, 'C': 1, 'H': 0, 'S': 1}

ACE = 20
MIN_RUN_LENGTH = 3

def factorial(n):
    '''calculates the n factorial for some input n'''
    if n == 0: 
        return 1
    return n * factorial(n - 1)

def comp10001go_score_group(cards):
    '''takes in a list of cards and returns an integer score for the group
    based on the rules of the game'''
    
    # returns zero if empty group
    if not cards:
        return 0
    
    # returns the negative score sum if group is singleton
    if len(cards) == 1:
        value = cards[0][0]
        return -VALUES[value]
    
    # extract the card values and colours into a list of tuples
    card_tuples = []
    for card in cards:
        card_tuples.append((VALUES[card[0]], SUITS[card[-1]]))
    card_tuples = sorted(card_tuples)
    
    # if the group is a valid n-of-a-kind, score is value times n factorial
    if card_tuples[-1][0] != ACE:
        values_set = set(x for x, y in card_tuples)
        if len(values_set) == 1:
            return card_tuples[0][0] * factorial(len(card_tuples))
    
    # early exit if there are fewer than three cards
    if len(card_tuples) < MIN_RUN_LENGTH:
        return -sum(list(x for (x, y) in card_tuples))
    
    # counts the number of aces in the group 
    ace_tally = 0
    red_ace_tally = 0
    black_ace_tally = 0
    for card in card_tuples[::-1]:
        if card[0] == ACE:
            ace_tally += 1
            card_tuples.remove(card)
            if card[1] == 0:
                red_ace_tally += 1
            else:
                black_ace_tally += 1
        else:
            break
    
    # check if the group is a valid run
    # early exit if the group only consists of aces
    if not card_tuples:
        return ace_tally * ACE
    
    # early exit if there are repeats in the group
    values_set = set(x for x, y in card_tuples)
    if len(values_set) != len(card_tuples):
        return -sum(list(x for (x, y) in card_tuples)) - ace_tally * ACE
    
    # early exit if the aces can't possibly fill the gaps
    low = card_tuples[0][0]
    high = card_tuples[-1][0]
    if (high - low + 1) != len(card_tuples) + ace_tally:
        return -sum(list(x for (x, y) in card_tuples)) - ace_tally * ACE
    
    # check if there are the correct number of correct coloured aces for the 
    # group to form a run
    prev_value = low
    prev_colour = card_tuples[0][1]
    counted_cards = [card_tuples[0]]
    card_tuples = card_tuples[1:]
    while prev_value < high:
        if card_tuples[0][0] != prev_value + 1:
            if prev_colour:
                red_ace_tally -= 1
            else:
                black_ace_tally -= 1
        elif (card_tuples[0][1] + prev_colour) % 2 == 0:
            return (
                    - sum(list(x for (x, y) in card_tuples)) - 
                    sum(list(x for (x, y) in counted_cards)) - 
                    ace_tally * ACE
                    )
        else:
            counted_cards.append(card_tuples[0])
            card_tuples = card_tuples[1:]
        prev_value += 1
        prev_colour = (prev_colour + 1) % 2
    
    # case where the aces could not act as wilds to form a run
    if red_ace_tally != 0 or black_ace_tally != 0:
        return (
                - sum(list(x for (x, y) in card_tuples)) - 
                sum(list(x for (x, y) in counted_cards)) - 
                ace_tally * ACE
                )
    
    # if the group is a run, return the sum of the continuous sequence 
    value = 0
    for x in range(low, high + 1):
        value += x
    return value