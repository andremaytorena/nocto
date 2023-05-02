from mohawk import Sender
import requests, os, time, sys, csv, random, string, json
from twocaptcha import TwoCaptcha
from Paths.paths import PATH_SETTINGS, PATH_PROXIES, PATH_SIZE_ACCGENPROFILES, MAIN_PATH
import RaffleModules.webhook_management as webhooks
import threading
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonentrydelay, json2captcha, proxiesfile
from os import path

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def gen_hawk():
    url = "https://size-mosaic-webapp.jdmesh.co"
    content = '' #ANY CONTENT IF U NEED
    content_type = 'application/json' # CONTENT TYPE

    sender = Sender({'id': 'e27d1ea0',
    'key': '0ce5f6f477676d95569067180bc4d46d',
    'algorithm': 'sha256'}, url, "GET", content=content, content_type=content_type)

    headers = {
        "x-api-key": "GT0P5LZCT9364QEH2WVK3YVKT6P467S3",
        "X-Request-Auth": sender.request_header,
    }

    return sender.request_header

def size_2captcha(email, count):
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Solving ReCaptcha..'} {reset_color}")
    api_key = os.getenv('APIKEY_2CAPTCHA', twocaptchakey)

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey='6LcHpaoUAAAAANZV81xLosUR8pDqGnpTWUZw59hN',
            url='https://size-mosaic-webapp.jdmesh.co',
            version='v3',
            action="Login/SignUp",
            score=0.9
        )

    except Exception as e:
        sys.exit(e)

    else:
        token = result['code']
        return token

def gen_phone():
    num1 = random.randint(0,9)
    num2 = random.randint(0,9)
    num3 = random.randint(0,9)
    num4 = random.randint(0,9)
    num5 = random.randint(0,9)
    num6 = random.randint(0,9)
    num7 = random.randint(0,9)
    num8 = random.randint(0,9)
    num9 = random.randint(0,9)
    num10 = random.randint(0,9)

    phone = ('+44')+ str(num1) + str(num2) + str(num3) + str(num4) + str(num5) + str(num6) + str(num7) + str(num8) + str(num9) + str(num10)
    return phone

def gen_postcode():
    postcode_response = requests.get('https://api.postcodes.io/random/postcodes').json()

    postcode = (postcode_response['result']['postcode'])
    return postcode

def signup_loyalty(user_id, count, email, proxies, session):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Adding Size? Access'} {reset_color}")
    
    url = f'https://mosaic-platform.jdmesh.co/stores/size/users/{user_id}/loyalty?api_key=0ce5f6f477676d95569067180bc4d46d&channel=iphone-mosaic'

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': gen_hawk(),
        'connection': 'keep-alive',
        'content-type': 'text/plain;charset=UTF-8',
        'host': 'mosaic-platform.jdmesh.co',
        'origin': 'https://size-mosaic-webapp.jdmesh.co',
        'originalhost': 'mosaic-platform.jdmesh.co',
        'referer': 'https://size-mosaic-webapp.jdmesh.co/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'x-requested-with': 'fp.launch'
    }
    payload = {
        "optedIn": True,
        "birthday": {
            "day": 12,
            "month": 9,
            "year": 1995
        },
        "favoriteBrand": "Nike",
        "gender": "male",
        "shoeSize": "9",
        "email": email,
        "phone": gen_phone()
        }
    
    loyalty_response = session.post(url, json=payload, headers=headers, proxies=proxies)
    try:
        if loyalty_response.json()['successInfo'] == 'Loyalty Activated':
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Successfully Added Size? Access'} {reset_color}")
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Failed to Add Size? Access: '}{loyalty_response.json()['errorInfo']} {reset_color}")

def gen_acc(email, password, firstname, lastname, proxies, count):

    session = requests.Session()

    url = 'https://mosaic-platform.jdmesh.co/stores/size/users/signup?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic'

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': gen_hawk(),
        'connection': 'keep-alive',
        'content-type': 'text/plain;charset=UTF-8',
        'host': 'mosaic-platform.jdmesh.co',
        'origin': 'https://size-mosaic-webapp.jdmesh.co',
        'originalhost': 'mosaic-platform.jdmesh.co',
        'referer': 'https://size-mosaic-webapp.jdmesh.co/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'x-requested-with': 'fp.launch'
    }
    
    payload = {
    "guestUser": False,
    "loggedIn": False,
    "firstName": firstname,
    "lastName": lastname,
    "password": password,
    "addresses": [
        {
        "firstName": firstname,
        "lastName": lastname,
        "address1": ''.join(random.choice(string.ascii_uppercase) for _ in range(3)),
        "address2": "",
        "town": ''.join(random.choice(string.ascii_uppercase) for _ in range(3)),
        "county": "",
        "postcode": gen_postcode(),
        "locale": "gb",
        "phone": "",
        "isPrimaryAddress": True,
        "isPrimaryBillingAddress": True
        }
    ],
    "email": email,
    "verification": size_2captcha(email, count)
    }

    gen_response = session.post(url,json=payload, headers=headers, proxies=proxies)

    try:
        user_id = gen_response.json()['customer']['userID']
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Successfully Generated Account'} {reset_color}")
        webhooks.size_accgen_webhook(email, password, webhook)
        webhooks.astro_logs("Account Generated!", "Size Launches")
        signup_loyalty(user_id, count, email, proxies, session)
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Failed to Generate Account: '}{gen_response.json()['errorInfo']} {reset_color}")

def set_proxies_file():

    print("")

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

def start():

    global twocaptchakey, webhook

    finished_entering = False

    proxy_count = 0
    count = 0
    profiles_line_number = 1

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    twocaptchakey = json2captcha()

    PATH_PROXIES = set_proxies_file()

    proxiesfile(PATH_PROXIES)

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())
    
    while finished_entering == False:

        for i in range(threads): #amount of threads

            try:
                with open(PATH_SIZE_ACCGENPROFILES) as accounts:
                    mycsv = accounts.readlines()
                    x = mycsv[profiles_line_number].rstrip('\n')
                    x = x.split(",")
                    row = x
                    email = row[0]
                    password = row[1]
                    firstname = row[2]
                    lastname = row[3]
            except IndexError:
                finished_entering = True
                break
            
            for i in range(3):
                random_proxy_number = random.randint(0,int(amount_of_proxy_lines))
                try:
                    with open(PATH_PROXIES) as file:
                        myproxies = file.readlines()
                        x = myproxies[random_proxy_number].rstrip('\n')
                        x = x.split(":")
                        proxies = x

                        PROXY_HOST = proxies[0]
                        PROXY_PORT = proxies[1]
                        PROXY_USER = proxies[2]
                        PROXY_PASS = proxies[3]

                    PROXY = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
                    proxies = {
                        "http": PROXY,
                        "https": PROXY,
                    }   
                    break
                except:
                    None

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Generating Account..'} {reset_color}")

            # gen_acc(email, password, firstname, lastname, proxies, count)
            thread = threading.Thread(target=gen_acc, args=[email, password, firstname, lastname, proxies, count])
            thread.start()

            proxy_count+=1
            count+=1
            profiles_line_number+=1
        
        thread.join()
        time.sleep(delay)


