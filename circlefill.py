# after http://paulbourke.net/texture_colour/randomtile/

import random
import turtle
from math import sqrt


def dist(p1, p2):
    return sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) +
                (p1[1]-p2[1]) * (p1[1]-p2[1]))


def circlefill(n):
    result, s = [], 400
    while n > 0:
        cp = (random.uniform(-s, s), random.uniform(-s, s))
        rad = min(s/10, s-cp[0], cp[0]+s, s-cp[1], cp[1]+s)
        for c in result:
            rad = min(rad, dist(c[0], cp) - c[1])
            if rad < 2:
                break
        else:  # Executed if previous loop did not break out
            result.append((cp, rad))
            n -= 1
            if n % 100 == 0:
                turtle.update()
    return result


def render(circles):
    turtle.hideturtle()
    turtle.tracer(100, 0)
    turtle.colormode(cmode=255)
    for c in circles:
        turtle.penup()
        turtle.goto((c[0][0] + c[1], c[0][1]))
        turtle.setheading(90)
        turtle.pendown()
        turtle.fillcolor(random.randint(0, 255), random.randint(0, 255),
                         random.randint(0, 255))
        turtle.begin_fill()
        turtle.circle(c[1])
        turtle.end_fill()


if __name__ == "__main__":
    render(circlefill(50))
