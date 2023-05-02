import requests
import csv
import Modules.logger as logger
from Paths.paths import PATH_POSTCODE_FOLDER
from os import path
import time, os

def request(count):

    s  = requests.get('https://api.postcodes.io/random/postcodes')

    data = s.json()


    postcode = (data['result']['postcode'])
    postcode_main(postcode, count)

def postcode_main(postcode, count):

    with open(path.join(PATH_POSTCODE_FOLDER, "postcodes.csv"), "a", newline='') as csvfile:
        fieldnames = ['postcode']
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writerow({'postcode':postcode})

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{postcode} {reset_color}")



def postcode_start():


    amount = int(input('How many postcodes: '))

    with open(path.join(PATH_POSTCODE_FOLDER, "postcodes.csv"), "w", newline='') as csvfile:
            fieldnames = ['postcode']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()

    count = 1
    for i in range(amount):
        
        request(count)
        count +=1

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_POSTCODE_FOLDER, "postcodes.csv"))
    else:
        None