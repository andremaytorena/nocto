from requests_html import HTMLSession
from twocaptcha import TwoCaptcha
import json, requests
import sys
import time, os
import csv
from colorama import Fore
from Paths.paths import PATH_WEBDE_PROFILES, PATH_PROXIES, PATH_SETTINGS

def log_success():
    owner_success_json = {
        "content": None,
        "embeds": [
            {
            "title": "Web.de Email Generated",
            "color": None,
            "fields": [
                {
                "name": "Email:",
                "value": 'Web.de Email Generated'
                }
            ]
            }
        ],
        "attachments": []
        }
    URL = 'https://discord.com/api/webhooks/1046551228030664775/SxBnnLGaKBjNDMWqHtMUZVeta2NqOiew-PXPHxOGiUDNx4-HzGPEonHSXIL1_AjXBlJK'
    requests.post(URL, json=owner_success_json)
    requests.post(webhook, json=owner_success_json)

def get_proxy(proxy_count):
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
    
    return proxies

def send_request(email, password, firstname, lastname, addressline1, city, postcode, countrycode, phonenumber, birthday, gender, account_number, proxy_count):
    for i in range(1):

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red 

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Generating Authentication Values..'} {reset_color}")
        session = HTMLSession()

        proxies = get_proxy(proxy_count)

        for i in range(retry_limit):
            try:
                r = session.get('https://registrierung.web.de/', proxies=proxies)

                r.html.render()

                time.sleep(3)

                ccguid = r.text.split('l?ccguid=')[1].split('"')[0]
                auth = r.text.split('accessToken": "')[1].split('"')[0]
                
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Successfully Generated Auth Values'} {reset_color}")

                error_1 = False

                break
            
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Failed Generating Authentication Values, rotating proxy....'} {reset_color}")
                proxy_count = proxy_count+1
                print(proxy_count)
                proxies = get_proxy(proxy_count)
                error_1 = True

        if error_1 == False:
            None
        elif error_1 == True:
            break


        for i in range(retry_limit):
            try:
                url = "https://captcha.ui-portal.de/captchachallengecreation"

                payload = json.dumps({
                "siteKey": "1reg-live-39fa752c-da8c-4c80-a301-e996c4c71215"
                })
                headers = {
                'authority': 'captcha.ui-portal.de',
                'accept': 'application/vnd.captcha.challenge-v1+json',
                'accept-language': 'en-US,en;q=0.9,es;q=0.8',
                'content-type': 'application/vnd.captcha.challenge.parameter-v1+json',
                'dnt': '1',
                'origin': 'https://registrierung.web.de',
                'referer': 'https://registrierung.web.de/',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
                }

                response = session.request("POST", url, headers=headers, data=payload)
                jsonresponse = response.json()
                image = (jsonresponse["imageDataUrl"])
                token = (jsonresponse['token'])

                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Successfully Generated Auth Values (1)'} {reset_color}")

                break
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Failed Generating Authentication Values (1)'} {reset_color}")

            
    
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Waiting'}{delay}{'sec..'}{reset_color}")
        time.sleep(delay)

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Solving Image Captcha...'} {reset_color}")

        for i in range(retry_limit):
            try:
                solver = TwoCaptcha(api_key)

                try:
                    result = solver.normal(image)

                except Exception as e:
                    sys.exit(e)

                else:
                    code = (result['code'])
                    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Successfully Solved Image Captcha'} {reset_color}")
                    break
            
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Failed Solving Image Captcha'} {reset_color}")
        
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Generating Email..'} {reset_color}")

        payload = {

            "mailAccount" : {
                "email": email
            },

            "product": "webdeFree",

            "user":{
                "address": {
                    "countryCode": countrycode, #GB,
                    "locality": city,
                    "postalCode": postcode,
                    "region": "",
                    "streetAddress": addressline1
                },

                "birthDate": birthday,#2000-11-01
                "credentials": {
                    "password": password
                },
                "familyName": lastname,
                "gender": gender, #MALE
                "givenName": firstname,
                "mobileNumber": phonenumber #+4915141628492
            } 
        }


        header_bot = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Authorization": "Bearer " + auth,
            "Campaign": "#hashtag:.pc_page.tarifvergleich.index.teaser_1.registrierung#kid:kid@autoref@web.de",
            "Connection": "keep-alive",
            "Content-Length": "359",
            "Content-Type": "application/vnd.ui.mam.account.creation+json",
            "Host": "registrierung.web.de",
            "Origin": "https://registrierung.web.de",
            "Referer": "https://registrierung.web.de/",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "X-CAPTCHA-SOLUTION": code, #changes
            "X-CAPTCHA-TOKEN": token, #changes
            "X-CCGUID": ccguid, #changes,
            "X-Security-Request": "required",
            "X-UI-AP": "@umreg/registration-app2/7.1.12"
        }

        url = ' https://registrierung.web.de/account/email-registration'
        res = session.post(url, json=payload, headers=header_bot, proxies=proxies)
        if str(res.status_code) == '204':
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Successfully Generated Web.de Email'} {reset_color}")
            log_success()
        else:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Failed to Gen Email: '}{res.text} {reset_color}")


def module_start():

    global delay
    delay = int(input('Delay Between Requests (recommended 40): '))

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    if len(settings["Retry_Limit"])==0:
        print(f'{Fore.RED}ERROR; Go on settings.json and fill in the retry limit')
        input(f'{Fore.RESET}Press any key to close this window...')
        sys.exit()
    else:
        global retry_limit
        retry_limit = int(settings['Retry_Limit'])
    
    key_settings = (bool(settings['2captcha_key']))

    if key_settings == True:
        global api_key
        api_key = (settings["2captcha_key"])

    else:
        print(f'{Fore.RED}ERROR, Go to the settings.json and fill in the 2captcha API Key')
        print(f'{Fore.RESET}')
        sys.exit()

    global webhook

    if len(settings["Webhook"])==0:
        print(f'{Fore.RED}ERROR; Go on settings.json and fill in the Webhook')
        input(f'{Fore.RESET}Press any key to close this window...')
        sys.exit()
    else:
        webhook = settings['Webhook']

    proxy_error = os.path.getsize(PATH_PROXIES) > 0
    if proxy_error == False:
        print(f'{Fore.RED}ERROR, Add proxies in the proxies.txt file')
        input(f'{Fore.RESET}Press any key to close this window...')
        sys.exit()
    else:
        None

    proxy_count = 0
    account_number = 1

    reset_color = '\033[0m' #reset color

    with open(PATH_WEBDE_PROFILES) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            email = row[0]
            password = row[1]
            firstname = row[2]
            lastname = row[3]
            addressline1 = row[4]
            city = row[5]
            postcode = row[6]
            countrycode = row[7]
            phonenumber = row[8]
            birthday = row[9]
            gender = row[10]

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{account_number}] [{email}] {'Web.de Email Generator: Starting Session'} {reset_color}")

            send_request(email, password, firstname, lastname, addressline1, city, postcode, countrycode, phonenumber, birthday, gender, account_number, proxy_count)

            proxy_count = proxy_count + 1
            account_number = account_number + 1
            


# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup

# if __name__ == '__main__':
#     driver = uc.Chrome()
#     driver.get('https://registrierung.web.de/')
#     time.sleep(5)

#     html_source_code = driver.execute_script("return document.body.innerHTML;")

#     ccguid = html_source_code.split('l?ccguid=')[1].split('"')[0]
#     auth = html_source_code.split('accessToken": "')[1].split('"')[0]
#     soup = BeautifulSoup(html_source_code, 'html.parser')
#     captchaimage = soup.find_all(id="captchaImage")
#     tok = soup.find_all(id='token')
#     token_value = str(tok).split('value=')[1].split('"')[1]
#     image = str(captchaimage).split('src=')[1].split('"')[1]
#     time.sleep(40)
#     module(ccguid, auth, token_value, image)
    

# from selenium import webdriver
# from bs4 import BeautifulSoup

# options = webdriver.ChromeOptions()

# driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
# driver.get("https://registrierung.web.de/")
# time.sleep(5)
# html_source_code = driver.execute_script("return document.body.innerHTML;")
# driver.quit()
# ccguid = html_source_code.split('l?ccguid=')[1].split('"')[0]
# auth = html_source_code.split('accessToken": "')[1].split('"')[0]
# soup = BeautifulSoup(html_source_code, 'html.parser')
# captchaimage = soup.find_all(id="captchaImage")
# tok = soup.find_all(id='token')

# val = str(tok).split('value=')[1].split('"')[1]

# image = str(captchaimage).split('src=')[1].split('"')[1]
# print(image)
# # print(val)

# value = '[<input class="ng-untouched ng-pristine ng-valid" formcontrolname="token" id="token" name="token" type="hidden" value="5iXFnpde21GShl8RnnwCMYVS2Z7YL6ofV09Ae_NblTs"/>]'

# val = value.split('value=')[1].split('"')[1]
# print(val)


