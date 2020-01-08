# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 21:37:53 2020

@author: ray.edwards
"""

import pandas as pd
import pulp

def read_menu(): 
    live_mas = pd.read_csv('live_mas.csv')
    food_items = list(live_mas['product'])
    prices = dict(zip(food_items, live_mas['price']))
    return food_items, prices

def maximize_spend(budget=9.42, item_limit=1, tax=.04):
    #calculate the afterTax_budget
    afterTax_budget = budget/(1+tax)
    #instantiate the problem
    problem = pulp.LpProblem('LiveMas', pulp.LpMaximize)
    #create decision variables as non-negative integers with a varialbe upper bound
    food_var = pulp.LpVariable.dicts('',
                                food_items,
                                lowBound= 0, 
                                upBound = item_limit,
                                cat='Integer')
    #add the objective function to the problem
    problem += pulp.lpSum([prices[i] * food_var[i] for i in food_items]), "Total Due"
    #add the budget constraint to the problem
    problem += pulp.lpSum([prices[i] * food_var[i] for i in food_items]) <= afterTax_budget, "Budget Constraint"
    #solve the problem
    problem.solve()
    return problem

def print_order_items(problem):
    for v in problem.variables():
        if v.varValue >0:
             print(v.name[1:], 'qty =', v.varValue)
            
#print("Status", pulp.LpStatus[spend.status])

food_items, prices = read_menu()
spend = maximize_spend()
print('You can spend $'+str(spend.objective.value())+' on:')
print_order_items(spend)