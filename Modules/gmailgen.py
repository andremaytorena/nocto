from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time, random
from colorama import Fore
import pandas as pd
from smsactivate.api import SMSActivateAPI # SMSActivateAPI Contains all basic tools for working with the SMSActivate API 
import csv
import os
import json
import logging
import requests
import sys
from Paths.paths import PATH_PROXIES, PATH_GMAIL_CREATED, PATH_GMAIL_EMAILS
import Modules.jsonerrorlogs as jsonerrorlogs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller


def CheckEntryStatus(): # Opens accounts csv and gets account

    global APIKEY, mode, webhook, country_code, retry_limit

    account_num = 1
    entered_num = 1

    proxy_line = 0
    account_number = 1

    retry_limit = int(jsonerrorlogs.jsonretrylimit())

    webhook = jsonerrorlogs.jsonwebhook()
    
    country_code = jsonerrorlogs.jsongmailcountrycode()
    
    Phone_Verification_Mode = jsonerrorlogs.jsongmailphoneauth()

    if Phone_Verification_Mode == 'manual':
        mode = True
    elif Phone_Verification_Mode == 'smsactivateru':
        mode = False
        APIKEY = jsonerrorlogs.jsonsmsactivatekey()
    
    prox = os.stat(PATH_PROXIES).st_size == 0
    if prox == False:
        True
    elif prox == True:
        print(f'{Fore.RED}ERROR; Go on proxies.txt and add proxies')
        input(f'{Fore.RESET}Press any key to close this window...')
        sys.exit()
        

    results_accounts = pd.read_csv(PATH_GMAIL_EMAILS)
    _linesaccounts = int((len(results_accounts)))


    results_entered = pd.read_csv(PATH_GMAIL_CREATED)
    _linesentered = int((len(results_entered)))


    for i in range(_linesaccounts): # amount of lines in accounts CSV
        entered_num = 1
        for i in range(_linesentered): # amount of lines in entered CSV
            error = 0
            with open(PATH_GMAIL_EMAILS) as accounts:
                mycsv = accounts.readlines()
                y = mycsv[account_num].rstrip('\n')
                y = y.split(",")
                emails = y
                username = emails[0]
                password = emails[1]
                firstname = emails[2]
                lastname = emails[3]
                recovery = emails[4]
                day = emails[5]
                month = emails[6]
                year = emails[7]
                gender = emails[8]
                phone = emails[9]


            with open(PATH_GMAIL_CREATED) as entered:
                mycsv = entered.readlines()
                x = mycsv[entered_num].rstrip('\n')
                x = x.split(",")
                ent = x[0]
                
            
            if username == ent:
                error = 1
                print(f'{Fore.RED}This email has already been created, moving to the next one....')
                break
            else:
                entered_num = entered_num + 1
                continue
                    
        if error == 1:
            account_num = account_num + 1
            continue
        else:

            s = username.split('@')
            username = (s[0])
            
            start(firstname,lastname,username,password,recovery,day,month,year,gender,phone, account_number, proxy_line)
            
            entered_num = 0
            account_num = account_num + 1

            account_number = account_number + 1
            proxy_line = proxy_line + 1



def GetSMS(idnum, account_number, username, APIKEY):
    sa = SMSActivateAPI(APIKEY)

    count = True
    while count == True:
        status = sa.getStatus(id=idnum) # STATUS_WAIT_CODE 
        try: 
            status = (sa.activationStatus(status)) # {'status': 'STATUS_WAIT_CODE', 'message': 'Ожидание смс'} 
            messageid = str(status['status'])
            if messageid == 'STATUS_WAIT_CODE':
                print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Waiting for SMS...')
                time.sleep(4)
            else:
                newstr = messageid.replace("STATUS_OK:", "")
                print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'SMS code: ' + newstr)
                count = False
                return newstr

        except: 
            print(status['message']) # Error text  


def send_webhook_success(username, password, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
    success = {
            "content": None,
            "embeds": [
                {
                "title": "Gmail Successfully Generated",
                "color": None,
                "fields": [
                    {
                    "name": "Email",
                    "value": username,
                    "inline": None
                    },
                    {
                    "name": "Password",
                    "value": password,
                    "inline": None
                    },
                    {
                    "name": "Proxy",
                    "value": PROXY_HOST + PROXY_PORT + PROXY_USER + PROXY_PASS
                    }
                ],
                "footer": {
                    "text": "Powered by NoctoTools",
                    "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
                },
                "thumbnail": {
                    "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
                }
                }
            ],
            "attachments": []
            }

    owner_success_json = {
        "content": None,
        "embeds": [
            {
            "title": "Gmail Generated",
            "color": None,
            "fields": [
                {
                "name": "Email:",
                "value": username
                }
            ]
            }
        ],
        "attachments": []
        }
                
    owner_success = 'https://discord.com/api/webhooks/1034870524091842621/PdoX_e2suCJkHi9nuBnLtQeu7oLyuuHA8I9g3PD18YK9aOQvPrTEoLT2BBR_KNVfhMVC'
    requests.post(webhook, json=success)
    requests.post(owner_success, json=owner_success_json)


def human_type(element, text):
    for char in text:
        time.sleep(random.randint(0.1,0.3)) #fixed a . instead of a ,
        element.send_keys(char)


def createaccount(firstname, lastname, username, password, recovery, day, monthdate, year, genderis, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, account_number, phone):
    for i in range(1):


        http_proxy = 'http://' + PROXY_USER + ':' + PROXY_PASS + '@' + PROXY_HOST + ':' + PROXY_PORT
        https_proxy = 'https://' + PROXY_USER + ':' + PROXY_PASS + '@' + PROXY_HOST + ':' + PROXY_PORT

        options = {
                'proxy': {
                    'http': http_proxy,
                    'https': https_proxy,
            }
            }
        
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--ignore-certificate-errors")


        logging.getLogger("seleniumwire").setLevel(logging.ERROR)

        #change this to your chromedriver path
        
        driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=options)

        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Getting URL')
        driver.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')

        # time.sleep(100000)

        # input_field = driver.find_element(By.XPATH, '//*[@id="firstName"]')
        # actions = ActionChains(driver)
        # actions.move_to_element(input_field)
        # actions.click(input_field)
        # for char in firstname:
        #     actions.send_keys(char)
        #     actions.perform()
        #     time.sleep(random.uniform(0.1, 0.3))

    
        #adding first name ---------------------------------------------------------------------------------------------------------------------
        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Adding Information')
        for i in range(retry_limit):
            try:
                # driver.find_element(By.XPATH, '//*[@id="firstName"]').send_keys(firstname)
                input_field = driver.find_element(By.XPATH, '//*[@id="firstName"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in firstname:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)

        time.sleep(1)
        #adding last name -----------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                # driver.find_element(By.XPATH, '//*[@id="lastName"]').send_keys(lastname)
                input_field = driver.find_element(By.XPATH, '//*[@id="lastName"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in lastname:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)
        
        time.sleep(1)
        #adding email ----------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                # driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
                input_field = driver.find_element(By.XPATH, '//*[@id="username"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in username:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)

        time.sleep(1)
        #adding password --------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                # driver.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input').send_keys(password)
                input_field = driver.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in password:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)

        time.sleep(1)
        #adding password again
        for i in range(retry_limit):
            try:
                #driver.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input').send_keys(password)
                input_field = driver.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in password:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)

        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="accountDetailsNext"]/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Information, Retrying...')
                time.sleep(2)



        time.sleep(5)
        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Getting Phone Number')
        # GETTING PHONE NUMBER ----------------------------------------------------------------------------------------------------------------------------------------
        global phonenumber
        if mode == True:
            phonenumber = phone

        elif mode == False:
            sa = SMSActivateAPI(APIKEY)

            number = sa.getNumberV2(service='go', country=country_code) 
            try: 
                # print(number['phoneNumber']) # 79999999999 
                idnum = (number['activationId'])
                phonenumber = number['phoneNumber']

            except: 
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'SMS Activate: ' + (number['message']))
                break

        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Adding Phone Number')

        #adding phone number ---------------------------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                #driver.find_element(By.XPATH, '//*[@id="phoneNumberId"]').send_keys(phonenumber)
                input_field = driver.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in phonenumber:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Phone Number, Retrying...')
                time.sleep(2)

        time.sleep(2)
        #confirming phone number -----------------------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:

                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Verifying Adding Phone Number, Retrying...')
                time.sleep(2)
        
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div[2]/div[2]/div')
            break
        except:
            nonsense = False
        
        if mode == True:
            newstr = input(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Input the SMS code:')
        elif mode == False:
            newstr = GetSMS(idnum, account_number, username, APIKEY)


        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Verifying Phone number')
        #adding sms code -----------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                #driver.find_element(By.XPATH, '//*[@id="code"]').send_keys(newstr)
                input_field = driver.find_element(By.XPATH, '//*[@id="code"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in newstr:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding SMS Code, Retrying...')
                time.sleep(2)
        time.sleep(1.5)
        #confirming sms code -----------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Confirming SMS Code, Retrying...')
                time.sleep(2)
        time.sleep(5)
    
        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Adding Recovery Email/Dob/Gender')
        
        #adding recovery email ----------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                input_field = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in recovery:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                #driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input').send_keys(recovery)
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Recovery Email, Retrying...')
                time.sleep(2)

        time.sleep(1)
        #adding birthday -------------------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                input_field = driver.find_element(By.XPATH, '//*[@id="day"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in day:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                #driver.find_element(By.XPATH, '//*[@id="day"]').send_keys(day)
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Birthday, Retrying...')
                time.sleep(2)

        #adding birthmonth ------------------------------------------------------------------------------------------------------------------------------------
        for i in range(retry_limit):
            try:
                input_field = driver.find_element(By.XPATH, '//*[@id="month"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                time.sleep(0.5)
                driver.find_element(By.XPATH, monthdate).click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Birthmonth, Retrying...')
                time.sleep(2)
        
        #adding birthyear
        for i in range(retry_limit):
            try:
                input_field = driver.find_element(By.XPATH, '//*[@id="year"]')
                actions = ActionChains(driver)
                actions.move_to_element(input_field)
                actions.click(input_field)
                for char in year:
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.1, 0.3))
                # driver.find_element(By.XPATH, '//*[@id="year"]').send_keys(year)
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Adding Birthyear, Retrying...')
                time.sleep(2)

        time.sleep(1)
        
        input_field = driver.find_element(By.XPATH, '//*[@id="gender"]')
        actions = ActionChains(driver)
        actions.move_to_element(input_field)
        driver.find_element(By.XPATH, '//*[@id="gender"]').click()
        driver.find_element(By.XPATH, genderis).click()
        time.sleep(2)

        print(f'{Fore.RESET}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Finishing Account Details')

        #finalizing details check THIS WORKS
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Submitting Details, Retrying...')
                time.sleep(2)

        time.sleep(2)
        #get more from your number pop up
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button').click()
                break
            except:
                time.sleep(2)

        #finalizing details check 1 
        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button/span').click()
                break
            except:
                time.sleep(2)

        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]/div').click()
                break
            except:
                time.sleep(2)        

        #finalizing details check 2
        # time.sleep(2)
        # for i in range(retry_limit):
        #     try:
        #         driver.find_element(By.XPATH, '//*[@id="selectionc10"]').click()
        #         break
        #     except:
        #         print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Submitting Details (Check2), Retrying...')
        #         time.sleep(2)

        #finalizing details check 3
        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Submitting Details (Check3), Retrying...')
                time.sleep(2)

        #finalizing details check 4
        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Submitting Details (Check4), Retrying...')
                time.sleep(2)
        
        #finalizing details check 5
        time.sleep(2)
        for i in range(retry_limit):
            try:
                driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span').click()
                break
            except:
                print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Failed Submitting Details (Check5), Retrying...')
                time.sleep(2)
    
        time.sleep(17)

        try:
            driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/header/div[2]')
            print(f'{Fore.LIGHTGREEN_EX}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'Successfully Created Gmail Account')
            send_webhook_success(username, password, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
            record_success(username, password) 
            
        except:
            print(f'{Fore.RED}|'+ str(account_number) + '| '  + (username) + '@gmail.com | ' + 'FAILED')

        # time.sleep(3)

        # def forward_email():
        #     driver.get('https://mail.google.com/mail/u/0/#settings/fwdandpop')
        #     time.sleep(1)
        #     driver.find_element(By.XPATH, '//*[@id=":jy"]/input').click()
        #     time.sleep(0.5)
        #     driver.find_element(By.XPATH, '//*[@id=":k5"]').send_keys('andremayto@gmail.com')
        #     time.sleep(0.5)
        #     driver.find_element(By.XPATH, '/html/body/div[36]/div[3]/button[1]').click()
        #     driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/input[3]').click()
        #     input('done')


        # # forward_email()






def start(firstname,lastname,username,password,recovery,day,month,year,gender,phone, account_number, proxy_line):
    
    monthdate = f'//*[@id="month"]/option[{int(month)+1}]'


    if gender == 'M':
        genderis = '//*[@id="gender"]/option[3]'
    elif gender == 'F':
        genderis = '//*[@id="gender"]/option[2]'


    with open(PATH_PROXIES) as file:
        myproxies = file.readlines()
        x = myproxies[proxy_line].rstrip('\n')
        x = x.split(":")
        proxies = x

        PROXY_HOST = proxies[0]
        PROXY_PORT = proxies[1]
        PROXY_USER = proxies[2]
        PROXY_PASS = proxies[3]

    createaccount(firstname, lastname, username, password, recovery, day, monthdate, year, genderis, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, account_number, phone)




def record_success(username, password):

    username = username + '@gmail.com'

    fieldnames = ['Email', 'Password']

    with open(PATH_GMAIL_CREATED) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_GMAIL_CREATED, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Email':username, 'Password':password}
        ]

        if not has_newline:
            f.write('\n')

        writer.writerows(rows)

