import stripe
import csv
import time
from colorama import Fore
import json, os
from Paths.paths import PATH_SETTINGS, PATH_STRIPE
from os import path

def Card():

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    loadsettings = (settings["Stripe"])
    API = (loadsettings['API_Key'])
    CARDHOLDER_ID = (loadsettings['CardHolder_ID'])

    stripe.api_key = API

    createcard = stripe.issuing.Card.create(
    cardholder=CARDHOLDER_ID,
    currency="gbp",
    type="virtual",
    )

    ID = (createcard['id'])

    stripe.issuing.Card.modify(ID, status="active")

    card_details = stripe.issuing.Card.retrieve(ID, expand=["number", "cvc"])
    number = (card_details['number'])
    cvc = (card_details['cvc'])
    month = (card_details['exp_month'])
    year = (card_details['exp_year'])
    cardholder = (card_details['cardholder'])
    name = cardholder['name']
    if not card_details:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Stripe Card Generator: Failed Creating Card'} {reset_color}")
        
    else:
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Stripe Card Generator: Successfully Created Card'} {reset_color}")
        writecard(number, cvc, month, year, name)



def createCSV():

    currenttime = str(time.time())

    currenttime = currenttime + '.csv'

    global NEW_PATH
    NEW_PATH = path.join(PATH_STRIPE, currenttime)

    global fieldnames
    
    with open(NEW_PATH, 'w', newline='') as file:
        fieldnames = ['Name', 'Card Number', 'Card Month', 'Card Year', 'CVC']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()

    

def writecard(number, cvc, month, year, name):

    with open(NEW_PATH) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(NEW_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Name': name, 'Card Number': number, 'Card Month': month, 'Card Year': year, 'CVC': cvc}
        ]

        if not has_newline:
            f.write('\n')
    
        writer.writerows(rows)



def start():
    
    amount = int(input('How many cards: '))
    global count
    count = 1

    createCSV()

    for i in range(amount):
        Card()
        count = count + 1
        time.sleep(3)

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(NEW_PATH)
    else:
        None





