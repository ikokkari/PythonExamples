from abc import ABC, abstractmethod
from math import pi
from random import randint

# Making your class extend ABC forbids creation of objects. This
# type serves as abstract superclass that guarantees that every
# subclass that will ever exist will have certain methods in them.

# Shape hierarchy is a standard example of class inheritance, other
# than the Animal class hierarchy, both quite a bit cliched. But all
# cliches became cliches in the first place by being so good that
# everybody and their brother kept using them!


class Shape(ABC):

    # A class attribute, so the same value is shared by everyone.
    count = 0

    # This method is executed automatically at every object creation.
    # Even though Shape is an abstract class, subclass objects can
    # still be created, and we want them to count as Shapes.
    def __init__(self):
        Shape.count += 1

    # All subclasses must implement these abstract methods, since
    # otherwise those subclasses are also abstract. (Which can also
    # be totally reasonable in some situations.)
    @abstractmethod
    def name(self):
        # Python do-nothing statement for situations like this.
        pass

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    # Dunder ("magic") method to convert the object into a string. Note
    # how we take the existence of name() and area() for granted.
    def __str__(self):
        n, a, p = self.name(), self.area(), self.perimeter()
        return f"{n} of area {a:.2f} and perimeter {p:.2f}"


# A subclass of Shape that defines area and perimeter to work one way.

class Rectangle(Shape):

    def __init__(self, width, height):
        super().__init__()
        self.__width = width
        self.__height = height

    def name(self):
        if self.is_square():
            return 'Square'
        else:
            return 'Rectangle'

    def area(self):
        return self.__width * self.__height

    def perimeter(self):
        return 2 * (self.__width + self.__height)

    # We can define new methods that do not exist in superclass.

    def is_square(self):
        return self.__width == self.__height


# Another subclass of Shape, with different area and perimeter formulas.

class Circle(Shape):

    def __init__(self, radius):
        super().__init__()
        self.__radius = radius

    def name(self):
        return 'Circle'

    def area(self):
        return pi * self.__radius * self.__radius

    def perimeter(self):
        return pi * self.__radius * 2


# Just like function decorators, objects can be decorated. The class
# for this purpose has the same methods, but those methods first ask
# the underlying object for the answer that they then modify some way.

class Scaled(Shape):

    def __init__(self, other, scale):
        super().__init__()
        self.other = other
        self.scale = scale

    def name(self):
        return f"({self.other.name()} scaled by {self.scale})"

    def area(self):
        return self.other.area() * self.scale * self.scale

    def perimeter(self):
        return self.other.perimeter() * self.scale


# Demonstrate the previous classes in action.

def __demo():
    # An abstract class cannot be instantiated.
    try:
        _ = Shape()
    except Exception as e:
        print(f"Caught: {e}")

    # Let's create some objects to demonstrate how classes work.
    r1 = Rectangle(2, 3)
    print(f"Created: {r1}.")
    r2 = Rectangle(5, 5)
    print(f"Created: {r2}.")
    c = Circle(10)
    print(f"Created: {c}.")
    d = Circle(5)
    print(f"Created: {d}.")

    # Next, we ask these objects what they think they are.
    print(f"\nObject r1 is of type {type(r1)}.")
    print(f"Is object r1 a Rectangle? {isinstance(r1, Rectangle)}")
    print(f"Is object r1 a Circle? {isinstance(r1, Circle)}")

    # An object is an instance of every class of its superclass chain.
    print(f"Is object r1 a Shape? {isinstance(r1, Shape)}")

    # Object attributes can be "monkey patched" on the fly. People
    # used to Java and other statically typed languages would reel
    # back in horror seeing something like this. But go bananas!

    # First, take the original names for safekeeping.
    tmp1, tmp2 = c.name, c.area
    # Lambdas can be defined to take no parameters, thus behaving
    # essentially as data.
    c.name = lambda: "Bob"
    c.area = lambda: randint(1, 100)
    print(f"\nObject c is now: {c}")  # Bob
    print(f"Object d is now: {d}")    # behaves normally

    # Restore the balance of the world.
    c.name, c.area = tmp1, tmp2
    print(f"Object c is now: {c}")  # behaves normally again
    print(f"Object d is now: {d}")  # behaves normally (still)

    # Demonstrate an object decorator in action.
    s1 = Scaled(r1, 2)
    print(f"Created: {s1}.")
    # Why not? Scalers are shapes, same way as any other shape.
    # Therefore they can be further decorated.
    s2 = Scaled(s1, 3)
    print(f"Created: {s2}.")

    print(f"Total of {Shape.count} Shape objects were created.")


if __name__ == "__main__":
    __demo()
