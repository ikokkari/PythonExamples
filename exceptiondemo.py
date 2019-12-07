# So far, we have assumed that nothing goes wrong. However, things can go
# wrong while the program is run, and we must be able to detect and recover
# from these sort of situations. For example, when asking user to input a
# number, he has obediently typed in a number... but what if he types in
# "Hello world", just to see what happens? The next piece of code is more
# robust in that if the input is not an integer, it detects this and asks
# the user to try again.

while True: # loop as long as we have to
    try:
        value = int(input("Please enter an integer: "))
        # If we get here, the previous statement worked
        break
    except ValueError:
        print("That is not an integer. Try again.")
        
print("You entered", value)

# Similarly, what if we try to open a nonexistent file? That also has to
# fail somehow, right?

try:
    file = None # Make sure the variable 'file' exists no matter what
    file = open("nonexistent.txt")
    lines = list(file)
except IOError:
    print("Can't open the file.")
finally:  # This code will be executed no matter what happens earlier
    if file != None:
        file.close()

# However, not all exceptions are errors, but they are a perfectly
# valid part of Python's control. For example, so far we have iterated
# over sequences and other iterables with the for loop. Let's see how
# the explicit iteration works. The Python functions iter and next are
# used to iterate explicitly, and when the iterator reaches the end of
# whatever it is iterating, it raises a StopIteration exception.

items = [1, 2, 3, 4]
it = iter(items)     # ask the list for an iterator to its beginning
try:
    while True:
        value = next(it) # raises StopIteration at the end
        print(value)
except StopIteration:
    print("And that's all she wrote!")

# Of course, in practice we rarely write an explicit iteration loop
# like the above, since Python's for-iteration does the same with a
# much easier syntax.