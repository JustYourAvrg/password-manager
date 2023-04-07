import sqlite3
import string
import random
import termcolor
from rich.console import Console
from tabulate import tabulate
import os
import time

console = Console()

# creating the function for the code

def PasswordGen():
    global rand_pass
    punc_question = input('Add Symbols? (Y/N) -> ')
    if punc_question.lower() == "y":
        rand_pass_gen = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    elif punc_question.lower() == "n":
        rand_pass_gen = string.ascii_lowercase + string.ascii_uppercase + string.digits
    else:
        console.print('ERROR PLEASE PROVIDE A CORRECT INPUT', style="bold red")
    
    length = int(input('Length of password -> '))

    rand_pass = ''.join(random.choice(rand_pass_gen) for i in range(length))
    return rand_pass



conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# function to create the database if you haven't already
def CreateDatabase():
    cursor.execute("""
    CREATE TABLE passwords (
        id INTERGER PRIMARY KEY,
        item VARCHAR(100),
        pass VARCHAR(100)
    )
    """)
    return ""
    
# function to add a password to the database
def AddItemToDatabase():
    rand_pass_option = input('Would you like to use a random password as the input? (Y/N) -> ')
    if rand_pass_option.lower() == "y":
        print(PasswordGen())
        item = input('Item -> ')
        passwrd = rand_pass
        cursor.execute("""
        INSERT INTO passwords (item, pass)
        VALUES (?, ?)
        """, (item, passwrd,))
    elif rand_pass_option.lower() == "n":
        item = input('Item -> ')
        passwrd = input('Password -> ')

        cursor.execute("""
        INSERT INTO passwords (item, pass)
        VALUES (?, ?)
        """, (item, passwrd,))
    else:
        console.print("ERROR!", style="bold red")
    
    conn.commit()
    
    return ""

# function to delete a password from the database
def DeleteItemFromDatabase():
    item = input('Password For -> ')

    cursor.execute('SELECT * FROM passwords WHERE item = ?', (item,))
    row = cursor.fetchone() 

    if row:
        confirm = input(f' Delete password for ( {row[1]} ) (Y/N) -> ')

        if confirm.lower() == "y":
            cursor.execute('DELETE FROM passwords WHERE item = ?', (item,))
            conn.commit()
            console.print(f'Deleted Password For [ {row[1]} ]', style="bold cyan")
        else:
            console.print("Canceled Deletion", style="bold red")
    else:
        console.print(f'No Item found', style="bold red")
    
    conn.commit()

    return ""

def ShowPassAll():
    cursor.execute('SELECT * FROM passwords')

    rows = cursor.fetchall()
    headers = ['item', 'pass']

    if rows:
        print(tabulate(rows, headers=headers, tablefmt='fancy_grid'))
    else:
        console.print("No Passwords Found", style="bold red")
    
    return ""

def ShowPassSpecific():
    show_item = input('item -> ')
    cursor.execute('select pass FROM passwords WHERE item = ?', (show_item,))
    
    row = cursor.fetchone()
    
    if row:
        console.print(tabulate([[show_item, row[0]]], headers=['item', 'pass'], tablefmt='fancy_grid'))
    else:
        console.print(f"No password for a {show_item} account has been found", style="bold red")

    return ""

# calling the functions via user input

help = """
[bold cyan]help[/bold cyan] [blink]>>>[/blink] [dim red]brings up this message[/dim red]
[bold cyan]pass-gen[/bold cyan] [blink]>>>[/blink] [dim red]runs the random password generator[/dim red]
[bold cyan]database-creator[/bold cyan] [blink]>>>[/blink] [dim red]creates a password database for the password saver[/dim red]
[bold cyan]pass-deletor[/bold cyan] [blink]>>>[/blink] [dim red]deletes a saved password from the password database[/dim red]
[bold cyan]pass-add[/bold cyan] [blink]>>>[/blink] [dim red]adds a password to the password database[/dim red]
[bold cyan]show-pass-all[/bold cyan] [blink]>>>[/blink] [dim red]shows all saved passwords in the password database[/dim red]
[bold cyan]show-pass[/bold cyan] [blink]>>>[/blink] [dim red]shows a specific saved password in the password database[/dim red]
[bold cyan]cls[/bold cyan] [blink]>>>[/blink] [dim red]clears the screen[/dim red]
[bold cyan]end[/bold cyan] [blink]>>>[/blink] [dim red]ends the script[/dim red]

[bold]Bonus information[/bold]
For the "item" input, enter the name of the website or service for which you are saving the password.
Example: item -> facebook | password -> 123456789
"""

console.print("Type 'help' if you don't know what to do", style="cyan")\
# turn this into a loop eventually

loop = True
while loop == True:
    do_something = input('-> ')

    if do_something.lower() == "help":
        console.print(help)

    elif do_something.lower() == "database-creator":
        print(CreateDatabase())
        console.print('Database created succesfully', style="bold white")

    elif do_something.lower() == "pass-gen":
        print(PasswordGen())

    elif do_something.lower() == "pass-add":
        print(AddItemToDatabase())

    elif do_something.lower() == "pass-deletor":
        print(DeleteItemFromDatabase())
    
    elif do_something.lower() == "end":
        console.print('ENDING SCRIPT', style="bold red")
        loop = False

    elif do_something.lower() == "cls":
        console.print('CLEARING', style="bold white")
        time.sleep(1)
        os.system('cls')

    elif do_something.lower() == "show-pass-all":
        print(ShowPassAll())

    elif do_something.lower() == "show-pass":
        print(ShowPassSpecific())

    else:
        console.print("ERROR - MAKE SURE YOU'RE TYPING THE CORRECT COMMAND IF LOST TYPE 'HELP'", style="bold red")
    
    conn.commit()

conn.commit()
conn.close()