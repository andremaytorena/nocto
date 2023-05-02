import requests, csv, time, os, sys
from Paths.paths import PATH_PRODIRECT_PROFILES, PATH_PROXIES
from colorama import Fore
import Modules.proxieserrorlogs as proxieserrorlogs
def generate_token(proxies):

    red_color = '\033[91m' #red
    reset_color = '\033[0m' #reset color
    
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Generating Authentication Values.. '} {reset_color}")

    url = 'https://login.prodirectsoccer.com/accounts.initRegistration?APIKey=3_kmzOK10aUUHncVW6NPJP89y02hj5Pu5MmkLVxLXw5O8VBegAbV967SA1USJHNwrJ&source=showScreenSet&sdk=js_latest&authMode=cookie&pageURL=https%3A%2F%2Fwww.prodirectsport.com%2Fsoccer%2F&sdkBuild=13432&format=json'

    payload = {
        "APIKey": "3_kmzOK10aUUHncVW6NPJP89y02hj5Pu5MmkLVxLXw5O8VBegAbV967SA1USJHNwrJ",
        "source": "showScreenSet",
        "sdk": "js_latest",
        "authMode": "cookie",
        "pageURL": "https://www.prodirectsport.com/soccer/",
        "sdkBuild": "13432",
        "format": "json"
    }


    headers = {
        "origin": "https://www.prodirectsport.com",
        "referer": "https://www.prodirectsport.com/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    for i in range(1):
        try:
            res = requests.post(url, json=payload, headers=headers, proxies=proxies)
            jsonresponse = res.json()
            regToken = (jsonresponse['regToken'])
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Successfully Generated Authentication Values'} {reset_color}")
            return regToken
            break
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Failed Generating Authentication Values'} {reset_color}")

def generate_account(regToken, email, password, firstname, lastname, proxies):

    red_color = '\033[91m' #red
    reset_color = '\033[0m' #reset color
    green_color = '\033[92m' #light green

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Generating Account..'} {reset_color}")

    s = requests.Session()

    url = 'https://login.prodirectsoccer.com/accounts.register'

    payload = {
        "email": email,
        "password": password,
        "regToken": regToken,
        "regSource": "https://www.prodirectsport.com/soccer/",
        "profile": '{"firstName":"' + firstname + '","lastName":"' + lastname + '"}',
        "lang": "en",
        "targetEnv": "jssdk",
        "sessionExpiration": "-1",
        "include": "profile,data,emails,loginIDs,subscriptions,preferences,",
        "includeUserInfo": "true",
        "APIKey": "3_kmzOK10aUUHncVW6NPJP89y02hj5Pu5MmkLVxLXw5O8VBegAbV967SA1USJHNwrJ",
        "source": "showScreenSet",
        "sdk": "js_latest",
        "pageURL": "https://www.prodirectsport.com/soccer/",
        "sdkBuild": "13432",
        "format": "json"
    }

    headers = {
        "origin": "https://www.prodirectsport.com",
        "referer": "https://www.prodirectsport.com/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    for i in range(3):
        try:
            res = s.post(url, data=payload, headers=headers,proxies=proxies)
            jsonresponse = (res.json())
            reg_token = (jsonresponse['regToken'])
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Successfully Generated Account'} {reset_color}")
            return reg_token
            break

        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Failed Generating Account'} {reset_color}")
            time.sleep(2)

def set_birthday(reg_token, bday, proxies):

    red_color = '\033[91m' #red
    reset_color = '\033[0m' #reset color
    green_color = '\033[92m' #light green

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Adding Birthday..'} {reset_color}")

    new_bday = str(bday).split("-")
    day = new_bday[0]
    month = new_bday[1]
    year = new_bday[2]

    url = 'https://login.prodirectsoccer.com/accounts.setAccountInfo'

    payload = {
        "profile": '{"birthDay":"' + day + '","birthMonth":"' + month + '","birthYear":"' + year + '","gender":"m"}',
        "data": '{"registrationCompleted":"true"}',
        "conflictHandling": "fail",
        "lang": "en",
        "APIKey": "3_kmzOK10aUUHncVW6NPJP89y02hj5Pu5MmkLVxLXw5O8VBegAbV967SA1USJHNwrJ",
        "source": "showScreenSet",
        "sdk": "js_latest",
        "login_token": reg_token,
        "authMode": "cookie",
        "pageURL": "https://www.prodirectsport.com/soccer/",
        "sdkBuild": "13432",
        "format": "json"
    }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "643",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.prodirectsport.com",
        "referer": "https://www.prodirectsport.com/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    
    res = requests.post(url, data=payload, headers=headers,proxies=proxies)
    if res.json()['statusCode'] == 200:
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Successfully Added Birthday'} {reset_color}")
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Pro Direct: Failed To Add Birthday: Wrong Format'} {reset_color}")


def gen_acc(email, password, firstname, lastname, bday, proxies):
    regToken = generate_token(proxies)
    reg_token = generate_account(regToken, email, password, firstname, lastname, proxies)
    set_birthday(reg_token, bday, proxies)
    

def start():

    global count

    proxy_count = 0
    count = 1

    proxieserrorlogs.checkproxies()

    with open(PATH_PRODIRECT_PROFILES) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            email = row[0]
            password = row[1]
            firstname = row[2]
            lastname = row[3]
            bday = row[4]

            with open(PATH_PROXIES) as file:
                myproxies = file.readlines()
                x = myproxies[proxy_count].rstrip('\n')
                x = x.split(":")
                PROXY_HOST = (x[0])
                PROXY_PORT = (x[1])
                PROXY_USERNAME = (x[2])
                PROXY_PASSWORD = (x[3])

            PROXY = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
            proxies = {
                "http": PROXY,
                "https": PROXY,
            }

        
            gen_acc(email, password, firstname, lastname, bday, proxies)

            proxy_count+=1
            count+=1

