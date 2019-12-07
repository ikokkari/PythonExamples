# Execute the given trialf a total of n times, giving trialargs
# as its arguments each time, and return the average of the
# answers returned by trialf.

def trial_average(trialf, n, trialargs=[]):
    total = 0
    for i in range(n):
        total += trialf(*trialargs)
    return total / n

import random

# If there are n different coupons, one random coupons inside each
# cereal box, how many boxes do you need to buy to collect all n?

def coupon_collector_trial(n):
    result = [0 for i in range(n)]
    remain = n
    total = 0
    while remain > 0:
        total += 1
        curr = random.randint(0, n-1)
        if result[curr] == 0:
            result[curr] = 1
            remain -= 1
    return total

# Does the randomly generated point from the unit square fall
# inside the unit circle? Used to estimate the value of pi / 4.

def estimate_pi_trial():
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1:
        return 1
    else:
        return 0

# Roll two dice until you get either boxcars (6-6) or snake-eyes (1-1).
# How many rolls do you need to make on average?

def snake_eyes_or_boxcars_trial():
    count = 0
    d1, d2 = 2, 2
    while not ((d1 == 1 and d2 == 1) or (d1 == 6 and d2 == 6)):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        count += 1
    return count

# A snake oil salesman in the old west starts at frontier town 0,
# with a line of towns at integer points on the real line all the
# was for coast to coast far away. After plying his dirty trade in
# town i, he will randomly move east or west to 1, 2, ..., step
# towns over. How long until the salesman accidentally comes back
# to the town that he has previously visited, and gets tarred and
# feathered by the angry citizens who remember him?

def snake_oil_salesman_trial(step):
    visited = set()
    visited.add(0)
    count = 1
    curr = 0
    while(True):
        curr += random.randint(1, step) * random.choice([-1,1])
        if curr in visited:
            return count
        else:
            count += 1
            visited.add(curr)

# Given two functions f1 and f2 assumed to be probability distributions,
# which one gives a bigger value now?
 
def distribution_trial(f1, f2):
    x1 = f1()
    x2 = f2()
    if x1 > x2: return 1
    else: return 0

# In the famous Monty Hall gameshow, follow the strategy of switching.
# What is our expected win rate? It should be 2/3, if theory is correct.

def monty_hall_switching_trial():
    car = random.randint(1, 3)
    guess = random.randint(1, 3)
    if car != guess:
        monty = 6 - car - guess
    else:
        monty = random.choice([[2,3],[1,3],[1,2]][car - 1])
    guess = 6 - guess - monty
    return int(guess == car)

# Starting at time zero, the time to the next random arrival is taken
# from exponential probability distribution with parameter lamb. How
# many arrivals appear before time reaches 1? The discrete distribution
# of integers produced by this process is the useful Poisson distribution. 

def poisson_trial(lamb):
    total = 0
    count = 0
    while total < 1:
        count += 1
        total += random.expovariate(lamb)
    return count - 1

from functools import partial

if __name__ == "__main__":
    print("\nSampling two continuous distributions:")
    f1 = partial(random.normalvariate, 0.5, 0.1)
    f2 = partial(random.betavariate, 2, 3)
    result = trial_average(distribution_trial, 100000, (f1, f2))
    print(f"{result:.4f}")
    print("\nEstimates for coupon collector problem:")
    for n in range(2, 21):
        result = trial_average(coupon_collector_trial, 10000, (n,))
        print(f"To collect {n} coupons, need {result:.1f} boxes on average.")
    print("\nEstimate for pi:")
    for n in range(1, 8):
        result = 4 * trial_average(estimate_pi_trial, 10**n)
        print(f"{n}: {result:.7f}")
    result = trial_average(snake_eyes_or_boxcars_trial, 100000)
    print(f"\nNumber of rolls until snake eyes or boxcars is {result:.1f}.")
    print("\nSnake oil salesman average visited towns:")
    for n in range(2, 20):
        result = trial_average(snake_oil_salesman_trial, 10000, (n,))
        print(f"{n}: {result:.3f}")
    monty = trial_average(monty_hall_switching_trial, 1000000)
    print(f"\nProbability of winning in Monty Hall with switching is {monty:.4f}.")
    pois = trial_average(poisson_trial, 10000, (3,))
    print(f"\nPoisson random process with parameter 3 gives average of {pois:.4f}.")

    # If Anaheim Duckwalks scores 3 goals per game on average, and Vegas Ni-Knights
    # scores n goals per game on average, what percentage of their mutual matches
    # is won by Ni-Knights?

    ducks = [100 * trial_average(distribution_trial, 100000, (
              partial(poisson_trial, n),
              partial(poisson_trial, 3)
          )) for n in range(1, 20)]
    print("\nVegas Ni-Knights vs. Anaheim Duckwalks:")
    for n in range(1, 10):
        print(f"Averaging {n} goals per game, Ni-Knights wins {ducks[n-1]:.1f} per cent of time.")