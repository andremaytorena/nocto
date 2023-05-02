import requests, sys, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from twocaptcha import TwoCaptcha
import time
from Paths.paths import PATH_CHROME_DRIVER
import requests, os, sys, time, threading
import pandas as pd 
from Paths.paths import PATH_JDX_FOLDER, PATH_JDX_LOGS, MAIN_PATH, PATH_PROXIES
import RaffleModules.webhook_management as webhooks
from os import path
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, json2captcha, proxiesfile
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


success_entry_count = 0
failed_entry_count = 0

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red


def enter_raffle(size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, main_count):

    solver = TwoCaptcha(os.getenv('APIKEY_2CAPTCHA', captcha_key))

    session = requests.Session()

    try:
        result = solver.recaptcha(
            sitekey='6LdTCMAUAAAAAP_h-Uqc7LqpUnZKYeFpowq29qQj',
            url=raffle_name,
            version='v3',
            action='demo_action',
            score=0.9
        )

    except Exception as e:
        sys.exit(e)

    else:
        token = result['code']

    url = 'https://nk7vfpucy5.execute-api.eu-west-1.amazonaws.com/prod/save_entry'

    headers = {
        "accept": "text/plain, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "984",
        "content-type": "application/json",
        "origin": "https://raffles.jdsports.co.uk",
        "referer": "https://raffles.jdsports.co.uk/",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    payload = {
        "address1": addressline1,
        "address2": addressline2,
        "city": city,
        "county": "Greater London",
        "dateofBirth": "01/10/2000",
        "email": email,
        "email_optin": "0",
        "firstName": firstname,
        "hostname": "https://raffles.jdsports.co.uk",
        "lastName": lastname,
        "mobile": phonenumber,
        "paypalEmail": email,
        "postCode": postcode,
        "rafflesID": "3344",
        "shoeSize": "TID3SqO1",
        "shoeSizeSkuI": "2154935",
        "siteCode": "JDUK",
        "sms_optin": "0",
        "token": token
    }

    res = session.post(url, json=payload, headers=headers)

    checkout_token = str(res.json()['pre_auth']).split('preauth=')[1]

    headers = {
        "accept": "text/plain, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "984",
        "content-type": "application/json",
        "origin": "https://raffles.jdsports.co.uk",
        "referer": "https://raffles.jdsports.co.uk/",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-api-token": checkout_token
    }
    payload = {
        "paymentMethod": "PAYPAL"
    }

    url = 'https://raffles-checkout-api.jdsports.co.uk/payments/init_Payment'
    res = session.post(url, json=payload, headers=headers)

    paypal_url = res.json()['body']['redirectUrl']['href']
    print(paypal_url)

    ser = Service()
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=ser, options=options, service_log_path='/dev/null')

    driver.get(paypal_url)

    webhooks.astro_logs("Entered Raffle!", "JDX Launches")

    time.sleep(100)


def set_csvs():

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_JDX_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_JDX_FOLDER, choose_csv[option])
    print("")
    return PROFILES_CSV

def set_proxies_file():

    choose_proxy = list(filter(lambda x: '.txt' in x, os.listdir(MAIN_PATH)))
    amount_proxyfiles = (len(choose_proxy))
    line = 0
    for i in range(amount_proxyfiles):
        with open(path.join(MAIN_PATH, choose_proxy[line]), 'r') as fp:
            amount_of_proxy_lines = len(fp.readlines())
        print(str(line) + ('. ') + choose_proxy[line] + ' [' + str(amount_of_proxy_lines) + ']')
        line+=1

    option = int(input('Option: '))
    PATH_PROXIES = path.join(MAIN_PATH, choose_proxy[option])
    print("")
    return PATH_PROXIES

def CheckEntryStatus(): # Opens accounts csv and gets account

    global amount_of_proxy_lines, webhook, retrylimit, captcha_key, raffle_name
    main_count = 0

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    retrylimit = int(jsonretrylimit())
    captcha_key = json2captcha()
    
    #gets current open raffles
    os.system(f'title JDX Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{0}] {'Getting Open Releases..'} {reset_color}")
    
    PROFILES_CSV = set_csvs()
    
    PATH_PROXIES = set_proxies_file()

    proxiesfile(PATH_PROXIES)

    raffle_name = input("Enter url: ")

    chromedriver_autoinstaller.install()

    account_num = 1
    entered_num = 1

    proxy_line = 0
    account_number = 1

    finished_entering = False
    
    results_accounts = pd.read_csv(PROFILES_CSV)
    _linesaccounts = int((len(results_accounts)))

    results_entered = pd.read_csv(PATH_JDX_LOGS)
    _linesentered = int((len(results_entered)))

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())

    while finished_entering == False:

        for i in range(threads): #amount of threads

            for i in range(1): # amount of lines in accounts CSV
                entered_num = 1
                for i in range(_linesentered): # amount of lines in entered CSV
                    error = 0
                    try: 
                        with open(PROFILES_CSV) as accounts:
                            mycsv = accounts.readlines()
                            y = mycsv[account_num].rstrip('\n')
                            row = y.split(",")
                            size = row[0]
                            email = row[1]
                            password = row[2]
                            firstname = row[3]
                            lastname = row[4]
                            addressline1 = row[5]
                            addressline2 = row[6]
                            city = row[7]
                            postcode = row[8]
                            phonenumber = row[9]
                    except IndexError:
                        finished_entering = True
                        break

                    with open(PATH_JDX_LOGS) as entered:
                        mycsv = entered.readlines()
                        x = mycsv[entered_num].rstrip('\n')
                        x = x.split(",")
                        entered_email = x[0]
                        entered_raffle = x[1]
                        
                    if email == entered_email and raffle_name == entered_raffle:
                        error = 1
                        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{0}] {'Already Entered Account'} {reset_color}")
                        break
                    else:
                        entered_num = entered_num + 1
                        continue
                            
                if error == 1:
                    account_num = account_num + 1
                    continue
                else:
                    if finished_entering == False:
                        try:
                            thread = threading.Thread(target=enter_raffle, args=[size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, main_count])
                            thread.start()
                        except UnboundLocalError:
                            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][][{0}] {'No Profiles Loaded'} {reset_color}")
                            input('Press Enter to Exit: ')
                            sys.exit()

                    entered_num = 0
                    account_num = account_num + 1

                    account_number = account_number + 1
                    proxy_line = proxy_line + 1
                    
                    main_count+=1

        if error == 1 or finished_entering == 1:
            None
        else:
            thread.join()
            time.sleep(delay)

