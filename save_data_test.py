import unittest
import data_changes as dc
import pandas as pd
import os
from datetime import datetime

class TestBasicFunctions(unittest.TestCase):

    def test_save_data(self):
        ## The save_data() function should take in a DataFrame and then save it as a csv file
        df = pd.DataFrame({'A': [1, 5], 'B': [3, 4]})
        dc.save_data(df, filename='./budget_data_test.csv')
        self.assertTrue(os.path.isfile('./budget_data_test.csv'))## Checks to see that the file exists
        os.remove('./budget_data_test.csv') ## Removes the file once done
    
    def test_help(self):
        self.assertEqual(dc.help(), "\n \
Here is a list of user commands: \n\n \
help: this command! \n\n \
save changes: saves all changes made \n\n \
add new entry: will prompt you for the information relevant to making a new entry \n\n \
make a new column: used to make a new column in the tracker. will set the values in each row to a default of None, but can be changed \n \
remove column: prompts you for which column to remove \n\n \
create a new category: makes a new budget category \n\n \
remove category: Prompts you to select which category you want to remove \n\n \
see current categories: shows you what the current categories are \n\n \
edit row: will prompt you for what row (if you know), otherwise for the data in that row \n\n \
remove row: will prompt you for what row (if you know), otherwise for the data in that row\n\n \
edit cell: will prompt you for what row and column (if you know), otherwise for the data in that row, as well as the column you wish to change \n\n \
set a category budget: will prompt you for what category you wish to add a budget to, then what you would like the budget to be \n\n \
set total budget: will ask you what you want your total budget to be \n\n \
view spending graph: will ask you what time period of spending you want to see (pre-set or custom time period). Option to show the total spending budget along with the spending data \n \
view deposit graph: will ask you what time period of deposits you want to see (pre-set or custom time period) \n\n \
view total balance graph: will ask you what time period of total balance you want to see (pre-set or custom time period) \n\n \
view spending graph by category: will ask you what time period of spending you want to see (pre-set or custom time period), as well as what category/categories you wish to see. Option to display a line with the budget for that category/categories\n\n \
close: saves the updates if you haven't already, and ends the program \n")

class TestCalculateNewBalance(unittest.TestCase):

    def test_len_one_type_withdrawal(self):
        dummy_data = [300, 'withdrawal', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        dummy_len = 1
        dummy_previous_balance = None
        self.assertEqual(dc.calculate_new_balance(dummy_data, dummy_len, dummy_previous_balance), -300)
    def test_len_one_type_deposit(self):
        dummy_data = [300, 'deposit', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        dummy_len = 1
        dummy_previous_balance = None
        self.assertEqual(dc.calculate_new_balance(dummy_data, dummy_len, dummy_previous_balance), 300)
    
    def test_len_zero(self):
        dummy_data = [300, 'deposit', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        dummy_len = 0
        dummy_previous_balance = None
        self.assertRaises(TypeError, lambda: dc.calculate_new_balance(dummy_data, dummy_len, dummy_previous_balance))
        ## Lambda to fix the problem of the function raising the error before assertRaises can be evaluated

unittest.main(verbosity=2)