#Contributed Jan 1, 2020
#quick implementation of a Monte Carlo solver
from random import randint

#Helper function to get the price of items in a list
def get_price(items, order):
    if not order:
        return 0
    s = 0
    for item in order:
        s += items[item]
    return s

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
        total = get_price(items, order)
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

def main():
    import argparse
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    from tqdm import tqdm
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_amount', default=20.0, type=float, help='Max amount to spend')
    parser.add_argument('--num_trials', default=100, type=int, help='Number of trials')
    parser.add_argument('--csv_path', default=None, type=str, help='Path of input csv')
    
    args = parser.parse_args()
    
    if not args.csv_path:
        from random import triangular
        items = {i: int(triangular(.50, 7.99, 4.00) * 100) / 100 for i in range(35)}
    else:
        import pandas as pd
        df = pd.read_csv(args.csv_path)
        df = df.set_index('product')
        items = df['price'].to_dict()
    orders = list()
    prices = list()
    for i in tqdm(range(args.num_trials)):
        orders.append(indecisive_buyer(items, args.max_amount))
        prices.append(get_price(items, orders[-1]))
    winning_index = np.argmax(prices)
    winning_order = orders[winning_index]
    print(winning_order)
    sns.distplot(prices)
    plt.xlabel('Money spent ($)')
    plt.title(f'Distribution of orders n:{args.num_trials}, target:{args.max_amount}')
    plt.savefig("order_simulation.pdf", dpi=150)
if __name__ == '__main__':
    main()