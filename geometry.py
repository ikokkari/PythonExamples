# "God made the integers; all else is the work of man."
# -- Leopold Kronecker

import random
from functools import cmp_to_key

# Computational geometry is that what we can done with nothing
# but integers and their basic arithmetic operations. No trig
# or anything that could not be done with integers is needed,
# and yet we can do surprisingly much on the 2D plane.

# First, compute the signed 2D cross product of vectors
# p2-p1 and p3-p1 defined by three points p1, p2 and p3. This
# cross product is positive if the turn p1:p2:p3 is left-handed,
# negative if the turn p1:p2:p3 is right-handed, and zero if
# the points are collinear.


def cross(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

# The magnitude of the cross product is equal to the area of the
# parallelogram defined by the corner points p1, p2 and p3. The
# area of the triangle is therefore exactly half of that.

# The rest of the functions that operate on plane polygons assume
# that the corner points are given in counterclockwise order.
# Otherwise, exchange "left" and "right" in each discussion. Also,
# the polygon edges should not be self-crossing or degenerate.

# The area of an arbitrary polygon could be computed by splitting it
# into triangles (an interesting computational geometry problem of
# its own) and then adding up these triangles. However, we can do
# better with the shoelace algorithm. It adds up the area of polygon
# by adding signed triangles viewed from an arbitrary point, usually
# the origin. These signed areas cancel each other out when adding
# and subtracting the space outside the polygon.


def polygon_area_twice(poly):
    total, prev = 0, poly[-1]
    for p in poly:
        total += cross((0, 0), prev, p)
        prev = p
    return total


# Testing whether two line segments intersect can be done with
# checking turn handedness. No floating point arithmetic, trig or
# any kind of divisions are needed.

def __sign(n):
    return -1 if n < 0 else (+1 if n > 0 else 0)


def line_segment_intersect(p0, p1, p2, p3):
    # Just in case one of the line segments is a degenerate point.
    if p0 == p1:
        p0, p1, p2, p3 = p2, p3, p0, p1

    # Extract the components into named variables.
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p0, p1, p2, p3

    # Bounding box quick rejection check.
    if max(x0, x1) < min(x2, x3) or max(x2, x3) < min(x0, x1):
        return False
    if max(y0, y1) < min(y2, y3) or max(y2, y3) < min(y0, y1):
        return False

    # The turns (p0:p1:p2) and (p0:p1:p3) must have opposite signs.
    s1 = __sign(cross(p0, p1, p2))
    s2 = __sign(cross(p0, p1, p3))
    if s1 < 0 and s2 < 0 or s1 > 0 and s2 > 0:
        return False
    # It's important to check the crossing in both directions.
    s1 = __sign(cross(p2, p3, p0))
    s2 = __sign(cross(p2, p3, p1))
    return not(s1 < 0 and s2 < 0 or s1 > 0 and s2 > 0)


# An polygon is convex iff every turn along its edge is same-handed.

def polygon_is_convex(poly):
    p1, p2 = poly[-1], poly[-2]
    for p0 in poly:
        if cross(p2, p1, p0) < 0:
            return False
        p1, p2 = p0, p1
    return True


# To check whether a point x is inside the given convex polygon,
# check that the turn x:pts[i]:pts[i+1] is left-handed for every
# polygon edge pts[i]:pts[i+1].

# This function returns 0 if p is outside the polygon, 1 if it lies
# on the edge, 2 if it is a corner point, and 3 if the point lies
# properly inside with a nonzero distance to the outside world.

def point_inside_convex_polygon(poly, p):
    p1 = poly[-1]
    for p0 in poly:
        if p == p0:
            return 2
        if line_segment_intersect(p0, p1, p, p):
            return 1
        c = cross(p, p1, p0)
        if c < 0:
            return 0
        p1 = p0
    return 3


# Convexify the given polygon by eliminating right turns along
# the polygon edge. Also removes the redundant corner points
# that connect two consecutive collinear edges.

def convexify(poly, clean_only=False):
    # Initialize the stack with the first polygon edge.
    n, result = len(poly), [poly[0], poly[1]]

    def reject(c):
        return (clean_only and c == 0) or (not clean_only and c <= 0)
    # Loop through the points and eliminate right turns.
    for i in range(2, n + 1):
        p = poly[i % n]
        while len(result) > 1 and reject(cross(result[-2], result[-1], p)):
            result.pop()
        result.append(p)
    if result[0] == result[-1]:
        result.pop()
    return result


# Checking whether point (x, y) is inside an arbitrary polygon
# is a bit harder, but can be done based on observation that if
# you shoot an imaginary ray from (x, y) to any direction towards
# infinity, it will cross an odd number of edges on its way out.
# We have to be careful with corner points that connect two
# edges. Since we get to choose the direction of our imaginary
# ray freely, let's shoot it straight up towards the infinity of
# heavens.

def __cross_ray(x, y, x0, y0, x1, y1):
    # Quick rejection tests.

    if y0 < y and y1 < y:  # Both endpoints are below (x, y)
        return False
    if (x0 <= x and x1 <= x) or (x0 > x and x1 > x):
        return False  # Both are to left, or both are to right
    if y0 >= y and y1 >= y:
        return True   # Both above and on different sides

    # Swap if necessary for (x0, y0) to be left of (x1, y1).
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0

    # Turn (x0, y0) - (x, y) - (x1, y1) must be left-handed.
    return cross((x0, y0), (x, y), (x1, y1)) >= 0


def point_inside_polygon(poly, p):
    (x, y), (x1, y1), total = p, poly[-1], 0
    for (x0, y0) in poly:
        if (x0, y0) == (x, y):
            return 2
        if line_segment_intersect((x0, y0), (x1, y1), (x, y), (x, y)):
            return 1
        if __cross_ray(x, y, x0, y0, x1, y1):
            total += 1
        (x1, y1) = (x0, y0)
    return 3 if total % 2 == 1 else 0


# https://en.wikipedia.org/wiki/Pick%27s_theorem

def demonstrate_picks_theorem(poly):
    area_shoe = polygon_area_twice(poly)
    inside, boundary = 0, 0
    min_x = min((x for (x, y) in poly)) - 1
    max_x = max((x for (x, y) in poly)) + 1
    min_y = min((y for (x, y) in poly)) - 1
    max_y = max((y for (x, y) in poly)) + 1
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            r = point_inside_polygon(poly, (x, y))
            if r == 3:
                inside += 1
            elif r > 0:
                boundary += 1
    area_pick = 2*inside + boundary - 2
    print(f"shoe = {area_shoe}, pick = {area_pick}")
    return area_shoe == area_pick


# Compute the convex hull polygon of the given set of points. Graham
# scan starts by finding the star polygon of the points viewed from
# the lowest y-coordinate point, and then uses the previous stack
# algorithm to convexify the star polygon into the convex hull.

def convex_hull(pts, clean_only=False):
    pb = (min((x for (x, y) in pts)), min(y for (x, y) in pts))

    def angle_cmp(p1, p2):
        if p1 == pb:
            return -1
        elif p2 == pb:
            return +1
        c = -cross(pb, p1, p2)
        if c != 0:
            return c
        (dx, dy) = (p2[0] - p1[0], p2[1] - p1[1])
        if dy != 0:
            return dy
        elif dx != 0:
            return -dx
        else:
            return 0

    pts.sort(key=cmp_to_key(angle_cmp))
    return convexify(pts, clean_only)


# A "sweepline" algorithm that finds the two closest points in
# the given list of points on the two-dimensional plane. Sort
# the points by ascending x-coordinate. When comparing pairs of
# points, each point needs to be compared only with the previous
# points whose x-distance is less than equal to the current best
# distance that we have found somewhere.

# Squared Euclidean distance between two points on the plane.

def dist(p1, p2):
    return (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2


def closest_points(pts):
    pts.sort()
    best_d = dist(pts[0], pts[1])
    for i in range(2, len(pts)):
        j = i - 1
        while j >= 0 and (pts[i][0] - pts[j][0])**2 < best_d:
            best_d = min(best_d, dist(pts[i], pts[j]))
            j -= 1
    return best_d


def __demo():

    print("Let us compute the convex hull of a big grid.")
    pts = [(x, y) for x in range(100) for y in range(100)]
    random.shuffle(pts)
    pts = convex_hull(pts)
    print("The convex hull consists of the four corners:")
    print(pts)

    m, pts = 100, set()
    print(f"Next, create {m} random points on the plane.")
    pts.add((0, 0))
    while len(pts) < m:
        pts.add((random.randint(1, m), random.randint(1, m)))
    pts = list(pts)
    print(f"Closest point distance is {closest_points(pts):.3f}.")

    star = convex_hull(pts, clean_only=True)
    print(f"The star polygon consists of {len(star)} points.")

    print(f"Let us demonstrate Pick's theorem:")
    demonstrate_picks_theorem(star)

    hull = convexify(star)
    print(f"The convex hull consists of {len(hull)} points.")
    print(f"They are: {hull}")
    print(f"Pick's theorem still works:")
    demonstrate_picks_theorem(hull)

    print("Let's verify the point in convex polygon shortcut.")
    all_ok = True
    for x in range(0, m):
        for y in range(0, m):
            in1 = point_inside_polygon(hull, (x, y))
            in2 = point_inside_convex_polygon(hull, (x, y))
            if in1 != in2:
                print(f"Discrepancy at {(x,y)}: {in1} {in2}")
                all_ok = False
    if all_ok:
        print("Both functions returned the same answers.")


if __name__ == "__main__":
    __demo()
