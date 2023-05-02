import random
import csv
from Paths.paths import PATH_BDAY_FOLDER
import time, os
from os import path

def bdaygen_main():

    amount = int(input("How many birthdates: "))

    with open(path.join(PATH_BDAY_FOLDER, "bdays.csv"), "w", newline='') as csvfile:
        fieldnames = ['bday']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        count = 1
        for i in range(amount):

            month = ['01','02','03','04','05','06','07','08','09','10','11','12']
            day = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

            random_month = random.choice(month)
            random_day = str(random.choice(day))

            bday = random_month + ('-') + random_day

            thewriter.writerow({'bday':bday})

            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            red_color = '\033[91m' #red
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{bday} {reset_color}")
            count += 1

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_BDAY_FOLDER, "bdays.csv"))
    else:
        None