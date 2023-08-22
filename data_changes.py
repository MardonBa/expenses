import time
from copy import deepcopy

def save_data(df): ## Saves the updated dataframe to the budget_data.csv file
    ## Runs on user request, or on terminal close
    df.to_csv('./budget_data.csv', index=False)
    print('Changes saved!')

def help():
    print("\n \
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
          
def calculate_new_balance(data, df_len, previous_row_balance):
    ## doesnt work
    print(data)
    transaction_type = data[1] ## withdrawal/deposit value is in the second position of the data list (index 1)
    if transaction_type.lower() == 'withdrawal': ## Uses lowercase in case the user capitalized any letters
        if df_len == 0:
            new_balance = -data[0] ## Since this is the first entry, set new balance to the amount removed
            ## The amount removed is stored in the first entry of the data list
            ## Negative since it is a removal
        else:
            new_balance = previous_row_balance - data[0] ## Subtract the amount of the latest withdrawal (stored in the data list) from the total amount in the previous entry
    else: ## if the transaction type was a deposit
        if df_len == 0:
            new_balance = data[0] ## Since this is the first entry, set new balance to the amount added
            ## The amount added is stored in the first entry of the data list
        else:
            new_balance = previous_row_balance + data[0] ## Add the amount of the latest deposit (stored in the data list) to the total amount in the previous entry

    return new_balance


from datetime import datetime
def add_new_entry(df, categories, add_to_end=True, index_to_add=None):
    print("dont forget, dates should be in the format MM/DD/YYYY")
    ## First, prompt the user for the information relevant to each column, and store that information in a list, to be added to the DataFrame
    ## This way, custom columns are included
    data = []
    index_to_add = int(index_to_add)

    for column in df.columns:
        ## The following code is written before asking for a user-inputed value because it should be calculated seperately from user input
        ## If new balance is the last column, the for loop is essentially broken out of, since continue cannot continue to an iteration that does not exist
        ## Use continue instead of break because the user can add custom columns, which would come after the new balance column
        if column == 'new balance': ## Calculates the new balance
            if add_to_end:
                previous_row_balance = df.at[len(df) - 1, 'new balance'] 
                data.append(calculate_new_balance(data, len(df), previous_row_balance)) ## Adds the calculated balance to the data
                continue ## Move on to the next iteration (necessary for if the user has created custom column)
            else:
                new_balances = [] ## Used to set the DataFrame column to this new list
                for i in range(len(df)): ## Iterate through the DataFrame
                    if i < index_to_add: ## No need to change the values that come before the edited row, so just add those values to new_balances
                        new_balances.append(df.at[i, 'new balance'])
                    else:
                        previous_row_balance = df.at[i - 1, 'new balance'] ## Uses i - 1 to find the previous balance of the row before it for making changes
                        new_balances.append(calculate_new_balance(data, len(df), previous_row_balance))
                        if i == index_to_add:
                            data.append(new_balances[-1]) ## Add the last value in the new balances list to the data list so that data maintains the corect length
                df["new balance"] = new_balances ## Updates dataframe
                continue ## Move on to next iteration


        elif column == 'category':
            user_input = input(f"What category would you like to track this input as? {categories}: ")
            if user_input not in categories:
                ## Potentially add a recursive case to continue asking
                user_input = input(f"Seems like you have a typo! What category would you like to track this input as? {categories}: ") 
            data.append(user_input)
            continue


        user_input = input(f"What value would you like to set for the {column} column? ")

        if column == 'withdrawal/deposit':
            if user_input.lower() != 'withdrawal' and user_input.lower() != 'deposit':
                ## Checks to see if the user has given correct spelling
                ## If not, ask for an answer again
                ## Maybe add some sort of recursive case to continue asking if the user repeatedly enters a typo
                user_input = input("It seems like you made a typo! Please re-enter whether the transaction is a withdrawal or a deposit. Don't mess up this time! ")

        elif column == 'date':
            try:
                user_input = datetime.strptime(user_input, '%m/%d/%Y')
            except:
                print("Sorry, it seems like you entered the date in the wrong format. Please start again")
            ## converted to a datetime object to easily add-subtract dates to find the difference in time
        
        try: ## Changes a numerical input to a float if possible
            user_input = float(user_input)
        except:
            pass

        
        data.append(user_input)
    
    if add_to_end: ## Adds the acquired data to the end of the dataframe
        df.iloc[len(df)] = data
    else: ## Adds the acquired data to a specified index

        df.iloc[index_to_add] = data

    return df


def create_new_column(df, col_name, default_value=0):
    ## Takes in a DataFrame, the name of a new column, and optionally a default value for the values of the column
    df[col_name] = [default_value for i in range(len(df))]

def edit_row(df, categories):
    knows_index = input("Do you know what the index of the row you want to edit is? (Y/n): ")
    knows_index = True if knows_index == "Y" else False ## Changes the user-inputted value to a boolean for ease of use

    if knows_index:
        index = input("Please enter the index of the row you want to edit") ## Used to pass into add_new_entry() as the index_to_add parameter
    else:
        known_values = [] ## Used to store the values the user inputs
        for column in df.columns:
            value = input('What is the value of "' + column + '" in the row that you want to edit? (press Enter if you dont know) ')
            try:
                value = float(value) ## Changes the value to a float instead of a string if possible/necessary
            except:
                pass ## Do nothing
            known_values.append(value)

        counter = 0
        for value in known_values:
            if value == "":
                counter += 1
        if counter == len(known_values):
            print("Sorry, you have to give some information to go off of in order to locate the row you want to edit")
            return ## Ends the function, since the user doesn't know any values, and doesn't know the index of the row
        
        potential_row_indexes = []
        items_to_remove = [] ## Tracks what to remove from potential indexes
        for j in range(len(df)): ## Iterates over each column in the dataframe
            first_iter = True
            for i in range(len(df.columns)): ## Iterates over each row in the dataframe
                if not first_iter: ## Checks to see if this is the first iteration
                    if known_values[i] == df.iat[j, i] and known_values[i] != "": ## If not, check to see if the known value for the given column is the in the cell being checked
                        if known_values[i] in potential_row_indexes: ## Since this is no longer the first iteration, check to see if the value being checked is already in the array
                            pass
                        else: ## If the known value for a given column is not in the potential row indexes, remove it, since it cannot be the row the user is looking for
                            ##potential_row_indexes.remove(potential_row_indexes[i])
                            items_to_remove.append(j)
                elif known_values[i] == df.iat[j, i] and known_values[i] != "": ## check to see if the known value for the given column is the in the cell being checked
                    potential_row_indexes.append(j) ## If it is, append that row index to the list of potential row indexes
                    first_iter = False ## Changes to False after the first iteration
                    ## first_iter is indented so that it doesn't change until a known value is presented, not an empty string, so that the program can have something to check off of for future iterations
        for item in items_to_remove:
            potential_row_indexes.remove(item) ## Removes the invalid rows from the list of potential rows
        
        print(f"potential row indexes: {potential_row_indexes}") ## Test

        for index in potential_row_indexes:
            print(\
f"Is the following the row that you are looking for? \n\n \
{[df.loc[index]]} \n\n \
If so, enter {index} when prompted")
            time.sleep(3)
            
        index = input("Please enter the number given that corresponds to the row you wish to edit: ")
    
    print("Follow the instructions to edit all the relevant values for this row")
    try:
        add_new_entry(df, categories, add_to_end=False, index_to_add=index) ## Prompts the user for the new information for the row
    except Exception as e:
        print(f"Error: {e}")
        print('Something went wrong. Please try again!')
