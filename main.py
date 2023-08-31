import pandas as pd
import json
import data_changes

## Check to see if the CSV file exists. If it does, create a dataframe from it. If not, create a new empty dataframe
import os
csv_exists = os.path.exists("./budget_data.csv")

if csv_exists: ## Loads the data if the file exists
    budget_df = pd.read_csv("./budget_data.csv")
else: ## Create a new DataFrame if the file hasn't been created yet
    budget_df = pd.DataFrame(columns=["amount", "withdrawal/deposit", "description", "category", "date", "new balance"])


with open("./misc_data.json", "r") as openfile:
    json_object = json.load(openfile)
    ## Gets the data stored in the json file and stores it as a dictionary

categories = json_object["categories"]

print(budget_df) ## Test

message = "Hi there! What would you like to do today? (Enter help to see a list of commands): "

while True: ## Event loop
    action = input(message)
    message = "Is there anything else you would like to do? (Enter help to see a list of commands): " ## Changes the message for the rest of the program's run

    ## series of if-elif statements for every action outlined in the help() function
    ## if there is a typo, the final else statement will run, saying that the user likely made a typo and to enter their command again
    if action  == 'help':
        print(data_changes.help()) ## Display the help
    
    elif action == 'save changes':
        data_changes.save_data(budget_df)

    elif action == 'add new entry':
        try: 
            budget_df = data_changes.add_new_entry(budget_df, categories)
        except Exception as e:
            print(e)
            print('Something went wrong. Please try again!')

    elif action == 'make a new column':
        column_name = input("What would you like to name the new column? ")
        default_value = input("Would you like to set a value for all previous tracker entries? (press enter to skip): ")
        if default_value != "":
            data_changes.create_new_column(budget_df, column_name, default_value)
        else:
            data_changes.create_new_column(budget_df, column_name)

    elif action == "remove column":
        print(f"columns: {[budget_df.columns]}")
        user_input = input("Which column would you like to remove? ")
        budget_df.drop(user_input, axis=1, inplace=True)
        print(f"Successfully removed the {user_input} column")
    
    elif action == 'create a new category': ## Gets the name of the new category and adds it to the list of categories
        user_input = input("What would you like the name of your new category to be? ")
        categories.append(user_input)
        print(categories)
        json_object["categories"] = categories ## Changes only that part of the json object
        with open("./misc_data.json", "w") as outfile: ## writes to the json file
            json.dump(json_object, outfile)
            print('done')

    elif action == 'remove category':
        print(f"categories: {categories}")
        user_input = input("Which category would you like to remove? ")
        categories.remove(user_input) ## Removes the category from the categories lsit
        json_object["categories"] = categories ## Changes only that part of the json object
        with open("./misc_data.json", "w") as outfile: ## writes to the json file
            json.dump(json_object, outfile)
            print('done')

    elif action == 'see current categories': ## Shows the user what categories there currently are
        print(categories)

    elif action == 'edit row':
        data_changes.edit_row(budget_df, categories)

    elif action == 'close':
        data_changes.save_data(budget_df) ## Save the changes
        break ## Breaks out of the while loop, which essentially ends the code
    
    else:
        print("You probably made a typo! Re-enter what you wish to do when you are prompted again.")



print("close the terminal or run the script again")