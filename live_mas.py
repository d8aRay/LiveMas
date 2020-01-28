# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 21:37:53 2020

@author: ray.edwards
"""

import pandas as pd
import pulp
import re

def read_menu(): 
    menu = {}
    live_mas = pd.read_csv('live_mas.csv')
    menu['food_items'] = list(live_mas['product'])
    food_items = menu['food_items']
    menu['prices'] = dict(zip(food_items, live_mas['price']))
    menu['calories'] = dict(zip(food_items,live_mas['calories']))
    menu['categories'] = set(live_mas['category'])
    menu['items_by_category'] = dict(zip(food_items, live_mas['category']))
    return menu

def maximize_spend(budget=9.42, item_limit=1, calorie_limit=0, tax=.04):
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
    if calorie_limit>0: 
        problem += pulp.lpSum(calories[i]*food_var[i] for i in food_items) <= calorie_limit, "Calorie Constraint"
    #solve the problem
    problem.solve()
    return problem

def print_order_items(problem):
    for v in problem.variables():
        if v.varValue >0:
             print(v.name[1:], 'qty =', v.varValue)
            
#print("Status", pulp.LpStatus[spend.status])

def parse_calories(menu_calories): 
    calorie_dict = {}
    for k, v in menu_calories.items():
        try: 
            calorie_string = re.split('[-\s]', v)
            calorie_range = [x for x in calorie_string if not any(stop in x for stop in ['Cal', 'Per', 'Item'])]
            upper = max(calorie_range)
            calorie_dict[k] = int(upper)
        except(TypeError, ValueError): 
            if k == 'Taco and Burrito Party Pack': 
                calorie_dict[k] = 2060
    return calorie_dict


menu = read_menu()
calories = parse_calories(menu['calories'])
items_by_category = menu['items_by_category']
categories = menu['categories']

food_items, prices = menu['food_items'], menu['prices']
spend = maximize_spend()
print('You can spend $'+str(spend.objective.value())+' on:')
print_order_items(spend)