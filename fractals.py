import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import ndimage
from functools import partial

# Generally all these are after http://paulbourke.net/fractals/


def pointstep(size, n, fx, fy, w=2, exp=.5):
    ctr = np.zeros(shape=(size, size), dtype='uint16')
    cx, cy = .1, .2
    mv = 0
    for i in range(n):
        nx, ny = fx(cx, cy), fy(cx, cy)
        px = int((nx + w) / (2*w) * size)
        py = int((ny + w) / (2*w) * size)
        if px >= 0 and px < size and py >= 0 and py < size:
            ctr[py][px] += 1
            if ctr[py][px] > mv:
                mv = ctr[py][px]
        cx, cy = nx, ny
    pix = np.zeros(shape=(size, size), dtype='float')
    for y in range(size):
        for x in range(size):
            pix[size-x-1][size-y-1] = math.pow(ctr[y][x] / mv, exp)
    mat = [[.1, -.1, .5], [-.1, .2, -.1], [.5, -.1, .1]]
    return ndimage.convolve(pix, mat)


def dejong(size, n, a, b, c, d):
    def f1(cx, cy):
        return math.sin(a * cy) + math.cos(b * cx)

    def f2(cx, cy):
        return math.sin(c * cx) + math.cos(d * cy)

    return pointstep(size, n, f1, f2)


def clifford(size, n, a, b, c, d):

    def f1(cx, cy):
        return math.sin(a * cy) + c * math.cos(a * cx)

    def f2(cx, cy):
        return math.sin(b * cx) + d * math.cos(b * cy)

    return pointstep(size, n, f1, f2)


def move(x, y, size, step=1):
    nx = x + np.random.randint(-step, step + 1)
    ny = y + np.random.randint(-step, step + 1)
    nx = nx % size
    ny = ny % size
    if nx < 0:
        nx += size
    if ny < 0:
        ny += size
    return (nx, ny)


def avalanche_world(size, n, step=2, prob=0.3, pf=None):
    if pf is None:
        def pf():
            return np.random.uniform(0, 1)
    ctr = np.zeros(shape=(size, size), dtype='uint16')
    x = size // 2
    y = size // 2
    for i in range(n):
        ctr[y][x] += 1
        nx, ny = move(x, y, size, 1)
        if ctr[y][x] > ctr[ny][nx]:
            if ((ctr[y][x] - ctr[ny][nx]) * prob > pf()):
                ctr[ny][nx] += 1
                ctr[y][x] -= 1
                x, y = move(nx, ny, size, step)
    return ctr


def ifs(size, n, tbl, w=2, exp=0.2):
    ctr = np.zeros(shape=(size, size), dtype='uint16')
    cx, cy = 1, 1
    mv = 0
    for i in range(n):
        a, b, c, d, e, f = tbl[np.random.randint(0, len(tbl))]
        nx = a * cx + b * cy + e
        ny = c * cx + d * cy + f
        px = int(abs(nx) * size)
        py = int(abs(ny) * size)
        if px >= 0 and px < size and py >= 0 and py < size:
            ctr[py][px] += 1
            if ctr[py][px] > mv:
                mv = ctr[py][px]
        cx, cy = nx, ny
    pix = np.zeros(shape=(size, size), dtype='float')
    for y in range(size):
        for x in range(size):
            pix[size - y - 1][x] = math.pow(ctr[y][x] / mv, exp)
    mat = [[.3, -.1, .3], [-.1, .2, -.1], [.3, -.1, .3]]
    return ndimage.convolve(pix, mat)


def pascal(size, n=2):
    tri = np.ones(shape=(size, size), dtype='uint8')
    for row in range(1, size):
        for col in range(1, size):
            tri[row][col] = (tri[row-1][col] + tri[row][col-1]) % n
    return tri


def display(img, info, cmap='gray_r'):
    print(info)
    w = img.shape[1]
    h = img.shape[0]
    plt.figure(figsize=((w / 80), (h / 80)), dpi=80)
    plt.axis('off')
    plt.imshow(img, cmap=cmap)
    plt.show()


if __name__ == "__main__":
    tbl = [  # http://paulbourke.net/fractals/ifs_tree_a/
       (0.1950, -0.4880, 0.3440, 0.4430, 0.4431, 0.2452),
       (0.4620, 0.4140, -0.2520, 0.3610, 0.2511, 0.5692),
       (-0.6370, 0, 0, 0.5010, 0.8562, 0.2512),
       (-0.0350, 0.0700, -0.4690, 0.0220, 0.4884, 0.5069),
       (-0.0580, -0.0700, 0.4530, -0.1111, 0.5976, 0.0969)
    ]
    display(ifs(1000, 100000, tbl, w=1), "IFS Tree", cmap="tab20c")
    display(avalanche_world(500, 500000, 1, prob=0.3,
                            pf=partial(np.random.exponential, .5)),
            "Avalanche", cmap="gray")
    display(clifford(800, 1000000, -1.4, 1.6, 1.0, 0.7),
            "Clifford", cmap="plasma")
    display(dejong(800, 1000000, 1.4, -2.3, 2.4, -2.1), "DeJong")
    display(pascal(800, 5), "Pascal", cmap="prism")
    display(pascal(800, 3), "Pascal", cmap="tab20")
