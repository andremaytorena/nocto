import Modules.logger as logger
from Paths.paths import PATH_PASSWORD_FOLDER
from os import path
import csv, os
import random
import time

def passwordgen_main():
        
    print('Type of password: ')
    print('')
    print('1. Symbols : @7Q4A4J8S5a')
    print("2. No symbols : 7Q4A4J8S5a")
    print('')
    option = int(input("Option: "))
    print('')

    amount = int(input("How many passwords: "))

    def symbol():
        with open(path.join(PATH_PASSWORD_FOLDER, "passwords.csv"), "w", newline='') as csvfile:
            fieldnames = ['password']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count = 1
            for i in range(amount):

                num1 = random.randint(0, 9)
                num2 = random.randint(0, 9)
                num3 = random.randint(0, 9)
                num4 = random.randint(0, 9)
                num5 = random.randint(0, 9)

                randuppercase = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_2 = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_3 = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_4 = chr(random.randint(ord('A'), ord('Z')))
                password = (("@") + str(num1) + str(randuppercase) + str(num2) + str(randuppercase_2) + str(num3) + str(randuppercase_3) + 
                str(num4) + str(randuppercase_4) + str(num5) + "a")

                thewriter.writerow({'password': password})

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{password} {reset_color}")
                count += 1


    def no_symbol():
        with open(path.join(PATH_PASSWORD_FOLDER, "passwords.csv"), "w", newline='') as csvfile:
            fieldnames = ['password']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count = 1
            for i in range(amount):

                num1 = random.randint(0, 9)
                num2 = random.randint(0, 9)
                num3 = random.randint(0, 9)
                num4 = random.randint(0, 9)
                num5 = random.randint(0, 9)

                randuppercase = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_2 = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_3 = chr(random.randint(ord('A'), ord('Z')))
                randuppercase_4 = chr(random.randint(ord('A'), ord('Z')))
                password = (str(num1) + str(randuppercase) + str(num2) + str(randuppercase_2) + str(num3) + str(randuppercase_3) + 
                str(num4) + str(randuppercase_4) + str(num5) + "a")

                thewriter.writerow({'password': password})
                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{password} {reset_color}")
                count += 1

    if option == 1:
        symbol()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PASSWORD_FOLDER, "passwords.csv"))
        else:
            None

    elif option == 2:
        no_symbol()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PASSWORD_FOLDER, "passwords.csv"))
        else:
            None