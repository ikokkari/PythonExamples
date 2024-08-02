class Card:

    # Whenever the outside users of the class are not supposed to
    # access some member, the convention is to use double underscore
    # to start its name. They can still access it, but at least they
    # know that they are doing something that they are not supposed
    # to be doing.
    __values = {'ace': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
                'ten': 10, 'jack': 11, 'queen': 12, 'king': 13}

    # Normally you would only put function and name declarations
    # inside a class body, but this one just goes to show that any
    # statements inside the class body are executed the same way as
    # any other statements.
    print('Here we are, declaring a class...')

    # Function definitions are stored inside the class object that
    # is being defined, instead of the global namespace as usual.
    # First, some "dunder" methods that integrate this data type to
    # the rest of Python language.
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    # Note that unlike in certain other languages, you don't need to
    # explicitly state your instance attributes. You simply create
    # them on the fly in __init__ and other methods as needed.

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"Card('{self.rank}', '{self.suit}')"

    def get_value(self):
        return Card.__values[self.rank]

    # It is better software engineering for the capabilities of some
    # objects to be defined inside those objects, instead of writing
    # this as an outside function outranks(c1, c2, trump) like it
    # was still the sixties.

    def outranks(self, other, trump=None):
        if other is None:
            return True
        elif trump is None and self.suit != other.suit:
            return False
        elif self.suit == trump and other.suit != trump:
            return True
        else:
            return self.get_value() > other.get_value()

# Using the Card class, we could now implement some kind of trick taking
# game where each player is given a hand that is a list of cards. Let's
# quickly demonstrate that our cards and their methods work correctly.


c1 = Card('eight', 'hearts')
c2 = Card('ace', 'clubs')
c3 = Card('queen', 'hearts')
c4 = Card('two', 'diamonds')

print(f"Our cards are {c1}, {c2}, {c3} and {c4}.")

# Let's ask these objects exactly who they think they are.

print(f"Is the object {c1} instance of Card? {isinstance(c1, Card)}.")
print(f"The type object of {c1} is {type(c1)}.")
print(f"The type object of {c1} is {c1.__class__}.")
print(f"The type object of that object is {type(type(c1))}.")
print(f"The type object of that object is {type(type(type(c1)))}.")

# Let's see what names these objects contains.

print(f"Here is the directory of names in {c1}:")
print(", ".join(dir(c1)))
print("Here is the directory of names its class:")
print(", ".join(dir(Card)))

# Cards have the ability to check if they outrank other cards.

print("\nNext, some ranking comparisons between these cards.")
print(f"Does {c1} outrank {c2} in notrump? {c1.outranks(c2)}")
print(f"Does {c1} outrank {c2} in hearts? {c1.outranks(c2, 'hearts')}")
print(f"Does {c1} outrank {c3} in notrump? {c1.outranks(c3)}")
print(f"Does {c3} outrank {c1} in notrump? {c3.outranks(c1)}")


# Watch how much easier thinking about computations becomes once the
# concepts are sufficiently high level. One from your graded labs:

def winning_card(cards, trump=None):
    winner_so_far = None
    for card in cards:
        if card.outranks(winner_so_far, trump):
            winner_so_far = card
    return winner_so_far


trick = [c1, c2, c3, c4]
# Conversion of list to string uses repr, not str, for the list elements.
print(f"\nCards played into the trick are: {str(trick)}.")
# Usually you want to get a human-readable representation of the list.
print(f"Cards played are: {', '.join([str(c) for c in trick])}.")
print(f"In notrump, trick is won by {winning_card(trick, None)}.")
print(f"Hearts as trump, trick is won by {winning_card(trick, 'hearts')}.")
print(f"Diamonds as trump, trick is won by {winning_card(trick, 'diamonds')}.")
