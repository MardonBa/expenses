import unittest
import data_changes as dc
import pandas as pd
import os
from datetime import datetime

class TestBasicFunctions(unittest.TestCase):

    def test_save_data(self):
        ## The save_data() function should take in a DataFrame and then save it as a csv file
        test_input = pd.DataFrame({'A': [1, 5], 'B': [3, 4]})
        dc.save_data(test_input, filename='./budget_data_test.csv')
        self.assertTrue(os.path.isfile('./budget_data_test.csv'))## Checks to see that the file exists
        os.remove('./budget_data_test.csv') ## Removes the file once done
    
    def test_help(self):
        real_output = dc.help()
        expected_output = "\n \
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
close: saves the updates if you haven't already, and ends the program \n"
        self.assertEqual(real_output, expected_output)

class TestCalculateNewBalance(unittest.TestCase):

    def test_len_one_type_withdrawal(self):
        input_data = [300, 'withdrawal', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 1
        input_previous_balance = None
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = -300
        self.assertEqual(real_output, expected_output)

    def test_len_one_type_deposit(self):
        input_data = [300, 'deposit', 'paycheck', 'paycheck', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 1
        input_previous_balance = None
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = 300
        self.assertEqual(real_output, expected_output)
    
    def test_len_zero(self):
        input_data = [300, 'withdrawal', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 0
        input_previous_balance = None
        self.assertRaises(TypeError, lambda: dc.calculate_new_balance(input_data, input_len, input_previous_balance))
        ## Lambda to fix the problem of the function raising the error before assertRaises can be evaluated

    def test_withdrawal_into_negative(self):
        input_data = [300, 'withdrawal', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 4
        input_previous_balance = 100
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = -200
        self.assertEqual(real_output, expected_output)

    def test_withdrawal_still_positive(self):
        input_data = [500, 'withdrawal', 'car payment', 'bills', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 4
        input_previous_balance = 700
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = 200
        self.assertEqual(real_output, expected_output)

    def test_deposit_negative(self):
        input_data = [300, 'deposit', 'paycheck', 'paycheck', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 4
        input_previous_balance = -500
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = -200
        self.assertEqual(real_output, expected_output)

    def test_deposit_positive(self):
        input_data = [300, 'deposit', 'paycheck', 'paycheck', datetime.strptime('8/30/2023', '%m/%d/%Y')]
        input_len = 4
        input_previous_balance = 100
        real_output = dc.calculate_new_balance(input_data, input_len, input_previous_balance)
        expected_output = 400
        self.assertEqual(real_output, expected_output)

class TestAddNewEntry(unittest.TestCase):

    def __init__(self):
        self._input_df = pd.DataFrame({ \
                'amount': [300, 400, 600, 100], \
                'withdrawal/deposit': ['deposit', 'withdrawal', 'deposit', 'deposit'], \
                'description': ['first deposit', 'income tax', 'paycheck', 'Ellie paid me for dinner'], \
                'category': ['paycheck', 'taxes', 'paycheck', 'leisure'], \
                'date': [str(datetime.strptime('9/2/2023', '%m/%d/%Y')), str(datetime.strptime('9/3/2023', '%m/%d/%Y')), str(datetime.strptime('9/4/2023', '%m/%d/%Y')), str(datetime.strptime('9/5/2023', '%m/%d/%Y'))], \
                'new balance': [300, -100, 500, 600]
                })
        self._input_default_categories = ["bills", "taxes", "paycheck", "leisure", "business"]
        self._input_custom_and_default_categories = ["bills", "taxes", "paycheck", "leisure", "business", "school", "food", "cleaning supplies"]

    def test_add_to_end_false(self):
        input_add_to_end = False

    def test_add_to_end_true(self):
        input_add_to_end = True

    def test_updates_balance_correctly(self): ## For add_to_end=True, checks to see if the new_balances column of the returned DataFrame are updated to the correct values
        input_add_to_end = True

    def test_has_custom_columns(self):
        input_add_to_end = False

unittest.main(verbosity=2)