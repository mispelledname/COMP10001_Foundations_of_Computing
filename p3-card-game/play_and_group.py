from itertools import combinations, groupby

# IMPORT FIRST & SECOND & BONUS DIAMONDS
# dictionary of card values with their corresponding point values
VALUES = {
               'A': 20, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
               '8': 8, '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13
               }

STD_FORM = {10: '0', 11: 'J', 12: 'Q', 13: 'K', 20: 'A'}

# dictionary of card suits and their corresponding colours where 0 denotes 
# black while 1 denotes red
SUITS = {'D': 0, 'C': 1, 'H': 0, 'S': 1}

ACE = 20
KING = 13
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

def comp10001go_valid_groups(groups):
    '''takes in a list of groups, each of which is a list of cards, and returns
    a Boolean indicating whether all groups are valid (i.e. singleton, 
    N-of-a-kind or a valid run) or not'''
    
    # early exit if group is empty 
    if not groups:
        return True
    
    # return False if there is a group with a negative score which is not a 
    # singleton 
    for cards in groups:
        if len(cards) != 1:
            score = comp10001go_score_group(cards)
            if score < 1:
                return False
    return True 

def group_generator(cards):
    '''takes a list of up to 10 cards and returns a tuple of all possible valid 
    grouping subsets alongside their scores'''
    
    # list all tuples of valid groups of size 1 to the total number of cards 
    i = len(cards)
    groups = []
    while i > 0:
        all_groups = list(combinations(cards, i))
        for group in all_groups:
            group = list(group)
            if comp10001go_valid_groups([group]):
                groups.append((comp10001go_score_group(group), group))
        i -= 1
    
    return sorted(groups, reverse=1)

def comp10001go_best_partitions(cards):
    '''takes a list of up to 10 cards and returns the groupings of cards that 
    score the most points from cards.'''
    
    # find all groups with positive scores 
    all_groups = group_generator(cards)
    pos_groups = []
    for group in all_groups:
        if group[0] > 0:
            pos_groups.append(group)
    
    # exceptional case where there are no groups with positive scores
    if not pos_groups:
        partition = []
        for card in cards:
            partition.append([card])
        return [partition]
    
    # generate all possible partitions that contain at least one positive 
    # scoring group 
    all_partitions = []
    for group in pos_groups:
        partition = [group[1]]
        score = group[0]
        curr_cards = [card for card in cards if card not in group[1]]
        while curr_cards:
            score += group_generator(curr_cards)[0][0]
            used = group_generator(curr_cards)[0][1]
            partition.append(used)
            for card in used:
                curr_cards.remove(card)
        all_partitions.append((score, sorted(partition)))
    all_partitions = sorted(all_partitions, reverse=1)
    
    # lists all unique partitions that generate the maximum possible score
    optimal_parts = []
    max_score = max([x for x, y in all_partitions])
    for score, partition in all_partitions:
        if score == max_score:
            optimal_parts.append(partition)
        
    return list(optimal_parts for optimal_parts,_ in groupby(optimal_parts))

def to_card_tuple(cards):
    '''Takes as input a list of cards in standard format and converts them into
    tuples of values and suits'''
    card_tuples = []
    for card in cards:
        card_tuples.append((VALUES[card[0]], card[-1]))
    return sorted(card_tuples)

def to_std_form(card_tuples):
    '''Takes as input card tuples and converts them into standard format'''
    cards = []
    for card in card_tuples:
        if card[0] < 10:
            cards.append(f'{card[0]}{card[1]}')
        else:
            cards.append(f'{STD_FORM[card[0]]}{card[1]}')
    return cards

def comp10001go_play(discard_history, player_no, hand):
    '''Takes as input the discard history of each player, the player's number 
    and the player's current hand and selects a single card to discard'''
    
    # early exit if there are no other options
    if len(hand) == 1:
        return hand[0]
    
    # extract values and suits from hand
    hand_tuples = to_card_tuple(hand)[::-1]
    
    # choose highest that is not K to play first
    if not discard_history:
        for value, suit in hand_tuples:
            if value != ACE and value != KING:
                return to_std_form([(value, suit)])[0]
    
    # extract the cards values and suits of currently in my discard pile
    my_discards = []
    for rounds in discard_history:
        my_discards.append(rounds[player_no])
    discard_tuples = to_card_tuple(my_discards)[::-1]
    
    # strategy for the first five rounds
    if len(discard_history) < 6:
        for value, suit in hand_tuples: 
            for card in discard_tuples: 
                # find duplicates
                if value == card[0]:
                    return to_std_form([(value, suit)])[0]
                # find consecutives
                if value == card[0] + 1 or value == card[0] - 1:
                    if SUITS[suit] != SUITS[card[1]]:
                        return to_std_form([(value, suit)])[0]
                    
    # strategy from the sixth round onwards
    elif len(discard_history) >= 6:
        possibilities = []
        # try every card in hand and return the card which produces the optimal
        # score 
        for card in hand:
            possible_discards = my_discards
            possible_discards.append(card)
            partition = comp10001go_best_partitions(possible_discards)[0]
            score = 0
            for group in partition:
                score += comp10001go_score_group(group)
            possibilities.append((score, card))
        possibilities = sorted(possibilities, reverse=1)
        
        return possibilities[0][1]

def comp10001go_group(discard_history, player_no):
    '''Takes as input the discard history of each player and the player number
    to group the discards into groups for scoring'''
    
    # create a list of the specified player's discarded cards
    cards = []
    for discards in discard_history:
        cards.append(discards[player_no])
    
    # return an optimal grouping of cards
    return comp10001go_best_partitions(cards)[0]