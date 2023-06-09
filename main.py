import mysql.connector
import functools
###functions needed: functions for all tasks (check balance, deposit, withdraw, create account, delete account, modify account) and create tables for account data.####
current_user = 0
exit = False
exists = False


#### PROBLEM IS WITH THIS
def create_account(connection, new_user, new_pin):
    print('\nCreating an account...\n')
    cursor=connection.cursor()
    addData="INSERT INTO account_table (balance, username, pin) VALUES (%s, %s, %s)"
    #is the problem that it needs to randomly generate an id in 'idaccount'? if so how do I do that??
    account_info = (0, new_user, new_pin)
    cursor.execute(addData, account_info)
    print('\n~ New user created ~\n')
    cursor.close

########

def log_in(connection, user, pin):
    user_valid= validate_user(connection, user)
    if not user_valid:
        print('Sorry, that is an invalid username!')
        return "invalid user"
    else:
        pin_valid = validate_pin(connection, user, pin)
        if not pin_valid:
            print('Sorry, that is not the correct password!')
            return "invalid pin"
        else:
            print('logging in...\n')
            return "valid user"


def validate_user(connection, attempt_user):
    exists = False
    cursor=connection.cursor()
    findUser = "SELECT username FROM account_table WHERE username = %s"
    cursor.execute(findUser, (attempt_user,))
    #not sure if this actually works?
    for item in cursor:
        exists = True
    cursor.close
    return exists
#this is true or false, use that


def validate_pin(connection, active_user, attempt_pin):
    cursor=connection.cursor()
    checkPin = "SELECT pin from account_table WHERE username=%s AND pin=%s"
    credentials = (active_user, attempt_pin)
    cursor.execute(checkPin, credentials)
    # add check for if user is true or false
    exists=False
    for item in cursor:
        exists=True
    # exists=cursor.rowcount > 0
    cursor.close
    return exists


def check_balance(connection, current_user):
    cursor=connection.cursor()
    testQuery= "SELECT balance FROM account_table WHERE username = %s"
    cursor.execute(testQuery, (current_user,))
    for item in cursor:
        balance_tuple = item
    balance_int = functools.reduce(lambda sub, ele: sub * 10 + ele, balance_tuple)
    print(f'Your balance is {balance_int}')
    cursor.close()

def deposit(connection, current_user):
    print(current_user)
    cursor=connection.cursor()
    add = int(input('How much would you like to deposit?\n> '))
    #make this select just specific user's balance, WHERE username == user
    user_tuple = (current_user,)
    # tuple(map(int, current_user.split(', ')))
    balance_query = "SELECT balance FROM account_table WHERE username = %s"

    cursor.execute(balance_query, user_tuple)
    for item in cursor:
        to_add = item
    int_base = functools.reduce(lambda sub, ele: sub * 10 + ele, to_add)
    # cursor.close()
    total = int_base + add
    # execute update statement with total value and same where clause as above, update is another query
    print(f'You deposited {add}, making your new account total:\n >>> {total} <<<')
    upload_deposit = 'UPDATE account_table SET balance = %s WHERE username=%s'
    total_data = (total, current_user)
    cursor.execute(upload_deposit, total_data)
    cursor.close()
    #figure out how to add to the actual value and upload that


def withdraw(connection, current_user):
    cursor=connection.cursor()
    minus = int(input('How much would you like to withdraw?\n> '))
    balance_query = "SELECT balance FROM account_table WHERE username=%s"
    cursor.execute(balance_query, (current_user,))
    for item in cursor:
        to_minus = item
    int_base = functools.reduce(lambda sub, ele: sub * 10 + ele, to_minus)
    if int_base > minus:
        total = int_base - minus
        print(f'You withdrew {minus}, making your new account total:\n >>> {total} <<<')
        # cursor.close()
        upload_deposit = 'UPDATE account_table SET balance = %s WHERE username=%s'
        total_data = (total, current_user,)
        cursor.execute(upload_deposit, total_data)
    else:
        print('You tried to withdraw more than you have in your account!')
    cursor.close

##################

connection = mysql.connector.connect(user = 'root', database = 'elite102project', password = 'Bippyb00')

###################

###     CLI     ###
print('\n\n-=- Welcome to your banking system! - Created using MySQL -=-\nBy Samantha Murphy---\n')
log_or_create = int(input('Enter "1" to log in, and "2" to create a new account\n> '))
if log_or_create == 1:
    attempt_user = input('Enter your username, be sure to get capitalization correct or you must restart the program to try again\n> ')
    #maybe check if this is a real user, or if dont have time just let it crash if there is no user
    attempt_pin = int(input('Enter your pin, be sure to enter only numbers or you must restart the program to try again\n> '))
    #check if user+pin work / log in
    valid_log = log_in(connection, attempt_user, attempt_pin)
    if valid_log == "valid user":
        current_user = attempt_user
    else:
        print('---------------\nSorry, that is not a valid log in! Try restarting the program...\n---------------')
        exit = True
elif log_or_create == 2:
    new_user = input('Create your username:\n> ')
    new_pin = int(input('Create a pin:\n> '))
    create_account(connection, new_user, new_pin)
    print('\n~ Account created... Please log in ~')

    attempt_user = input('Enter your username, be sure to get capitalization correct or you must restart the program to try again\n> ')
    #maybe check if this is a real user, or if dont have time just let it crash if there is no user
    attempt_pin = int(input('Enter your pin, be sure to enter only numbers or you must restart the program to try again\n> '))
    #check if user+pin work / log in
    valid_log = log_in(connection, attempt_user, attempt_pin)
    if valid_log == "valid user":
        current_user = attempt_user
    else:
        print('---------------\nSorry, that is not a valid log in! Try restarting the program...\n---------------')
        exit = True
else:
    print('Please restart the program! Next time enter just "1" or "2"')

##once in:
#
#main menu
while exit==False:
    print(f'\n--==-- Welcome {current_user}! --==--')
    menu_choice = int(input('Select your desired action by typing the number next to it:\n- 1 - Check account balance\n- 2 - Deposit Money\n- 3 - Withdraw Money\n- 4 - Exit\n----------=====----------\n> '))
    if menu_choice == 1:
        #check balance
        print('\nchecking balance...\n')
        check_balance(connection, current_user)
    elif menu_choice == 2:
        #deposit
        deposit(connection, current_user)
        print('')
    elif menu_choice == 3:
        #withdraw
        withdraw(connection, current_user)
        print('')
    elif menu_choice == 4:
        #exit
        print('~ Exiting program... ~')
        exit = True
    else:
        print('\nNext time please follow instructions! Exiting program...\n')
        exit = True

connection.close()