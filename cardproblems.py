# Define the suits and ranks that a deck of playing cards is made of.

suits = ['clubs', 'diamonds', 'hearts', 'spades']
ranks = {'two': 2, 'three': 3, 'four' : 4, 'five' : 5, 'six' : 6,
         'seven' : 7, 'eight' : 8, 'nine' : 9, 'ten' : 10, 'jack' : 11,
         'queen' : 12, 'king' : 13, 'ace' : 14 }

deck = [ (rank, suit) for suit in suits for rank in ranks ]

import random

# Deal a random hand with n cards, without replacement.

def deal_hand(n, taken = []):
    result = []
    while len(result) < n:
        c = random.choice(deck)
        if c not in result and c not in taken:
            result.append(c)
    return result

# If we don't care about taken, this could be one-liner:
# return random.sample(deck, n)

# Given cards in the game of gin rummy, count their deadwood points.

def gin_count_deadwood(hand):
    count = 0
    for (rank, suit) in hand:
        v = ranks[rank]
        if v == 14:
            v = 1
        elif v > 10:
            v = 10
        count += v
    return count

# Given a blackjack hand, count its numerical value. This value is returned
# as a string to distinguish between blackjack and 21 made with three or
# more cards, and whether the hand is soft or hard. 

def blackjack_count_value(hand):
    total = 0 # Current point total of the hand
    soft = 0 # Number of soft aces in the current hand
    for (rank, suit) in hand:
        v = ranks[rank]
        if v == 14: # Treat every ace as 11 to begin with
            total, soft = total + 11, soft + 1
        else:
            total += min(10, v) # All face cards are treated as tens
        if total > 21:
            if soft > 0: # Saved by the soft ace
                soft, total = soft - 1, total - 10                
            else:
                return "bust"
    if total == 21 and len(hand) == 2:
        return "blackjack"
    return f"{'soft' if soft > 0 else 'hard'} {total}"

# Determine if the five card poker hand has a flush, that is, all five
# cards have the same suit.

def poker_has_flush(hand):
    suit = None
    for (r, s) in hand:
        if suit == None:
            suit = s
        elif suit != s:
            return False
    return True

# A utility function that allows us quickly determine the rank shape of
# the hand. Count how many pairs of identical ranks there are in the
# hand, comparing each card to the ones after it.

from itertools import combinations

def count_rank_pairs(hand):
    count = 0
    for ((r1, s1), (r2, s2)) in combinations(hand, 2):
        if r1 == r2:
            count += 1
    return count

# The previous function makes all the following functions trivial.

def poker_four_of_kind(hand):
    return count_rank_pairs(hand) == 6

def poker_full_house(hand):
    return count_rank_pairs(hand) == 4

def poker_three_of_kind(hand):
    return count_rank_pairs(hand) == 3

def poker_two_pair(hand):
    return count_rank_pairs(hand) == 2

def poker_one_pair(hand):
    return count_rank_pairs(hand) == 1

# Of the possible poker ranks, straight is the trickiest to check when
# the hand is unsorted. Also, ace can work either as highest or lowest
# card inside a straight. 

def poker_has_straight(hand):
    # If a hand has any pairs, it is not a straight.
    if count_rank_pairs(hand) > 0: return False
    # We know now that the hand has no pairs.
    hand_ranks = [ranks[rank] for (rank, suit) in hand]
    min_rank = min(hand_ranks)
    max_rank = max(hand_ranks)
    if max_rank == 14: # Special cases for ace straights
        if min_rank == 10: return True #AKQJT
        return all(x in hand_ranks for x in [2, 3, 4, 5]) #A2345
    else:
        return max_rank - min_rank == 4

# Straight flushes complicate the hand rankings a little bit.

def poker_flush(hand):
    return poker_has_flush(hand) and not poker_has_straight(hand)

def poker_straight(hand):
    return poker_has_straight(hand) and not poker_has_flush(hand)

def poker_straight_flush(hand):
    return poker_has_straight(hand) and poker_has_flush(hand)

# "Sometimes nothing can be a pretty cool hand."

def poker_high_card(hand):
    return count_rank_pairs(hand) == 0 and not poker_has_flush(hand)\
           and not poker_has_straight(hand)

# In fact, there are not too many five card hands (since there are
# exactly choose(52, 5) = 2,598,960) for us to loop through to make
# sure that all counts agree with those given in the Wikipedia page
# https://en.wikipedia.org/wiki/List_of_poker_hands 

def evaluate_all_poker_hands():
    funcs = [poker_high_card, poker_one_pair, poker_two_pair, 
             poker_three_of_kind, poker_straight, poker_flush,
             poker_full_house, poker_four_of_kind, poker_straight_flush]
    counters = [0] * len(funcs)
    for hand in combinations(deck, 5):
        for (i, f) in enumerate(funcs):
            if f(hand):
                counters[i] += 1
                break # No point looking for more for this hand
    return [(f.__name__, counters[i]) for (i, f) in enumerate(funcs)]


# Compute the resulting score of a made contract in the game
# of contract bridge.
def bridge_score(suit, level, vul, dbl, made):
    mul = {'X':2, 'XX':4 }.get(dbl, 1)
    score, bonus = 0, 0
    
    # Add up the values of individual tricks.
    for trick in range(1, made + 1):
        # Raw points for this trick.
        if suit == 'clubs' or suit == 'diamonds':
            pts = 20
        elif suit == 'hearts' or suit == 'spades':
            pts = 30
        else:
            pts = 40 if trick == 1 else 30
        
        if trick <= level: # Part of contract
            score += mul * pts
        elif mul == 1: # Undoubled overtrick
            bonus += mul * pts
        elif mul == 2: # Doubled overtrick
            bonus += 200 if vul else 100
        else: # Redoubled overtrick
            bonus += 400 if vul else 200
    if score >= 100: # Game bonus
        bonus += 500 if vul else 300
    else: # Partscore bonus
        bonus += 50
    if level == 6: # Small slam bonus
        bonus += 750 if vul else 500
    if level == 7: # Grand slam bonus
        bonus += 1500 if vul else 1000
    score += bonus
    if mul == 2: # Insult bonus for making a (re)doubled contract
        score += 50
    elif mul == 4:
        score += 100
    return score


if __name__ == "__main__":
    print(evaluate_all_poker_hands())