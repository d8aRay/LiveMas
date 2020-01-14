import matplotlib.pyplot as plt
import seaborn as sns
import solver_utilities as util
import solvers
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', default=None, type=str, required=True, help='Path of input csv')
    parser.add_argument('--budget', default=None, type=float, required=True, help='Maximum budget')
    args = parser.parse_args()
    
    items = util.get_item_dict(args.csv_path)
    fxn_args = [items, args.budget]
    print('CVXPY')
    cvxpy_result = util.time_it(solvers.cvxpy_approach, fxn_args)
    print(f'\tcvxpy results:\n\t\tPrice: {util.get_price(items, cvxpy_result):.2f}\n\t\t{", ".join(cvxpy_result)}')
    print('Monte Carlo')
    random_result = util.time_it(solvers.random_approach, fxn_args)
    print(f'\tcvxpy results:\n\t\tPrice: {util.get_price(items, random_result):.2f}\n\t\t{", ".join(random_result)}')
    
    
if __name__ == '__main__':
    main()