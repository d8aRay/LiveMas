# LiveMas
 Taco Bell Optimizer


## menu_scrape.py
menu_scrape.py scrapes the taco bell website for the menu prices/calories

### Dependencies: 
        -Requests
        -bs4

### ToDo
missing calories for all items

## live_mas.py        
live_mas.py will maximize the total spend due against a budget constraint and
taxes.  

### Dependencies 
    -Pandas
    -Pulp

### ToDo
    -user input for budget
    -user input for item limit (and work around "no limit")
    -add a calorie constraint
    -add product categories
    -    allow user to prioritize categories and set category dependent item limits
    -add tax dictionary and allow user to input state for tax accuracy. 