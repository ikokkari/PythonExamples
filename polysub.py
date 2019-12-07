import random
import turtle

def interp(p1, p2, t):
    return ( (1-t) * p1[0] + t * p2[0], (1-t)* p1[1] + t * p2[1] )

def dist(p1, p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1])

def polysub(pts, depth = 5, width = 0.1):
    polys = []
    def subdivide(pts, depth):
        if depth < 1:
            polys.append(pts)
        else:
            l1 = dist(pts[0], pts[1])
            l2 = dist(pts[1], pts[2])
            r = random.uniform(0, l1+l2)
            if r < l1:
                i = 0
            else:
                i = 1
            t1 = random.uniform(0.5 - width, 0.5 + width)
            t2 = random.uniform(0.5 - width, 0.5 + width)
            pa = interp(pts[i], pts[i+1], t1)
            pb = interp(pts[i+2], pts[(i+3)%4], t2)
            subdivide((pts[i], pa, pb, pts[(i+3)%4]), depth - 1)
            subdivide((pa, pts[i+1], pts[i+2], pb), depth - 1)
    subdivide(pts, depth)
    return polys

def render(polys):
    turtle.hideturtle()
    turtle.title("Pastel subdivision")
    turtle.tracer(10000,0)
    turtle.colormode(cmode = 255)
    for pts in polys:
        turtle.penup()
        turtle.goto(pts[3])
        turtle.begin_fill()
        turtle.fillcolor(random.randint(64, 192), random.randint(64, 192),
                         random.randint(64, 192))
        turtle.pendown()
        for pt in pts:
            turtle.goto(pt)
        turtle.end_fill()
    turtle.update()
            

render(polysub(((-350,-350),(350,-350),(350,350),(-350,350)), 6, 0.07))
