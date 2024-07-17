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


def gin_count_deadwood(deadwood):
    """Count the deadwood points of leftover cards in gin rummy."""
    return sum(1 if rank == 'ace' else min(ranks[rank], 10) for (rank, _) in deadwood)


def blackjack_count_value(hand):
    """Given a blackjack hand, count its numerical value. This
    value is returned as a string to distinguish between blackjack
    and 21 made with three or more cards, and whether the hand is
    soft or hard."""
    total = 0  # Current point total of the hand
    soft = 0   # Number of soft aces in the hand
    for (rank, _) in hand:
        rank_n = ranks[rank]
        if rank_n == 14:  # Treat every ace as 11 to begin with
            total, soft = total + 11, soft + 1
        else:
            total += min(10, rank_n)  # All face cards are treated as tens
        if total > 21:
            if soft:  # Saved by the soft ace
                soft, total = soft - 1, total - 10
            else:
                return 'bust'
    if total == 21 and len(hand) == 2:
        return 'blackjack'
    return f"{'soft' if soft else 'hard'} {total}"


def poker_has_flush(hand):
    """Determine if the five card poker hand has a flush."""
    return all(suit == hand[0][1] for (_, suit) in hand)


def count_rank_pairs(hand):
    """Utility function that allows us quickly determine the
    rank shape of the hand. Count how many pairs of identical
    ranks exist inside the hand, comparing each card to the
    ones after it. Instead of two nested for-loops, we use
    itertools.combinations for brevity and clarity."""
    return sum(r1 == r2 for ((r1, _), (r2, _)) in combinations(hand, 2))


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
    hand_ranks = [ranks[rank] for (rank, _) in hand]
    # Pythonic technique to check that list doesn't contain duplicates.
    if len(set(hand_ranks)) < 5:
        return False
    # Now we know that the hand doesn't contain duplicate ranks.
    min_rank, max_rank = min(hand_ranks), max(hand_ranks)
    if max_rank == 14:  # Special cases for straights with an ace
        return min_rank == 10 or sorted(hand) == [2, 3, 4, 5, 14]
    else:  # Hand has no aces, so check if it is five consecutive ranks
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
    result = [(f.__name__, count) for (f, count) in zip(funcs, counters)]
    expected = [1098240, 123552, 54912, 9180, 5112, 3744, 624, 36, 1303560]
    assert [count for (_, count ) in result] == expected
    return result


if __name__ == "__main__":
    print(evaluate_all_poker_hands())
