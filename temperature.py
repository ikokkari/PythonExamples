# Example class to represent temperatures in various units. Showcases
# the use of properties to define managed attributes in classes that
# look like normal attributes from the outside, but whose setters and
# getters can silently perform arbitrary computations.


class Temperature:

    def __init__(self, t, unit='K'):
        if unit == 'K':
            self.K = t
        elif unit == 'C':
            self.C = t
        elif unit == 'F':
            self.F = t
        else:
            raise ValueError(f"Unknown unit system {unit}!")

    # The temperature is actually stored as kelvins inside the object.
    # However, the properties K, C and F allow the same temperature
    # to be accessed from the outside in different units as desired.

    @property
    def K(self):
        return self.__k

    @K.setter
    def K(self, k):
        # Prevent the creation of impossible temperatures.
        if k < 0:
            raise ValueError(f"Absolute temperature {k} may not be negative.")
        else:
            self.__k = k

    # The properties C and F are managed, that is, their values are
    # not actually stored inside the object, but they are computed
    # on the spot every time they are requested. When some class is
    # properly designed, it should be impossible for outside users
    # to be able to tell which properties are managed.

    @property
    def C(self):
        return self.K - 273

    @C.setter
    def C(self, c):
        self.K = c + 273

    @property
    def F(self):
        return 1.8 * self.C + 32

    @F.setter
    def F(self, f):
        self.C = (f - 32) / 1.8

    # The dunder methods for the string representation of object.
    # String representation meant for human readers.
    def __str__(self):
        return f"Temperature of {self.K} kelvins."

    # Representation meant for computer and eval function.
    def __repr__(self):
        return f"Temperature({self.K}, 'K')"

    # To allow order and equality comparisons, define the following
    # dunder methods in your class for the six operators.

    def __lt__(self, other):  # <
        return self.K < other.K

    def __gt__(self, other):  # >
        return self.K > other.K

    def __eq__(self, other):  # ==
        return self.K == other.K

    def __ne__(self, other):  # !=
        return self.K != other.K

    def __le__(self, other):  # <=
        return self.K <= other.K

    def __ge__(self, other):  # >=
        return self.K >= other.K

    # For temperatures, addition is meaningless, but temperatures
    # can be meaningfully subtracted from each other. Weird.
    def __sub__(self, other):
        return Temperature(abs(self.K - other.K))

    # Technically, temperature and temperature difference are two
    # separate concepts of the problem domain in physics, and thus
    # should be represented by two different data types, analogous
    # how datetime and timedelta are different data types in the
    # datetime standard library module.


def __demo():
    t1 = Temperature(30, 'C')
    print(f"Temperature t1 is {t1.C:.1f} C, {t1.F:.1f} F, {t1.K:.1f} K.")
    t2 = Temperature(100, 'F')
    print(f"Temperature t2 is {t2.C:.1f} C, {t2.F:.1f} F, {t2.K:.1f} K.")
    t3 = t1 - t2
    print(f"Their difference is {t3.K:.1f} K.")
    print(f"Does t1 < t2 ? {t1 < t2}")
    print(f"Does t1 > t2 ? {t1 > t2}")
    print(f"Does t1 == t1 ? {t1 == t1}")
    # And the crash.
    try:
        _ = Temperature(-400, 'C')
    except ValueError as e:
        print(f"Caught error: {e}")


if __name__ == "__main__":
    __demo()
