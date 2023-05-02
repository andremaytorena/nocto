import requests, csv, random, string, time, json, sys, os
from Paths.paths import PATH_FOOTPATROL_ACCGENPROFILES, MAIN_PATH
import threading
import RaffleModules.webhook_management as webhooks
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, proxiesfile
from os import path

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def gen_postcode():
    postcode_response = requests.get('https://api.postcodes.io/random/postcodes').json()

    postcode = (postcode_response['result']['postcode'])
    return postcode

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

def gen_acc(email, password, firstname, lastname, proxies, count):

    session = requests.Session()
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "424",
        "content-type": "application/json",
        "origin": "https://www.footpatrol.com",
        "referer": "https://www.footpatrol.com/myaccount/register/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    payload = {
        "addressPredictflag": "false",
        "billingAddress1":''.join(random.choice(string.ascii_uppercase) for _ in range(3)),
        "billingCountry": "United Kingdom|gb",
        "billingPostcode": gen_postcode(),
        "billingTown": ''.join(random.choice(string.ascii_uppercase) for _ in range(3)),
        "confirmPassword": password,
        "deliveryAddressPredictFlag": "false",
        "email": email,
        "firstName": firstname,
        "lastName": lastname,
        "password": password,
        "phone": gen_phone(),
        "saveDetails": "on",
        "shippingCountry": "United Kingdom|gb",
        "useBillingAddress": "on"
    }
    url = 'https://www.footpatrol.com/myaccount/registerCustomer/'
    res = session.post(url, json=payload, headers=headers, proxies=proxies)

    try:
        if res.json()['success']['message'] == 'Your account has been created':
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{count}] {'Successfully Generated Account'} {reset_color}")
            webhooks.footpatrol_accgen_webhook(email, password, webhook)
            webhooks.astro_logs("Account Generated!", "Footpatrol Launches")
        else:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{count}] {'Failed to Generate Account'} {reset_color}")
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{count}] {'Failed to Generate Account: '}{res.json()['error']['message']} {reset_color}")

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

    global webhook

    finished_entering = False

    proxy_count = 0
    count = 1
    profiles_line_number = 1

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())

    PATH_PROXIES = set_proxies_file()

    proxiesfile(PATH_PROXIES)

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())

    while finished_entering == False:

        for i in range(threads): #amount of threads

            try:
                with open(PATH_FOOTPATROL_ACCGENPROFILES) as accounts:
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

            thread = threading.Thread(target=gen_acc, args=[email, password, firstname, lastname, proxies, count])
            thread.start()

            proxy_count+=1
            count+=1
            profiles_line_number+=1
        
        thread.join()
        time.sleep(delay)
