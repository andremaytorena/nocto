from capmonster_python import *
import requests, os, sys, time, datetime, pytz, re, json, base64, urllib, csv, random, threading
from twocaptcha import TwoCaptcha
from py_adyen_encrypt import encryptor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd 
from Paths.paths import PATH_HIPSTORE_LOGS, PATH_HIPSTORE_FOLDER, MAIN_PATH, PATH_CHROME_DRIVER
import RaffleModules.webhook_management as webhooks
from os import path
from selenium.webdriver.chrome.options import Options
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, json2captcha, proxiesfile
from mohawk import Sender

success_entry_count = 0
failed_entry_count = 0

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def write_success_logs(email):

    fieldnames = ['Email', 'Raffle']

    with open(PATH_HIPSTORE_LOGS) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_HIPSTORE_LOGS, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Email':email, 'Raffle':raffle_name}
        ]
        if not has_newline:
            f.write('\n')

        writer.writerows(rows)

def discord_log_entry(email, size):

    webhooks.hipstore_entry_webhook(raffle_name, email, size, image, webhook)
    webhooks.astro_logs("Entered Raffle!", "Footpatrol Launches")

def gen_hawk():
    url = "https://hipstoregb-mosaic-webapp.jdmesh.co"
    content = '' #ANY CONTENT IF U NEED
    content_type = 'application/json' # CONTENT TYPE

    sender = Sender({'id': '4d4f739014',
    'key': 'da2adfc4bf0d6be8986c038f8f2fffd5',
    'algorithm': 'sha256'}, url, "GET", content=content, content_type=content_type)

    headers = {
        "x-api-key": "244343803EAA4F10AE31BEEB10ECF5B8",
        "X-Request-Auth": sender.request_header,
    }

    print(sender.request_header)

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
        'Origin': 'https://hipstoregb-mosaic-webapp.jdmesh.co',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Referer': 'https://hipstoregb-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2',
        'Accept-Language': 'en-gb'
    }

    payload = {
        'PaReq': paReq,
        'MD': md,
        'TermUrl': f'https://mosaic-platform.jdmesh.co/stores/hipstoregb/preAuthorise/{order_id}/payment/3dsecure'
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

    ser = Service(PATH_CHROME_DRIVER)
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
        "TermUrl": f'https://mosaic-platform.jdmesh.co/stores/footpatrolgb/preAuthorise/{order_id}payment/3dsecure?isNewClient=1',
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
    r = session.post(f'https://mosaic-platform.jdmesh.co/stores/hipstoregb/preAuthorise/{order_id}/payment/3dsecure?isNewClient=1', headers=headers, data=payload)
    url = f'https://mosaic-platform.jdmesh.co/stores/hipstoregb/preAuthorise/{order_id}/payment/3dsecure?api_key=09667273333ddbfd1e6b055ae783a89f&channel=android-app-tablet-mosaic'
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
            'Origin': f'https://hipstoregb-mosaic-webapp.jdmesh.co',
            'Connection': 'keep-alive',
            'User-Agent': "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
            'Referer': f'https://hipstoregb-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2'
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
    ADYEN_KEY = '10001|8677B0C92CA9D3FF33C345BD024EBC6235D2A79DEFFCE50F28F517447AECD7D95CD0663842CDB51D63E78AD86EDF4B4D569824B41B161E479909A4B141ED9C1CD7C492B81ECABD4D6984413D456BF4016C09E17283D436AEED0C85B0C9B745D9D19823123100A7D8E0EF8B32ED7191EC740F839D5C91C4A415F7750D1D69CC46DFA3E058007490133993E76C43B2D70B005A7BFA73DD66C652DAAC861B686C891B89B24C54F4F699D0770A2D53BFF29B60DBA42777C3A1C0ACCDA49CDF18382637DDE4123413FBEB897F3BD96B5467A3DB9606764979BCB6480BF497D0C75FFB719A4E54D0612982E0393B1A6BDF25546EE3D6443B9AEF5A1210A10AC2C26259'

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
                url='https://hipstoregb-mosaic-webapp.jdmesh.co',
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
                url='https://hipstoregb-mosaic-webapp.jdmesh.co',
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
        print('TWO CAPTCHA ERROR')
        sys.exit()

def size_capmonster_captcha(website_url, sitekey, action):
        capmonster = RecaptchaV3Task("152d483aa8e2a900e7312d2f99c05ac5")
        task_id = capmonster.create_task(website_url, sitekey, page_action=action)
        result = capmonster.join_task_result(task_id)
        return (result.get("gRecaptchaResponse"))

def enter_raffle(user_id, product_id, product_size_id, size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, proxies, main_count, session):

    for i in range(1):

        headers = {
        'Host': 'mosaic-platform.jdmesh.co',
        'Accept': '*/*',
        'Authorization': gen_hawk(),
        'originalhost': 'mosaic-platform.jdmesh.co',
        'Accept-Language': 'en-gb',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://hipstoregb-mosaic-webapp.jdmesh.co',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'Referer': 'https://hipstoregb-mosaic-webapp.jdmesh.co/?channel=android-app-tablet-mosaic&appversion=2',
        }

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Getting Raffle..'} {reset_color}")
        product_url = f"https://mosaic-platform.jdmesh.co/stores/hipstoregb/user/{user_id}/preauth/product/{product_id}?api_key=09667273333ddbfd1e6b055ae783a89f&channel=android-app-tablet-mosaic"
        product_response = session.get(product_url, proxies=proxies, headers=headers)
        print(product_response.text)
        print(product_url)

        time.sleep(100)

        enter_url = f"https://mosaic-platform.jdmesh.co/stores/hipstoregb/preAuthorise/order?api_key=09667273333ddbfd1e6b055ae783a89f&channel=android-app-tablet-mosaic&userID={user_id}"
    

        payload = {
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
            "ID": "957b232e-d94b-4770-aecd-a5b97cba8669",
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
        # "googleClientID": "1147653153.1672353444"
        }
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Shipping Details'} {reset_color}")
        enter_raffle_response = session.post(enter_url, json=payload, proxies=proxies, headers=headers)
        print(enter_raffle_response.text)

        try:
            if enter_raffle_response.json()['errorInfo'] == 'You have already entered this raffle.':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Already Entered Raffle'} {reset_color}")
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

        put_url = f'https://mosaic-platform.jdmesh.co/stores/hipstoregb/preAuthorise/payment/{order_id}?api_key=09667273333ddbfd1e6b055ae783a89f&channel=android-app-tablet-mosaic&type=CARD'
        

        put_payload = {
        "user": user_id,
        "encryptedData": generate_ayden_data(cardnumber, cardmonth, cardyear, cardcvv, firstname, lastname)
        }

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Payment Details'} {reset_color}")
        put_response = session.put(put_url, json=put_payload, headers=headers, proxies=proxies)

        print(put_response.text)

        try:
            if put_response.json()['status'] == 'failed':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Submit Payment Details: '}{put_response.json()['refusalReason']} {reset_color}")
                entered_status = 'Failed'
                return entered_status
        except:
            None
        try:
            if put_response.json()['successCode'] == 'order-complete':
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Entered Raffle'} {reset_color}")
                write_success_logs(email)
                discord_log_entry(email, size)
                entered_status = 'Entered'
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
        'origin': 'https://hipstoregb-mosaic-webapp.jdmesh.co',
        'originalhost': 'mosaic-platform.jdmesh.co',
        'referer': 'https://hipstoregb-mosaic-webapp.jdmesh.co/',
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
        # "verification": size_captcha('https://size-mosaic-webapp.jdmesh.co', '6LcHpaoUAAAAANZV81xLosUR8pDqGnpTWUZw59hN',"Login/SignUp")
        "verification": size_2captcha(email, main_count)
    }
    login = session.post("https://mosaic-platform.jdmesh.co/stores/hipstoregb/users/login?api_key=09667273333ddbfd1e6b055ae783a89f&channel=android-app-tablet-mosaic", json=login_payload, proxies=proxies)
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

    url = 'https://mosaic-platform.jdmesh.co/admin/stores/hipstoregb/products?MESHKey=B26DC670995711E3A5E20800200C9A66'

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
    if 'CHI' not in size:
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
    
    elif 'CHI' in size:
        for i in range(len(sizes_list)):
            stripped_size = (str(sizes_list[count_sizes]['name']))
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

    for i in range(int(retrylimit)):

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
                    None

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
        os.system(f'title Hipstore Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    
    elif ENTERED_RAFFLE == False:
        failed_entry_count+=1
        os.system(f'title Hipstore Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')

def set_csvs():

    print("")

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_HIPSTORE_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_HIPSTORE_FOLDER, choose_csv[option])
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

    global amount_of_proxy_lines, webhook, twocaptchakey, retrylimit, PATH_PROXIES
    main_count = 0

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    twocaptchakey = json2captcha()
    retrylimit = int(jsonretrylimit())

    
    #gets current open raffles
    os.system(f'title Hipstore Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{0}] {'Getting Open Releases..'} {reset_color}")
    product_id, sizes_list = get_products()

    PROFILES_CSV = set_csvs()

    PATH_PROXIES = set_proxies_file()

    proxiesfile(PATH_PROXIES)

    account_num = 1
    entered_num = 1

    proxy_line = 0
    account_number = 1

    finished_entering = False
    
    results_accounts = pd.read_csv(PROFILES_CSV)
    _linesaccounts = int((len(results_accounts)))

    results_entered = pd.read_csv(PATH_HIPSTORE_LOGS)
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

                    with open(PATH_HIPSTORE_LOGS) as entered:
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

