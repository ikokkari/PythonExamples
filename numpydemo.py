# Updated for NumPy 2.0 and SciPy 1.14, July 31, 2024.

import numpy as np
import scipy.integrate
import scipy.optimize
import scipy.interpolate
import matplotlib.pyplot as plt

# Numpy has its own random number generators.

rng = np.random.default_rng()

# Ordinary Python list for comparison of operations.
a_p = [42, 99, 17, 0, -1]

# Numpy arrays can be created in many ways.
a_n = np.array(a_p, dtype=np.int16)
b_n = np.arange(-5, 6) ** 2
c_n = rng.poisson(5, 15)

print(f"a_n is {a_n} with shape {a_n.shape}.")
print(f"b_n is {b_n} with shape {b_n.shape}.")
print(f"c_n is {c_n} with shape {c_n.shape}.")
print(f"Mean, median, and variance of c_n are {np.mean(c_n)}, {np.median(c_n)} and {np.var(c_n)}.")

# Numpy arrays can be reshaped, and they still have the same elements.

c_n.shape = (3, 5)
print(f"After changing shape, c_n now equals {c_n}.")
print(f"Mean, median, and variance of c_n are {np.mean(c_n)}, {np.median(c_n)} and {np.var(c_n)}.")

# Numpy array arithmetic is always elementwise.

print(f"a_n + a_n equals {a_n + a_n}.")
print(f"a_p + a_p equals {a_p + a_p}.")
print(f"a_n * 3 equals {a_n * 3}.")
print(f"a_p * 3 equals {a_p * 3}.\n")

# Python list elementwise addition can be done with comprehension and zip.

print(f"a_p + a_p done elementwise equals {[x + y for (x, y) in zip(a_p, a_p)]}.\n")

# Slicing a Numpy array creates a view that shares the underlying data.

d_n = a_n[:3]
d_n[0] = 33
print(f"a_n is {a_n} with shape {a_n.shape}.")
print(f"d_n is {d_n} with shape {d_n.shape}.")

# If you want the data to be separate, you must use method .copy()

e_n = a_n[:3].copy()
e_n[0] = 123
print(f"a_n is {a_n} with shape {a_n.shape}.")
print(f"e_n is {e_n} with shape {e_n.shape}.\n")

# Numpy arrays allow "fancy indexing" with vector of truth values, akin
# to the standard library Python function itertools.compress.

idx = c_n > 5  # Produces a truth-valued array
print(f"Elements of c_n greater than 5 are {c_n[idx]}.")

# An array with floating point values.

f_n = np.linspace(0, np.pi, 20)
print(f"f_n is {f_n} with type {f_n.dtype}.")

# Universal functions are automatically vectorized over the array, so that
# you don't need to write a loop to apply them to every element.

f_n = np.sin(f_n)
print(f"After taking sine, f_n is {f_n} with type {f_n.dtype}.\n")


# Next, we will demonstrate a bit of scipy. Let's define a black box function
# that we will use in integration, optimization and interpolation.

def f(x):
    return np.float_power((np.e + np.cos(10*x)), np.sin(x - np.sqrt(x)))


# Integration of arbitrary black box function.
y = scipy.integrate.quad(f, 0, 10)
print(f"Quadratic numeral integral of f from 0 to 10 equals {y}.")

# Sometimes we only have some sample points.
xs = np.linspace(0, 10, 11) # A good value to create a ruler.
ys = f(xs)  # Ufuncs are vectorized over the entire vector.
y = scipy.integrate.simpson(ys, xs)
print(f"Simpson sample point integral of f from 0 to 10 equals {y}.")

# Finding the minimum of the given black box function.
x_min = scipy.optimize.minimize_scalar(f, bounds=[-5, 5])
print(f"In [-5, 5], f is minimized at {x_min.x}, where it equals {f(x_min.x)}.")

# Last, some interpolation of values from the known sample points.
cubic_spline = scipy.interpolate.CubicSpline(xs, ys)
print(f"Cubic spline says that f(5.5) = {cubic_spline(5.5)}.")
akima = scipy.interpolate.Akima1DInterpolator(xs, ys)
print(f"Akima interpolator says that f(5.5) = {akima(5.5)}.")
print(f"The exact value of f(5.5) = {f(5.5)}.")

# Finish up with flourish with some Matplotlib plotting.
xxs = np.linspace(0, 10, 1001)
plt.figure()
# This is all just straight up Matlab.
plt.plot(xs, f(xs), 'bo', xxs, f(xxs), 'k')
plt.show()
