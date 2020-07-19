import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sci
import scipy.integrate as scint
import scipy.optimize as sco

a = np.array([1.2, 5.5, -4.3, 9.1, 0.2, -3.3], dtype='double')
print(f"a is now:\n{a!s}")
a = a.reshape((2, 3))
print(f"a is now:\n{a!s}")
a = a.reshape(6)
print(f"a is now:\n{a!s}")

# Unlike Python lists, slicing and views share underlying data.

b = a[2:4]
print(f"b is now:\n{b!s}")
a[2] = 2.54
print(f"b is now:\n{b!s}")

# Arithmetic works differently for numpy arrays and Python lists.

pl = [1, 2, 3]
print(f"Python list addition: {pl + pl}")
print(f"Python list multiplication: {pl * 3}")
na = np.array([1, 2, 3])
print(f"Numpy array addition: {na + na}")
print(f"Numpy array multiplication: {na * 3}")

# Ufuncs apply separately to each element of the array. This
# eliminates the need for us to write that loop explicitly. Often
# we do not wish to use list comprehension, since that could not
# operate in a numpy array in place, which might be important if
# the array is humongous.

a = a + np.cos(a)
print(f"a is now:\n{a!s}")

# When combinining matrices of different ranks, the smaller one
# is automatically broadcast into higher dimensions so that the
# shapes of the two matrices are compatible for that operation.

c = np.array([1, 2, 3, 4, 5, 6])
c = c.reshape((2, 3))        # shape (2, 3)
d = np.array([1, 2, 3])      # broadcast into (2, 3)
print("c + d equals:", (c + d))

# Cherry picking elements by indexing with a truth-valued array.

v = a > 3  # A truth-valued array from elementwise comparisons
print(f"v is now: {v}")
print(f"a[v] is: {a[v]}")

# Then, onto scipy and its basic functions copied from MATLAB.

# The lower resolution data points from interval [0, 10].
x = np.linspace(0, 10, 10)
# The higher resolution data points on same interval [0, 10].
xx = np.linspace(0, 10, 50)

# Ufuncs again apply to all elements of the array.
y = 3.2 * np.sin(x*1.4) + .35*x*x

# Interpolation of values between given data points.

# Create a function to represente the interpolation.
f = sci.interp1d(x, y, kind='cubic')
# Apply that function to elements on higher resolution.
yy = f(xx)

plt.figure(1)
# Classic MATLAB plotting syntax, two plots in the same graph.
# Good thing that Python functions can handle any number of
# any type of arguments given to them with *args and **kwargs.
plt.plot(x, y, 'o', xx, yy, '-')
plt.show()


# Scipy offers a host of numerical integration functions.

# First, let's make up a function to integrate.
def f(x):
    return 3.3*x*x - np.exp(x-3)*4.2*x + 1.5*np.cos(x)


# Integration, given a function f that works in any single point.
print(f"Quad: {scint.quad(f, -5, 5)[0]:.6f}")
print(f"Romberg: {scint.romberg(f, -5, 5):.6f}")
print(f"Fixed quad: {scint.fixed_quad(f, -5, 5)[0]:.6f}")

# Integration, given a fixed set of samples of values of f.
xx = np.linspace(-5, 5, 100)
yy = f(xx)
print(f"Trapezoidal: {scint.trapz(yy, x=xx):.6f}")
print(f"Simpson: {scint.simps(yy, x=xx):.6f}")

# Last, the minimization of some function f. (To maximize f,
# you can always simply minimize -f.)

result = sco.minimize(f, 0, method='BFGS')
print(f"Function is minimized at x = {result.x[0]:.5f}.")
