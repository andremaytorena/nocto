import requests
import time
from selenium import webdriver
import time
from Paths.paths import PATH_CHROME_DRIVER

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
        print(list_result['result']['hmeEmails'][count])
        email_id = list_result['result']['hmeEmails'][count]['anonymousId']
        status = str(list_result['result']['hmeEmails'][count]['isActive'])
        
        if status == "False":
            None
        else:

            reserve_email_result = session.post(
                'https://p33-maildomainws.icloud.com/v1/hme/deactivate',

                headers={
                    "Origin": "https://www.icloud.com"
                },

                json={
                    "anonymousId": email_id,
                }
            ).json()

            print(reserve_email_result)

        count+=1

# https://p33-maildomainws.icloud.com/v1/hme/deactivate?clientBuildNumber=2304Project37&clientMasteringNumber=2304B26&clientId=3082d623-77f5-41b1-a87f-5c2db0352e27&dsid=8202513079

        


def task():

    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])


    driver = webdriver.Chrome(
        options=options, executable_path=PATH_CHROME_DRIVER)

    driver.get('https://icloud.com')

    input('Press enter when you have logged in! ')

    cooks = driver.get_cookies()

    driver.close()

    export(cooks)

task()


