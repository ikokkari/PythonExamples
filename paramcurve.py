import turtle
import math


def dist(p1, p2):
    return (p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]-p2[1]) * (p1[1]-p2[1])


def render(f, ts, te, fill=True):
    def render_piece(f, ts, te, ps, pe, depth):
        if depth > 0 or dist(ps, pe) > 2:
            tm = (ts + te) / 2
            pm = f(tm)
            render_piece(f, ts, tm, ps, pm, depth-1)
            render_piece(f, tm, te, pm, pe, depth-1)
        else:
            turtle.goto(pe)
    ps = f(ts)
    pe = f(te)
    turtle.hideturtle()
    turtle.tracer(10000, 0)
    turtle.penup()
    turtle.goto(ps)
    turtle.pendown()
    turtle.pensize(width=2)
    if fill:
        turtle.begin_fill()
    render_piece(f, ts, te, ps, pe, 5)
    if fill:
        turtle.end_fill()
    turtle.update()


# https://en.wikipedia.org/wiki/Superellipse

def superellipse(cp, r, e):
    def f(t):
        co = math.cos(math.tau * t)
        si = math.sin(math.tau * t)
        if co > 0:
            co_s = +1
        else:
            co_s = -1
        if si > 0:
            si_s = +1
        else:
            si_s = -1
        return (cp[0] + r * math.pow(math.fabs(co), 2/e) * co_s,
                cp[1] + r * math.pow(math.fabs(si), 2/e) * si_s)
    return f


# https://en.wikipedia.org/wiki/Lissajous_curve

def lissajous(cp, a, b, A=45, B=45, delta=0):
    def f(t):
        return (cp[0] + A * math.sin(a * math.tau * t),
                cp[1] + B * math.cos(b * math.tau * t))
    return f


if __name__ == "__main__":
    e = 1.2
    turtle.title("Superellipses and Lissajous curves")
    for x in range(-400, 100, 100):
        for y in range(-300, 400, 100):
            render(superellipse((x, y), 45, e), 0, 1)
            e += 0.1
    for a in range(1, 5):
        for b in range(a+1, a+15, 2):
            x = 100 * a
            y = -350 + 50 * (b - a)
            render(lissajous((x, y), a, b), 0, 1, fill=False)
