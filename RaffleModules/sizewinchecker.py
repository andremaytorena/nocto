import requests, time, os, sys, csv, random, json, threading
from twocaptcha import TwoCaptcha
from Paths.paths import PATH_PROXIES, PATH_SIZE_FOLDER, PATH_SETTINGS, MAIN_PATH
from os import path
import RaffleModules.webhook_management as webhooks
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, json2captcha, proxiesfile

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def size_2captcha(email, main_count):
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Solving ReCaptcha..'} {reset_color}")
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


def check_win(user_id, proxies, raffle_id, email, main_count, session, password):

    url = f'https://mosaic-platform.jdmesh.co/stores/size/user/{user_id}/preauth?api_key=0ce5f6f477676d95569067180bc4d46d&channel=iphone-mosaic'

    win_response = requests.get(url, proxies=proxies).json()

    count = 0

    # print(win_response['orders'])
    if len(win_response['orders']) == 0:
        win_found = False

    for i in range(len(win_response['orders'])):
        
        current_wins = win_response['orders'][count]['product']['name'] + ' ' + win_response['orders'][count]['product']['subTitle']

        if current_wins == raffle_id:
            win_found = True
            break
        else:
            count+=1
            win_found = False

    if win_found == True:
        if win_response['orders'][count]['status'] == 'looser_processed':
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Unsucessful Entry: '}{win_response['orders'][count]['status']} {reset_color}")
        else:
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Win Logged: '}{win_response['orders'][count]['status']} {reset_color}")
            title = win_response['orders'][count]['product']['name']
            option_size = win_response['orders'][count]['product']['option']
            image = win_response['orders'][count]['product']['mainImage']['original']
            orderstatus = win_response['orders'][count]['orderStatus']
            addressline1 = win_response['orders'][count]['address']['address1']
            addressline2 = win_response['orders'][count]['address']['address2']
            postcode = win_response['orders'][count]['address']['postcode']

            webhooks.size_winchecker_webhook(title, option_size, image, orderstatus, addressline1, addressline2, postcode, email, password, webhook)
            webhooks.astro_logs("Win Found!", "Size Launches")

    elif win_found == False:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'No Entry Found'} {reset_color}")

def load_entries(user_id, proxies, session):

    url = f'https://mosaic-platform.jdmesh.co/stores/size/user/{user_id}/preauth?api_key=0ce5f6f477676d95569067180bc4d46d&channel=iphone-mosaic'

    entries_response = session.get(url, proxies=proxies).json()
    
    orderlist = entries_response['orders']
    
    product_count = 0
    productlist = []
    for i in range(len(orderlist)):
        title = orderlist[product_count]['product']['name']
        subtitle = orderlist[product_count]['product']['subTitle']

        print(str(product_count) + '. ' + title + subtitle)

        productlist.append(orderlist[product_count])

        product_count+=1
    
    print("")
    option = int(input("Option: "))
    # raffle_id = productlist[option]['id']
    raffle_id = productlist[option]['product']['name'] + ' ' + productlist[option]['product']['subTitle']
    
    return raffle_id


def login(email, password, proxies, main_count, session):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Logging in..'} {reset_color}")

    session.headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'undefined',
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
    login_payload = {
        "guestUser": False,
        "loggedIn": False,
        "firstName": "",
        "lastName": "",
        "password": password,
        "password2": "",
        "username": email,
        "billing": {
            "firstName": "",
            "lastName": "",
            "address1": "",
            "address2": "",
            "town": "",
            "county": "",
            "postcode": "",
            "locale": "",
            "phone": ""
        },
        "delivery": {
            "firstName": "",
            "lastName": "",
            "address1": "",
            "address2": "",
            "town": "",
            "county": "",
            "postcode": "",
            "locale": "gb",
            "phone": "",
            "useAsBilling": True
        },
        "verification": size_2captcha(email, main_count)
    }

    login = session.post("https://mosaic-platform.jdmesh.co/stores/size/users/login?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic", json=login_payload, proxies=proxies)
    
    if str(login.status_code) == '200':
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Logged In'} {reset_color}")
        user_id = login.json()['customer']['userID']
        login_status = 'Logged In'
        return user_id, login_status
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Log In'} {reset_color}")
        login_status = 'Not Logged In'
        user_id = 'null'
        return user_id, login_status


def get_proxy():

    for i in range(3):
        try:
            random_proxy_number = random.randint(0,int(amount_of_proxy_lines))
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
            return proxies
        except:
            None


def set_csvs():

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_SIZE_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_SIZE_FOLDER, choose_csv[option])
    print("")
    return PROFILES_CSV



def main_checks(email, password, proxies, raffle_id, main_count):

    for i in range(retrylimit):

        session = requests.Session()
        
        user_id, login_status = login(email, password, proxies, main_count, session)

        if login_status == 'Logged In':
            check_win(user_id, proxies, raffle_id, email, main_count, session, password)
            break
        else:
            None

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
    global amount_of_proxy_lines, twocaptchakey, retrylimit, webhook
    main_count = 1
    finished_entering = False
    account_num = 1

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    twocaptchakey = json2captcha()
    retrylimit = int(jsonretrylimit())

    PROFILES_CSV = set_csvs()

    PATH_PROXIES = set_proxies_file()

    proxiesfile(PATH_PROXIES)

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())

    for i in range(1):
        with open(PROFILES_CSV) as accounts:
            mycsv = accounts.readlines()
            y = mycsv[account_num].rstrip('\n')
            row = y.split(",")
            email = row[1]
            password = row[2]

        proxies = get_proxy()
        session = requests.Session()
        user_id, login_status = login(email, password, proxies, main_count, session)
        print("")

        if login_status == 'Logged In':
            None
        else:
            break

        raffle_id = load_entries(user_id, proxies, session)
        
        while finished_entering == False:

            for i in range(threads):
                try:
                    with open(PROFILES_CSV) as accounts:
                        mycsv = accounts.readlines()
                        y = mycsv[account_num].rstrip('\n')
                        row = y.split(",")
                        email = row[1]
                        password = row[2]
                except IndexError:
                    finished_entering = True
                    break

                proxies = get_proxy()

                # check_win(user_id, proxies, raffle_id, email)
                thread = threading.Thread(target=main_checks, args=[email, password, proxies, raffle_id, main_count])
                thread.start()

                main_count+=1
                account_num+=1

            thread.join()
            time.sleep(delay)




