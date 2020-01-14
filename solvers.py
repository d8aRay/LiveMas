import cvxpy as cv
import numpy as np
from random import randint
import solver_utilities as util

def cvxpy_approach(items, money):
    items = util.get_item_dict('live_mas.csv')
    price = money * 100
    A = np.diag(np.array(list(items.values())))
    A = 100 * A
    A = A.astype(int)

    ones = np.ones(len(items.values()))

    prices = np.array(list(items.values()))

    x = cv.Variable(len(items.values()), integer=True)
    obj = cv.Maximize(x*A*ones - price)
    constraints = [(x*A*ones <= price), x >= 0]

    prob = cv.Problem(obj, constraints)

    result = prob.solve()

    res = [0 if xi <= .1 else int(round(xi)) for xi in x.value]

    order = list()
    for i in range(len(res)):
        order += [list(items.keys())[i]] * res[i]
        
    return order

def indecisive_buyer(items, money, max_guesses=10):
#Generates an order based on the menu assuming random selection.
#
#Input:     items - dictionary of form {name: price}
#           money - constraint on price
#           max_guesses - Number of guesses before the algorithm gives up
#
#Output:    order - A valid order from the menu with total price <= money

    list_size = len(items.keys())
    total = 0
    order = []
    guesses = 0
    while total < money:
        total = util.get_price(items, order)
        idx = randint(0, list_size - 1)
        i_name = list(items.keys())[idx]
        item = (i_name, items[i_name])
        if item[1] + total < money:
            order.append(item[0])
            guesses = 0
        else:
            guesses += 1
        if guesses > max_guesses:
            break
    return order
    
def random_approach(items, money, iterations=100, max_guesses=10):
    orders = [indecisive_buyer(items, money, max_guesses=max_guesses) for i in range(iterations)]
    prices = [util.get_price(items, o) for o in orders]
    idx = np.argmax(prices)
    return orders[idx]