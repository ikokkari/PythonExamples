from random import Random
from itertools import combinations

# When using random numbers, hardcode the seed to make results reproducible.

rng = Random(12345)

# Define the suits and ranks that a deck of playing cards is made of.

suits = ['clubs', 'diamonds', 'hearts', 'spades']
ranks = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
         'nine': 9, 'ten': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

deck = [(rank, suit) for suit in suits for rank in ranks]


def deal_hand(n, taken=None):
    """Deal a random hand with n cards, without replacement."""
    hand, taken = [], taken if taken else []
    while len(hand) < n:
        c = rng.choice(deck)
        if c not in hand and c not in taken:
            hand.append(c)
    return hand

# If we don't care about taken, this could be one-liner:
# return rng.sample(deck, n)


def gin_count_deadwood(hand):
    """Count the deadwood points of leftover cards in gin rummy."""
    total = 0
    for (_, rank) in hand:
        total += 1 if ranks[rank] == 14 else min(ranks[rank], 10)
    return total


def blackjack_count_value(hand):
    """Given a blackjack hand, count its numerical value. This
    value is returned as a string to distinguish between blackjack
    and 21 made with three or more cards, and whether the hand is
    soft or hard."""
    total = 0  # Current point total of the hand
    soft = 0   # Number of soft aces in the hand
    for (rank, _) in hand:
        v = ranks[rank]
        if v == 14:  # Treat every ace as 11 to begin with
            total, soft = total+11, soft+1
        else:
            total += min(10, v)  # All face cards are treated as tens
        if total > 21:
            if soft:  # Saved by the soft ace
                soft, total = soft-1, total-10
            else:
                return 'bust'
    if total == 21 and len(hand) == 2:
        return 'blackjack'
    return f"{'soft' if soft else 'hard'} {total}"


def poker_has_flush(hand):
    """Determine if the five card poker hand has a flush."""
    look_for = None
    for (_, suit) in hand:
        if look_for is None:  # First card in the hand determines suit
            look_for = suit
        elif look_for != suit:  # Other cards must be same suit
            return False
    # We can't return True until we have looked at every card in hand.
    return True


def count_rank_pairs(hand):
    """Utility function that allows us quickly determine the
    rank shape of the hand. Count how many pairs of identical
    ranks exist inside the hand, comparing each card to the
    ones after it. Instead of two nested for-loops, we use
    itertools.combinations for brevity and clarity."""
    count = 0
    for ((r1, _), (r2, _)) in combinations(hand, 2):
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
    if count_rank_pairs(hand) > 0:
        return False
    # After that hurdle, we know that the hand has no pairs.
    hand_ranks = [ranks[rank] for (rank, _) in hand]
    min_rank, max_rank = min(hand_ranks), max(hand_ranks)
    if max_rank == 14:  # Special cases for straights with an ace
        return min_rank == 10 or sorted(hand) == [2, 3, 4, 5, 14]
    else:  # Hand has no aces, so it must be five consecutive ranks
        return max_rank-min_rank == 4


# Straight flushes complicate the hand rankings a bit.


def poker_flush(hand):
    return poker_has_flush(hand) and not poker_has_straight(hand)


def poker_straight(hand):
    return poker_has_straight(hand) and not poker_has_flush(hand)


def poker_straight_flush(hand):
    return poker_has_straight(hand) and poker_has_flush(hand)


# "Sometimes nothing can be a pretty cool hand."

def poker_high_card(hand):
    return count_rank_pairs(hand) == 0 and not poker_has_flush(hand) and not poker_has_straight(hand)

# In fact, there are not too many five card hands (since there are
# exactly choose(52, 5) = 2,598,960) for us to loop through to make
# sure that all counts agree with those given in the Wikipedia page
# https://en.wikipedia.org/wiki/List_of_poker_hands


def evaluate_all_poker_hands():
    funcs = [poker_one_pair, poker_two_pair, poker_three_of_kind,
             poker_straight, poker_flush, poker_full_house,
             poker_four_of_kind, poker_straight_flush, poker_high_card]
    counters = [0 for _ in funcs]
    for hand in combinations(deck, 5):
        for (i, f) in enumerate(funcs):
            if f(hand):
                counters[i] += 1
                break  # No point looking for more for this hand
    result = [(f.__name__, counters[i]) for (i, f) in enumerate(funcs)]
    assert sum(c for (_, c) in result) == 2598960
    return result


if __name__ == "__main__":
    print(evaluate_all_poker_hands())
