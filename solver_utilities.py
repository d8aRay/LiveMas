import pandas as pd
import time

def get_price(items, order):
    if not order:
        return 0
    s = 0
    for item in order:
        s += items[item]
    return s
    
def get_item_dict(path_to_csv):
    df = pd.read_csv(path_to_csv)
    df = df.set_index('product')
    df = df[df['price'] > 0.0]
    items = df['price'].to_dict()
    return items
    
def time_it(fn, args):
    start = time.time()
    ans = fn(*args)
    print(f'Process took {time.time() - start: .2f} seconds.')
    return ans
    