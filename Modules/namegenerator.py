import os
import names, string
import csv, random
from Paths.paths import PATH_NAME_FOLDER
from os import path
import time
from Loader.osSelector import clearScreen

def name():

    clearScreen()

    amount = int(input("How many names: "))

    with open(path.join(PATH_NAME_FOLDER, "names.csv"), "w", newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Full Name', 'Gender']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        count=1
        for i in range(amount):

            first_name = names.get_first_name()

            last_name = names.get_last_name()

            full_name = first_name + (' ') + last_name

            thewriter.writerow({'First Name':first_name,'Last Name':last_name, 'Full Name':full_name})

            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            red_color = '\033[91m' #red
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{first_name}{' | '}{last_name}{' | '}{full_name} {reset_color}")
            count+=1

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_NAME_FOLDER, "names.csv"))
    else:
        None

def jig_names():

    name = input('input name: ')
    amount = int(input('Amount of j1gs: '))

    with open(path.join(PATH_NAME_FOLDER, "names.csv"), "w", newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Full Name', 'Gender']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        count=1
        for i in range(amount):
            lengthofname = int(len(name))

            string.ascii_letters
            randomletter1 = random.choice(string.ascii_letters)
            randomletter2 = random.choice(string.ascii_letters)

            number = random.randint(0,lengthofname)
            first_word = name[:number]
            second_word = name[number:]
            word = first_word + randomletter1 + second_word


            lengthofname = int(len(word))

            number = random.randint(0,lengthofname)
            first_word = word[:number]
            second_word = word[number:]

            final_word = first_word + randomletter2 + second_word


            thewriter.writerow({'First Name':final_word,'Last Name':'BLANK', 'Full Name':'BLANK'})
            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{final_word}{reset_color}")
            count+=1
    
    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_NAME_FOLDER, "names.csv"))
    else:
        None

def start():
    print("1. Generate Names")
    print("2. Jig Names")
    print("")
    print("3. Back")
    print("")
    option = input("Option: ")

    if option == '1':
        name()
    elif option == '2':
        jig_names()
    elif option == '3':
        return "BACK"