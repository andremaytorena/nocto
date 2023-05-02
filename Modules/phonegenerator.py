import Modules.logger as logger
from Paths.paths import PATH_PHONE_FOLDER
import csv,os
from os import path
import random
import time


def phonegen_main():

    print('Type of Phone: ')
    print('')
    print('1. +447484889982')
    print("2. 07484889982")
    print('3. 7484889982')
    print("4. Custom")
    print('')
    option = int(input("Option: "))
    print('')

    amount = int(input("How many phones: "))

    def type_1():

        with open(path.join(PATH_PHONE_FOLDER, "phones.csv"), "w", newline='') as csvfile:
            fieldnames = ['phones']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count = 1
            for i in range(amount):

                num1 = random.randint(0,9)
                num2 = random.randint(0,9)
                num3 = random.randint(0,9)
                num4 = random.randint(0,9)
                num5 = random.randint(0,9)
                num6 = random.randint(0,9)
                num7 = random.randint(0,9)
                num8 = random.randint(0,9)
                num9 = random.randint(0,9)
                num10 = random.randint(0,9)

                phone = ('+44')+ str(num1) + str(num2) + str(num3) + str(num4) + str(num5) + str(num6) + str(num7) + str(num8) + str(num9) + str(num10)
                thewriter.writerow({'phones':phone})

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{phone} {reset_color}")
                count += 1
   

    def type_2():

        with open(path.join(PATH_PHONE_FOLDER, "phones.csv"), "w", newline='') as csvfile:
            fieldnames = ['address']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count = 1
            for i in range(amount):

                num2 = random.randint(0,9)
                num3 = random.randint(0,9)
                num4 = random.randint(0,9)
                num5 = random.randint(0,9)
                num6 = random.randint(0,9)
                num7 = random.randint(0,9)
                num8 = random.randint(0,9)
                num9 = random.randint(0,9)
                num10 = random.randint(0,9)

                phone = ('0') + ('7') + str(num2) + str(num3) + str(num4) + str(num5) + str(num6) + str(num7) + str(num8) + str(num9) + str(num10)
                thewriter.writerow({'address':phone})

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{phone} {reset_color}")
                count += 1


    def type_3():
        
        with open(path.join(PATH_PHONE_FOLDER, "phones.csv"), "w", newline='') as csvfile:
            fieldnames = ['address']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count = 1
            for i in range(amount):

                num2 = random.randint(0,9)
                num3 = random.randint(0,9)
                num4 = random.randint(0,9)
                num5 = random.randint(0,9)
                num6 = random.randint(0,9)
                num7 = random.randint(0,9)
                num8 = random.randint(0,9)
                num9 = random.randint(0,9)
                num10 = random.randint(0,9)

                phone = ('7') + str(num2) + str(num3) + str(num4) + str(num5) + str(num6) + str(num7) + str(num8) + str(num9) + str(num10)
                thewriter.writerow({'address':phone})

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{phone} {reset_color}")
                count += 1


    def type_4():
        
        with open(path.join(PATH_PHONE_FOLDER, "phones.csv"), "w", newline='') as csvfile:
            fieldnames = ['address']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            length = int(input('Length of number: '))
            country_code = input('Add a country code? (y/n): ')
            count = 1
            if country_code == 'y' or country_code == 'Y':
                code = input("Input country code: ")
                for i in range(amount):
                    string = ''
                    string = string + code
                    for i in range(length):
                        number = random.randint(1,9)
                        string = string + str(number)
                    thewriter.writerow({'address':string})
                    logger.phonenumber_log_success(string)
                    
            elif country_code == 'n' or country_code == 'N':
                None
                for i in range(amount):
                    string = ''
                    for i in range(length):
                        number = random.randint(1,9)
                        string = string + str(number)

                    thewriter.writerow({'address':string})
            
                    green_color = '\033[92m' #light green
                    reset_color = '\033[0m' #reset color
                    red_color = '\033[91m' #red
                    print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{string} {reset_color}")
                    count += 1




    if option == 1:
        type_1()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PHONE_FOLDER, "phones.csv"))
        else:
            None

    elif option == 2:
        type_2()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PHONE_FOLDER, "phones.csv"))
        else:
            None

    elif option == 3:
        type_3()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PHONE_FOLDER, "phones.csv"))
        else:
            None

    elif option == 4:
        type_4()
        OKBLUE = '\033[94m'
        reset_color = '\033[0m' #reset color
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(path.join(PATH_PHONE_FOLDER, "phones.csv"))
        else:
            None
