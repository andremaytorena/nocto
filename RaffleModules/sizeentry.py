from capmonster_python import *
import requests, os, sys, time, datetime, pytz, re, json, base64, urllib, csv, random, threading, chromedriver_autoinstaller
from twocaptcha import TwoCaptcha
from py_adyen_encrypt import encryptor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd 
from Paths.paths import PATH_SIZE_LOGS, PATH_PROXIES, PATH_SIZE_FOLDER, MAIN_PATH
import RaffleModules.webhook_management as webhooks
from os import path
from mohawk import Sender
from selenium.webdriver.chrome.options import Options
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, json2captcha, proxiesfile

success_entry_count = 0
failed_entry_count = 0

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def write_success_logs(email):

    fieldnames = ['Email', 'Raffle']

    with open(PATH_SIZE_LOGS) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_SIZE_LOGS, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Email':email, 'Raffle':raffle_name}
        ]
        if not has_newline:
            f.write('\n')

        writer.writerows(rows)

def discord_log_entry(email, size):

    webhooks.size_entry_webhook(raffle_name, email, size, image, webhook)
    webhooks.astro_logs("Entered Raffle!", "Size Launches")

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

def decode(data:str):
    return json.loads(base64.b64decode(bytes(data,'utf-8')))

def encode(data:dict):
    return str(base64.b64encode(json.dumps(data).replace(' ','').encode()).decode())


def identify3DS(redirect_url, md, paReq, pspReference, order_id, email, proxies, main_count, session, size):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Getting 3DS Browser..'} {reset_color}")

    headers = {
        'Host': 'checkoutshopper-live.adyen.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://size-mosaic-webapp.jdmesh.co',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Referer': 'https://size-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2',
        'Accept-Language': 'en-gb'
    }

    payload = {
        'PaReq': paReq,
        'MD': md,
        'TermUrl': f'https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/{order_id}/payment/3dsecure'
    }
    r = session.post(redirect_url, data=payload, headers=headers, proxies=proxies)
    token = re.search("token: '[^']*'", r.text).group().replace("token: '", '').replace("'", '')
    data = decode(token)
    threeDSData = {
        'acsURL': data['acsURL'],
        'acsTransID': data['acsTransID'],
        'threeDSServerTransID': data['threeDSServerTransID'],
        'messageVersion': data["messageVersion"]
    }


    # PATH_CHROME_DRIVER = os.path.expanduser("~/Desktop/chromedriver")
    ser = Service()
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=ser, options=options, service_log_path='/dev/null')

    transStatus = 'Y'
    driver.get(threeDSData["acsURL"])
    encoded = encode(
        {"acsTransID":threeDSData["acsTransID"],
        "messageVersion": threeDSData["messageVersion"],
        "threeDSServerTransID":threeDSData["threeDSServerTransID"],
        "messageType":"CReq",
        "challengeWindowSize":"03"}
    )
    driver.execute_script(f"""
        var form = document.createElement('form');
        form.method = 'POST';
        form.name = 'form_3ds';
        var inp1 = document.createElement('input');
        inp1.type = 'hidden';
        inp1.name = 'creq';
        inp1.value = '{encoded}';
        form.appendChild(inp1);

        var submit = document.createElement('input');
        submit.type = 'submit';
        form.appendChild(submit);
        document.body.appendChild(form);
        document.forms['form_3ds'].submit();
        """)
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Accept 3DS Notification..'} {reset_color}")
    while True:
        if 'checkoutshopper-live.adyen.com' in driver.current_url:
            transStatus = driver.execute_script("return transStatus")
            driver.close()
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'3DS Accepted!'} {reset_color}")
            break

    headers = {
        'Host': 'checkoutshopper-live.adyen.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://checkoutshopper-live.adyen.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
        'Referer': f'https://checkoutshopper-live.adyen.com/checkoutshopper/threeDS2.shtml?pspReference={pspReference}',
        'Accept-Language': 'en-gb'
    }
    payload = urllib.parse.urlencode({
        "MD": md,
        "PaReq": paReq,
        "TermUrl": f'https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/{order_id}payment/3dsecure?isNewClient=1',
        "transStatus": transStatus,
        "spcSupported": False,
        "webAuthnSupported": False,
        "successfulWebAuthnSupported": False,
        "webAuthnNotPerformedReason": None,
        "self.pspReference": pspReference
    })
    r = session.post('https://checkoutshopper-live.adyen.com/checkoutshopper/challengeShopper.shtml', headers=headers, data=payload, proxies=proxies)
    paRes = re.findall('value="[^"]*"', r.text)[1].replace('value="', '').replace('"', '')
    
    headers = {
        'Host': 'mosaic-platform.jdmesh.co',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://checkoutshopper-live.adyen.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
        'Referer': 'https://checkoutshopper-live.adyen.com/checkoutshopper/challengeShopper.shtml',
        'Accept-Language': 'en-gb'
    }
    payload = urllib.parse.urlencode({
        'MD': md,
        'PaRes': paRes
    })
    r = session.post(f'https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/{order_id}/payment/3dsecure?isNewClient=1', headers=headers, data=payload)
    url = f'https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/{order_id}/payment/3dsecure?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic'
    payload = {}
    content_type = 'text/plain;charset=UTF-8'
    try:
        # sender = genHeaders(url, str(payload), content_type, 'PUT')
        headers = {
            'Host': 'mosaic-platform.jdmesh.co',
            'Accept': '*/*',
            'Authorization': 'undefined',
            'originalhost': 'mosaic-platform.jdmesh.co',
            'Accept-Language': 'en-gb',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': f'https://size-mosaic-webapp.jdmesh.co',
            'Connection': 'keep-alive',
            'User-Agent': "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
            'Referer': f'https://size-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2'
        }
        final_order_response = session.put(url, headers=headers, json=payload, proxies=proxies)
        if str(final_order_response.status_code) == '200':
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Entered Raffle'} {reset_color}")
            write_success_logs(email)
            discord_log_entry(email, size)
            entered_status = 'Entered'
            return entered_status 
        else:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Enter Raffle'} {reset_color}")
            entered_status = 'Not Entered'
            return entered_status
    except:
        print("FAILED")


def generate_ayden_data(cardnumber, cardmonth, cardyear, cardcvv, firstname, lastname):
    ADYEN_KEY = '10001|ABEFDC7DC7BD08EBFABAFADA7433391F4F70FFE6BBB2CE00908FE2983E095FEAC29E5FC04BD26439752949C29323E39283C6F765AE30FE08BB3FAE69BB0C3DF72A16D58C4A102951FEB85A2802D94C8600AED86C9DC41EFE92BB7DF9D3C561479FBB2EC2D4409449C00FE7E63BBEA8813F072AF38198E513C43CDE744A61D02F0CE0F7E25FE79885481F822F79AF3A785E8073F576A64EE739402EAF4D954B2D6F5A1D78911A998298FB43F51CD01066F2249D4A282C4F712256673C041FAC42C67E3BA22F628CCB02082FB45C14D184006DB5F1892D72BBE8B6CC2A97AB1D74E2CB1B5A75C3F61862C0CB2B70D10FF9B634C56A4AC28B24F0CF97EC66C1884F'

    enc = encryptor(ADYEN_KEY, adyen_version='_0_1_18')
    generation_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    data = {
        "holderName": firstname + ' ' + lastname,
        "cvc": cardcvv,
        "number": cardnumber,
        "expiryYear": cardyear,  # XXXX format
        "expiryMonth": cardmonth,
        "generationtime": generation_time
    }
    encoded = enc.encrypt_from_dict(dict_=data)
    
    return encoded

def size_2captcha(email, main_count):
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Solving ReCaptcha..'} {reset_color}")
    
    api_key = os.getenv('APIKEY_2CAPTCHA', twocaptchakey)
    captcha_solved = False
    solver = TwoCaptcha(api_key)

    for i in range(3):
        try:
            result = solver.recaptcha(
                sitekey='6LcHpaoUAAAAANZV81xLosUR8pDqGnpTWUZw59hN',
                url='https://size-mosaic-webapp.jdmesh.co',
                version='v3',
                action="Login/SignUp",
                score=0.9
            )

            captcha_solved = True
            break

        except Exception:
            None

    if captcha_solved == True:
        token = result['code']
        return token
    else:
        print('TWO CAPTCHA OERROR')
        sys.exit()

def size_2captchaentry(email, main_count):
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Solving ReCaptcha..'} {reset_color}")

    api_key = os.getenv('APIKEY_2CAPTCHA', twocaptchakey)
    captcha_solved = False
    solver = TwoCaptcha(api_key)

    for i in range(3):
        try:
            result = solver.recaptcha(
                sitekey='6LcHpaoUAAAAANZV81xLosUR8pDqGnpTWUZw59hN',
                url='https://size-mosaic-webapp.jdmesh.co',
                version='v3',
                action="PreAuth_Create",
                score=0.9
        )

            captcha_solved = True
            break

        except Exception:
            None

    if captcha_solved == True:
        token = result['code']
        return token
    else:
        print('TWO CAPTCHA OERROR')
        sys.exit()

def size_capmonster_captcha(website_url, sitekey, action):
        capmonster = RecaptchaV3Task("152d483aa8e2a900e7312d2f99c05ac5")
        task_id = capmonster.create_task(website_url, sitekey, page_action=action)
        result = capmonster.join_task_result(task_id)
        return (result.get("gRecaptchaResponse"))

def enter_raffle(user_id, product_id, product_size_id, size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, proxies, main_count, session):

    for i in range(1):
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Getting Raffle..'} {reset_color}")
        product_url = f"https://mosaic-platform.jdmesh.co/stores/size/user/{user_id}/preauth/product/{product_id}?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic"
        product_response = session.get(product_url, proxies=proxies)

        enter_url = f"https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/order?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic&userID={user_id}"

        headers = {
            'Host': 'mosaic-platform.jdmesh.co',
            'Accept': '*/*',
            'Authorization': gen_hawk(),
            'originalhost': 'mosaic-platform.jdmesh.co',
            'Accept-Language': 'en-gb',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://size-mosaic-webapp.jdmesh.co',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Referer': 'https://size-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2'
        }

        payload =   {
        "customer": {
            "isPrefilled": False,
            "firstName": firstname,
            "lastName": lastname,
            "email": email,
            "phone": phonenumber
        },
        "delivery": {
            "isPrefilled": False,
            "firstName": firstname,
            "lastName": lastname,
            "postcode": postcode,
            "address1": addressline1,
            "address2": addressline2,
            "town": city,
            "county": "",
            "locale": "gb"
        },
        "billing": {
            "isPrefilled": False,
            "firstName": firstname,
            "lastName": lastname,
            "postcode": postcode,
            "address1": addressline1,
            "address2": addressline2,
            "town": city,
            "county": "",
            "locale": "gb"
        },
        "deliveryMethod": {
            "isPrefilled": False,
            "ID": "e2f78b7b-25b5-437b-abbd-099f51a6d75a",
            "name": "Standard Delivery (Delivered by DPD)",
            "price": {
            "amount": "4.49",
            "currency": "GBP"
            },
            "type": "delivery",
            "charity": False,
            "launchDay": False
        },
        "optionID": product_size_id,
        "productID": product_id,
        "verification": size_2captchaentry(email, main_count),
        "googleClientID": "1855824786.1672353384"
        }
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Shipping Details'} {reset_color}")
        enter_raffle_response = session.post(enter_url, json=payload, proxies=proxies, headers=headers)

        print(enter_raffle_response.text)

        try:
            if enter_raffle_response.json()['errorInfo'] == 'You have already entered this raffle.':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Already Entered Raffle'} {reset_color}")
                write_success_logs(email)
                entered_status = 'Already Entered'
                return entered_status
        except:
            None    
        
        try:
            order_id = enter_raffle_response.json()['orderID']
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Add Shipping Details'} {reset_color}")
            entered_status = 'Failed'
            return entered_status


        put_url = f'https://mosaic-platform.jdmesh.co/stores/size/preAuthorise/payment/{order_id}?api_key=0ce5f6f477676d95569067180bc4d46d&channel=android-app-tablet-mosaic&type=CARD'
        
        headers = {
        'Host': 'mosaic-platform.jdmesh.co',
        'Accept': '*/*',
        'Authorization': gen_hawk(),
        'originalhost': 'mosaic-platform.jdmesh.co',
        'Accept-Language': 'en-gb',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://size-mosaic-webapp.jdmesh.co',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Referer': 'https://size-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2'
        }

        put_payload = {
        "user": user_id,
        "encryptedData": generate_ayden_data(cardnumber, cardmonth, cardyear, cardcvv, firstname, lastname)
        }

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Payment Details'} {reset_color}")
        put_response = session.put(put_url, json=put_payload, headers=headers, proxies=proxies)

        try:
            if put_response.json()['status'] == 'failed':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Submit Payment Details: '}{put_response.json()['refusalReason']} {reset_color}")
                entered_status = 'Failed'
                return entered_status

        except:
            None
        try:
            if put_response.json()['successCode'] == 'order-complete':
                entered_status = 'Entered'
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Entered Raffle'} {reset_color}")
                write_success_logs(email)
                discord_log_entry(email, size)
                return entered_status
        except:
            None

        try:
            redirect_url = put_response.json()['redirectUrl']
            md = put_response.json()['md']
            paReq = put_response.json()['paReq']
            pspReference = str(redirect_url).split('=')[1]

            entered_status = identify3DS(redirect_url, md, paReq, pspReference, order_id, email, proxies, main_count, session, size)
            return entered_status
        except:
            None
    


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
    
    # try:
    #     if login.json()['errorInfo'] == 'Credentials supplied were not recognised':
    #         login_status = 'Fauled to Log In'
    #         user_id = 'null'
    #         return user_id, login_status
    # except:
    #     None

    if str(login.status_code) == '200':
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Logged In'} {reset_color}")
        user_id = login.json()['customer']['userID']
        login_status = 'Logged In'
        return user_id, login_status
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Log In'} {reset_color}")
        login_status = 'Not Logged In'
        user_id = 'null'
        return user_id, login_status


def get_products():

    global raffle_name, image

    url = 'https://mosaic-platform.jdmesh.co/stores/size/content?api_key=0ce5f6f477676d95569067180bc4d46d&channel=iphone-mosaic'

    res = requests.get(url)
    jsonresponse= res.json()

    count = 0
    new_count = 0

    products_list = []

    for i in range(len(jsonresponse['products'])):

        if jsonresponse['products'][count]['status'] == 'available':
            name = jsonresponse['products'][count]['name']
            subname = jsonresponse['products'][count]['subTitle']

            print(str(new_count)+ '.', name, subname)
                
            products_list.append(jsonresponse['products'][count])

            new_count+=1

        count+=1

    print("")
    option = int(input('Option: '))
    sizes_list = (products_list[option]['options'])

    raffle_name = products_list[option]['name'] + ' ' + products_list[option]['subTitle']
    image = products_list[option]['mainImage']['original']
    
    product_id = str(products_list[option]['options'][0]['optionID']).split(':')[0]
    return product_id, sizes_list
    
def get_size(sizes_list, size):

    count_sizes = 0
    for i in range(len(sizes_list)):
        stripped_size = (str(sizes_list[count_sizes]['name']).split('|')[0])[:-1]
        if stripped_size == size:
            product_size_id = sizes_list[count_sizes]['optionID']
            eligible_size = True
            break
        else:
            eligible_size = False

        count_sizes+=1

    if eligible_size == True:
        None
    elif eligible_size == False:
        sys.exit('size not found')

    return product_size_id

    
            
def start(size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, product_id, sizes_list, main_count):

    global entered_status, success_entry_count, failed_entry_count

    ENTERED_RAFFLE = False

    session = requests.Session()

    if len(cardyear) == 2:
        cardyear = '20' + cardyear
    
    if '+44' in phonenumber:
        phonenumber = '0' + phonenumber[3:]
    elif len(phonenumber) == 10:
        phonenumber = '0' + phonenumber

    for i in range(retrylimit):

        for i in range(1):
            
            for i in range(3): #retry number for getting proxy
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
                    break
                except:
                    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{0}] {'No Proxies Found'} {reset_color}")
                    input('Press Enter to Exit: ')
                    sys.exit()
            
            product_size_id = get_size(sizes_list, size)
    
            user_id, login_status = login(email, password, proxies, main_count, session)
            if login_status == 'Logged In':
                None
            else: 
                break
            
            entered_status = enter_raffle(user_id, product_id, product_size_id, size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, proxies, main_count, session)
            if entered_status == 'Not Entered':
                None
            elif entered_status == 'Failed':
                None
            elif entered_status == 'Entered':
                ENTERED_RAFFLE = True
                break
            elif entered_status == 'Already Entered':
                break
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Error: Make sure that your phone format is: 07484882283 and cc month: 2027'} {reset_color}")
                break

        
        if login_status == 'Logged In':
            if entered_status == 'Not Entered':
                None
            elif entered_status == 'Failed':
                None
            elif entered_status == 'Entered':
                break
            elif entered_status == 'Already Entered':
                break
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Error: Make sure that your phone format is: 07484882283 and cc month: 2027'} {reset_color}")
                None
        else:
            break

    
    if ENTERED_RAFFLE  == True:
        success_entry_count+=1
        os.system(f'title Size Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    
    elif ENTERED_RAFFLE == False:
        failed_entry_count+=1
        os.system(f'title Size Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')

    
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


def CheckEntryStatus(): # Opens accounts csv and gets account

    global amount_of_proxy_lines, webhook, twocaptchakey, retrylimit
    main_count = 0

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    twocaptchakey = json2captcha()
    retrylimit = int(jsonretrylimit())
    
    #gets current open raffles
    os.system(f'title Size Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{0}] {'Getting Open Releases..'} {reset_color}")
    product_id, sizes_list = get_products()

    PROFILES_CSV = set_csvs()
    
    PATH_PROXIES = set_proxies_file()

    chromedriver_autoinstaller.install()

    proxiesfile(PATH_PROXIES)

    account_num = 1
    entered_num = 1

    proxy_line = 0
    account_number = 1

    finished_entering = False
    
    results_accounts = pd.read_csv(PROFILES_CSV)
    _linesaccounts = int((len(results_accounts)))

    results_entered = pd.read_csv(PATH_SIZE_LOGS)
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
                            cardnumber = row[10]
                            cardmonth = row[11]
                            cardyear = row[12]
                            cardcvv = row[13]
                    except IndexError:
                        finished_entering = True
                        break

                    with open(PATH_SIZE_LOGS) as entered:
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
                    try:
                        thread = threading.Thread(target=start, args=[size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, product_id, sizes_list, main_count])
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

        if error == 1:
            None
        else:
            thread.join()
            time.sleep(delay)
        




