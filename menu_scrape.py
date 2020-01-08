# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 21:37:53 2020

@author: ray.edwards
"""

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
taco_bell= r'https://www.tacobell.com/food/'
menu_pages = ['deals-and-combos'
              , 'specialties'
              , 'tacos'
              , 'burritos'
              , 'quesadillas'
              , 'nachos'
              , 'cravings-value-menu'
              , 'sweets'
              , 'sides'
              , 'drinks'
              , 'power-menu'
              , 'party-packs'
              , 'vegetarian'
              , 'breakfast'
              ]
products = {}
for page in menu_pages: 
    print(page)
    url = taco_bell+page
    menu_request = requests.get(url, headers=headers)
    soup = BeautifulSoup(menu_request.content)
    product_cards = soup.find_all('div', class_ = 'product-card')
    for i in range(0, len(product_cards)):
        print(i)
        try:
            product_info = product_cards[i].find('div', class_ = 'product-details')
            product_name = product_info.find('div', class_ = 'product-name')
            a = product_name.find('a')
            name = a.text
            print(name)
        except:
            pass
        try:
            product_price = product_info.find('div', class_ = 'product-price')
            span = product_price.find('span', class_ = '')
            price = span.text
            print(price)
        except:
            try: 
                product_price = product_info.find('div', class_ = 'product-price')
                span = product_price.find('span', class_ = 'js-price-value')
                price = span.text
                print(price)
            except:
                price = ''
        try:
            product_calories = product_info.find('div', class_='product-calorie')
            calories = product_calories.text
            print(calories)
        except: 
            calories = '' 
        products[name] = {'price' : price
                        , 'calories' : calories
                        }
import pandas as pd
live_mas = pd.DataFrame.from_dict(products)
live_masT = live_mas.T
live_masT['product'] = live_masT.index
live_mas = live_masT
live_mas.to_csv('live_mas.csv', index=False)
