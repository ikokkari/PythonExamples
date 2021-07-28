import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, ndimage

# Demonstrate the manipulation of raster images as numpy arrays of
# (h, w) for grayscale images, and (h, w, 3) for RGB images. Also
# showcase some handy functions from scipy.ndimage submodule.

# In image processing, convolution with a tactically chosen kernel
# matrix can achieve all kinds of effects.


def convolve(img, kernel):
    return ndimage.convolve(img, kernel, mode='constant', cval=0.0)


def grayscale(img):
    # Dot product of (h, w, 3) matrix with 3-vector broadcasts the
    # 3-vector to be applied over all pixels in higher dimensions.
    return img.dot([0.299, 0.587, 0.114])


# Rotate every r*r subimage right by 90 degrees.

def rotate_mosaic(img, r=16):
    (h, w, *b) = img.shape
    return np.vstack(    # Stack the rotated rows vertically.
             [np.hstack(  # Stack the results of same row horizontally.
              [np.rot90(img[y:y+r, x:x+r, :])   # Rotate subimage.
               for x in range(0, w, r)])  # Over all columns.
              for y in range(0, h, r)  # Over all rows.
              ]
    )

# Many other ways to perform edge detection also exist.


Faler = [
           [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]],
           [[1, 1, 1], [0, 0, 0], [-1, -1, -1]],
           [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
           [[0, 1, 0], [-1, 0, 1], [0, -1, 0]]
      ]


def detect_edges(image, masks=None):
    if masks is None:
        masks = Faler
    edges = np.zeros(image.shape)
    for mask in masks:
        edges = np.maximum(ndimage.convolve(image, mask), edges)
    return edges


# Floyd-Steinberg dithering could be generalized to any colour space and
# palette of possible colours to use. Proper implementation would also
# apply gamma correction instead of blithely assuming linear brightness.
# https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

def floyd_steinberg(img, thres=0.7):
    (h, w, *b) = img.shape
    result = np.zeros(shape=(h, w), dtype='float')
    for y in range(h):
        for x in range(w):
            # How bright the pixel [y][x] should be.
            bt = float(img[y][x]) / 255 + result[y][x]
            actual = 1.0 if bt > thres else 0.0
            result[y][x] = actual
            error = bt - actual  # negate this for a fun effect
            if x < w - 1:
                result[y][x+1] += 7 * error / 16
            if y < h - 1:
                if x > 0:
                    result[y+1][x-1] += 3 * error / 16
                result[y+1][x] += 5 * error / 16
                if x < w - 1:
                    result[y+1][x+1] += error / 16
    return result


# Probabilistic dithering is also possible for black and white images.
# Just for fun, we also show how to make random numbers less "streaky"
# while still maintaining the essential parts of their randomness.

def probabilistic_dither(img, thres=0.7):
    (h, w, *b) = img.shape
    result = np.zeros(shape=(h, w), dtype='float')
    # Twenty numbers to choose from randomly.
    nums = np.linspace(-.2, .2, num=20)
    for y in range(h):
        # Dither each line separately from others.
        idx, acc = 0, 0
        for x in range(w):
            if idx == 0:
                np.random.shuffle(nums)
            acc += float(img[y][x]) / 256 + nums[idx]
            # Once accumulation reaches 1.0, make that pixel white.
            if acc > thres:
                result[y][x] = 1.0
                acc -= 0.7
            idx = (idx + 1) % 20
    return result


# Using matplotlib to display the image in a figure window.

def display(img, info, cmap='gray'):
    print(info)
    (h, w, *b) = img.shape
    # Create a new figure window without the axis lines.
    plt.figure(figsize=((w/80), (h/80)), dpi=80)
    plt.axis('off')
    # Render the image into the figure.
    plt.imshow(img, cmap=cmap)
    # Display that figure.
    plt.show()


if __name__ == "__main__":
    forig = misc.face()
    display(forig, "Original image.", cmap="BrBG")
    print(f"Image dimensions are: {str(forig.shape)}")

    # Images are arrays. All numpy array operations are fair game.

    fgray = grayscale(forig)
    display(fgray, "Converted to grayscale.")

    ffs = floyd_steinberg(fgray)
    display(ffs, "Floyd-Steinberg dithering to binary black and white.")

    fpd = probabilistic_dither(fgray)
    display(fpd, "Probabilistic dithering to binary black and white.")

    f3 = convolve(fgray, np.ones((15, 15)) / (15*15))
    display(f3, "Blurring as special case of convolution.")

    f4 = detect_edges(fgray, Faler)
    display(f4, "Edge detection as maximum of Faler convolutions.")

    f5 = rotate_mosaic(forig, r=64)
    display(f5, "Rotating each 64*64 subarray.")

    # Numpy arrays already know how to sort their elements with respect
    # to any gven dimension. Pixel sorting is a fun little algorithm
    # that, when combined with various other image processing algorithms,
    # produce artistic results.

    f6 = np.sort(forig, 1)
    display(f6, "Pixel sorting rows.")

    f7 = np.sort(forig, 0)
    display(f7, "Pixel sorting columns.")

    # http://www.degeneratestate.org/posts/2016/Oct/23/image-processing-with-numpy/
    # Nice little page with illustrations of using numpy for image processing.
    f8 = ndimage.median_filter(fgray, size=(15, 15))
    display(f8, "Median filter of 15*15 rectangle.")

    # A wavy kind of transformation of pixel coordinates.
    def trans(c):
        (cy, cx) = c[0], c[1]
        return (cy + 10*np.sin(.17*cy-.03*cx),
                cx + 12*(np.cos(-.06*cx) - np.sin(.12*cy)),
                c[2])

    import cmath
    import math

    # Transform point (x, y) of a spiral back into original image.

    def spiral(pt, repx=5, repy=1, pull=8, w=1024, h=768):
        (py, px, b) = pt
        dv = (px - w // 2, py - h // 2)
        if abs(dv[0]) + abs(dv[1]) < 2:
            return py, px, pt[2]
        r, phi = cmath.polar(dv[0] + dv[1] * 1j)
        r = math.log(r, pull)
        xf = repx * phi / math.tau
        xx = (xf - math.floor(xf)) * w
        yf = abs(r - repy * phi / math.tau)
        yy = (yf - math.floor(yf)) * h
        return yy, xx, pt[2]

    f9 = ndimage.geometric_transform(forig, trans)
    display(f9, "A geometric transformation.")

    # The spiral transformation needs to know the dimensions of
    # original image to be able to operate.

    ekw = {'w': forig.shape[1], 'h': forig.shape[0]}
    f10 = ndimage.geometric_transform(forig, spiral,
                                      extra_keywords=ekw)
    display(f10, "Another geometric transformation.")

    print("Contour plot of the image treated as grayscale array.")
    plt.figure(figsize=(12, 10))
    plt.contour(fgray[::-1, :], cmap='plasma')
    plt.show()

    # More at https://docs.scipy.org/doc/scipy/reference/ndimage.html
    print("And that's that about that!")
