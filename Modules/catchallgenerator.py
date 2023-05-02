import Modules.logger as logger
from Paths.paths import PATH_CATCHALL_FOLDER
from os import path
import csv
import random
import names
import time, os

def catchall_main():

    catchall = input('Input domain: EG. outlook.com / hotmail.com: ')
    print('')
    amount = int(input("How many emails: "))
    amount_of_num = int(input("How many numbers at the end of email: "))

    with open(path.join(PATH_CATCHALL_FOLDER, "catchall.csv"), 'w', newline='') as csvfile:
        fieldnames = ['address']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        count = 1
        for i in range(amount):

            rand_first = names.get_first_name()
            rand_last = names.get_last_name()

            numbers = ''
            for i in range(amount_of_num):
                num = random.randint(0,9)
                numbers = numbers + str(num)

            catchall_email = (rand_first + rand_last +numbers+ ("@") + catchall)

            thewriter.writerow({'address':catchall_email})
            
            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            red_color = '\033[91m' #red
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{catchall_email} {reset_color}")
            count += 1
    
    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_CATCHALL_FOLDER, "catchall.csv"))
    else:
        None