import requests, time, os, csv
from selenium import webdriver
from os import path
from Paths.paths import PATH_ICLOUD_GEN, PATH_ICLOUD_GEN_FOLDER, PATH_CHROME_DRIVER
import Modules.jsonerrorlogs as jsonerrorlogs

    

def createCSV():

    currenttime = str(time.time())

    currenttime = currenttime + '.csv'

    global NEW_PATH
    NEW_PATH = path.join(PATH_ICLOUD_GEN_FOLDER, currenttime)

    global fieldnames
    
    with open(NEW_PATH, 'w', newline='') as file:
        fieldnames = ['Emails']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()


def writeemail(hme_email):

    with open(NEW_PATH) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(NEW_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Emails': hme_email}
        ]

        if not has_newline:
            f.write('\n')
    
        writer.writerows(rows)



def log_success():
    owner_success_json = {
        "content": None,
        "embeds": [
            {
            "title": "iCloud Generated",
            "color": None,
            "fields": [
                {
                "name": "Email:",
                "value": 'iCloud Generated'
                }
            ]
            }
        ],
        "attachments": []
        }
    URL = 'https://discord.com/api/webhooks/1036411813526515803/nhzwThFbrtThlMPegC5Zms8hildOPv9_2AZpKL9SdrLnnCYrLiK9h-SKzJJ7ZM5WbE7G'
    requests.post(URL, json=owner_success_json)
    requests.post(webhook, json=owner_success_json)

def generate(cooks, AMOUNT):

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    TASKS_DONE = 1

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Starting Session'} {reset_color}")

    session = requests.session()

    for cookie in cooks:
        session.cookies.set(
            cookie["name"], cookie["value"], domain='icloud.com'
        )


    for i in range(AMOUNT):

        try:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Fetching Current Emails'} {reset_color}")
            list_result = session.get(
                'https://p68-maildomainws.icloud.com/v1/hme/list',

                headers={
                    "Origin": "https://www.icloud.com",
                }
            ).json()

            # print(list_result['result']['hmeEmails'][0]['hme'])


            if list_result['success'] == True:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Got Current Emails'} {reset_color}")

            # ------------------------

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Generating New Email 1/2'} {reset_color}")
            generate_result = session.post(
                'https://p68-maildomainws.icloud.com/v1/hme/generate',

                headers={
                    "Origin": "https://www.icloud.com",
                }
            ).json()


            if generate_result['success'] == True:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Generated New Email 2/2'} {reset_color}")

            # ------------------------

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Reserving New Email 2/2'} {reset_color}")
            reserve_email_result = session.post(
                'https://p68-maildomainws.icloud.com/v1/hme/reserve',

                headers={
                    "Origin": "https://www.icloud.com"
                },

                json={
                    "hme": generate_result['result']['hme'],
                    "label": "shopping",
                    "note": "",
                }
            ).json()

            if reserve_email_result['success'] == True:

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: New iCloud Email Generated: '}{generate_result['result']['hme']} {reset_color}")

                open(PATH_ICLOUD_GEN, 'a').write(f'\n' + generate_result['result']['hme'])

                log_success()

            elif reserve_email_result['success'] == False:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{TASKS_DONE}] {'iCloud Email Generator: Apple Rate Limit, Waiting 1 Hour'} {reset_color}")
                time.sleep(3660)

            TASKS_DONE+=1

        except:
            input("ERROR OCCURRED, cookies might have expired or no icloud + installed.")
            


def export(cooks):

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'iCloud Email Generator: Starting Session'} {reset_color}")

    session = requests.session()

    for cookie in cooks:
        session.cookies.set(
            cookie["name"], cookie["value"], domain='icloud.com'
        )


    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'iCloud Email Generator: Fetching Current Emails'} {reset_color}")
    list_result = session.get(
        'https://p68-maildomainws.icloud.com/v1/hme/list',

        headers={
            "Origin": "https://www.icloud.com",
        }
    ).json()

    email_list = list_result['result']['hmeEmails']
    count = 0
    for i in range(len(email_list)):

        hme_email = (list_result['result']['hmeEmails'][count]['hme'])
        writeemail(hme_email)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'iCloud Email Generator: Successfully Exported Email: '}{hme_email} {reset_color}")
        
        count = count + 1


        


def task(mode):

    global webhook

    webhook = jsonerrorlogs.jsonwebhook()

    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options, executable_path=PATH_CHROME_DRIVER)

    driver.get('https://icloud.com')

    input('Press enter when you have logged in! ')

    cooks = driver.get_cookies()

    driver.close()

    if mode == True:
        AMOUNT = int(input("How many emails: "))
        generate(cooks, AMOUNT)
    elif mode == False:
        createCSV()
        export(cooks)



def task_option():

    print("Select Module: ")
    print('')
    print("1. Generate iClouds")
    print("2. Export Current iClouds")
    print("")
    print("3. Back")
    print("")
    option = int(input('Option: '))
    if option == 1:
        mode = True
    elif option == 2:
        mode = False
    elif option == 3:
        return "BACK"

    task(mode)

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(NEW_PATH)
    else:
        None

