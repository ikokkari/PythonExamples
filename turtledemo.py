import turtle
from math import sqrt

def spiral(n):
    while(n > 5):
        turtle.forward(n)
        turtle.right(90)
        turtle.forward(n)
        turtle.right(90)
        n -= 5

def koch(d):
    # Once the line segment is short enough, render it as segment.
    if d < 5:
        turtle.forward(d)
    # Subdivide the segment into four thirds according to Koch rule.
    else:
        koch(d/3)
        turtle.left(60)
        koch(d/3)
        turtle.right(120)
        koch(d/3)
        turtle.left(60) # 60 - 120 + 60 == 0, as it should
        koch(d/3)

# Koch Snowflake consist of three Koch curves arranged in triangle.
def koch_snowflake(d):
    for x in range(3):
        koch(d)
        turtle.right(120)

s2 = sqrt(2)
def zig(d, m1, m2):
    if d < 10:
        turtle.forward(d)
    else:
        m1(90)
        zig(.5 * d, m1, m2)
        zig(.5 * d, m2, m1)
        m2(135)
        zig(.5 * s2 * d, m2, m1)
        zig(.5 * s2 * d, m1, m2)
        m1(45)

# Fractal trees are a classic turtle graphics application.
def tree(d):
        # Every tree starts with the trunk.
        turtle.forward(d)
        if d > 3:
            # Take the absolute position for safekeeping.
            pos = turtle.position()
            heading = turtle.heading()
            turtle.left(70)
            tree(d/1.5)
            # Restore the position to the end of trunk.
            turtle.penup()            
            turtle.setposition(pos)
            turtle.setheading(heading)
            turtle.pendown()
            turtle.right(35)
            tree(d/1.5)

if __name__ == "__main__":
    turtle.tracer(10000, 0)
    turtle.penup()
    turtle.hideturtle()
    turtle.setposition(0, 150)
    turtle.setheading(45)
    turtle.pendown()
    koch_snowflake(300)
    turtle.penup()
    turtle.setposition(-400, 350)
    turtle.setheading(0)
    turtle.pendown()
    spiral(300)
    turtle.penup()
    turtle.setposition(-300, -100)
    turtle.setheading(270)
    turtle.pendown()
    zig(150, turtle.left, turtle.right)
    turtle.penup()
    turtle.setposition(200, -380)
    turtle.setheading(90)
    turtle.pendown()
    tree(150)

    turtle.update()
    
