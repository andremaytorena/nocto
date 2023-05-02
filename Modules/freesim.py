import csv, names, time, random, os, sys, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
from Paths.paths import PATH_SIMCARDS_PROFILES, PATH_CHROME_DRIVER
import Modules.jsonerrorlogs as jsonerrorlogs

def log_success(order_success):
    owner_success_json = {
        "content": None,
        "embeds": [
            {
            "title": "Sim Card Generated",
            "color": None,
            "fields": [
                {
                "name": "Company:",
                "value": order_success
                }
            ]
            }
        ],
        "attachments": []
        }

    requests.post('https://discord.com/api/webhooks/1039291702692810762/MBAgb9wI-tHHXc2T7UR7b24T0wMBEy_RY6eC7bIXvie2puCLsV67wIF7ip4TeonloRZm', json=owner_success_json)

    requests.post(webhook, json=owner_success_json)

def solver(api_key, count, sitekey, url, store):
        
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    api_key = os.getenv('APIKEY_2CAPTCHA', api_key)

    solver = TwoCaptcha(api_key)

    if store == 'THREE':   
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Three Sim: Solving HCaptcha...'} {reset_color}")
        try:
            result = solver.hcaptcha(
                sitekey=sitekey,
                url=url,
            )
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Three Sim: Failed Captcha Solved'} {reset_color}")

        else:
            code = (result['code'])
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Three Sim: Captcha Solved'} {reset_color}")
            return code

    elif store == 'O2':
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'02 Sim: Solving HCaptcha...'} {reset_color}")
        try:
            result = solver.recaptcha(
                sitekey='6Ldu0RETAAAAAFRTCzycHREmOKJzX3ZCutyhHjEc',
                url='https://www.o2.co.uk/shop/sim-cards/pay-as-you-go/delivery?planId=2c87f734-a2c0-4903-855e-55714d08a75d',
            )
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'O2 Sim: Failed Captcha Solved'} {reset_color}")


        else:
            code = (result['code'])
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'O2 Sim: Captcha Solved'} {reset_color}")
            return code
        
    elif store == 'TESCO':
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Tesco Sim: Solving HCaptcha...'} {reset_color}")
        try:
            result = solver.recaptcha(
                sitekey='6LcfnMcZAAAAAO8f8ZhypqPrpRYu6954VPkM1IEa',
                url='https://www.tescomobile.com/order-sim',
                invisible=1
            )
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Tesco Sim: Failed Captcha Solved'} {reset_color}")


        else:
            code = (result['code'])
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Tesco Sim: Captcha Solved'} {reset_color}")
            return code


def three_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key):

    phone = '0'
    for i in range(10):
        number = random.randint(1,9)
        phone = phone + str(number)

    email = firstname + lastname
    for i in range(3):
        number = random.randint(1,9)
        email = email + str(number)
    email = email + "@gmail.com"

    code = solver(api_key, count, '28d6ff2e-5725-4d95-a4b8-2c0a400fd47c', 'https://www.three.co.uk/Support/Free_SIM/Order', 'THREE')

    payload = {
        'address2': addy2,
        'addressDropdown': "",
        'confirmemail': email,
        'email': email,
        'existingContactNumber':phone,
        'firstname': firstname,
        'g-recaptcha-response': code,
        'h-captcha-response': code,
        'hiddenField': "tr-triosim",
        "marketingPrefs": "Yes",
        'postcode': postcode,
        'street': addy1,
        'surname': lastname,
        'town': city,
        '_failure_url': "",
        '_form_url': "",
        '_success_url': "/Support/Free_SIM/Order_Confirmation",
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "3453",
        "Content-Type": "application/json",
        "Host": "www.three.co.uk",
        "Origin": "https://www.three.co.uk",
        "Referer": "https://www.three.co.uk/Support/Free_SIM/Order",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }

    res = requests.post('https://www.three.co.uk/cs/form/freesimreg', json=payload, headers=headers)
    jsonstatus = (res.json())
    status = (jsonstatus["status"])

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red
    
    if status == 'success':
        data = (jsonstatus["data"])
        order_success = 'Three'

        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Three Sim: Successfully Ordered Three Sim Card: '}{data} {reset_color}")
        
        log_success(order_success)

    elif status == 'fail':
        message = (jsonstatus["message"])

        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Three Sim: Failed to Order Sim Card: '}{message} {reset_color}")


def giffgaff(addy1, addy2, postcode, city, count, firstname, lastname):
    for i in range(1):

        email = firstname + lastname
        for i in range(3):
            number = random.randint(1,9)
            email = email + str(number)
        email = email + "@gmail.com"
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument('--headless')
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        try:
            driver = webdriver.Chrome(options=chrome_options, executable_path=PATH_CHROME_DRIVER)
        except:
            jsonerrorlogs.updateChromeDriver()
            driver = webdriver.Chrome(options=chrome_options, executable_path=PATH_CHROME_DRIVER)

        try:
            driver.get('https://www.giffgaff.com/free-sim-cards')

            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            red_color = '\033[91m' #red
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Getting URL'} {reset_color}")


            for i in range(3):
                try:
                    driver.find_element(By.XPATH, '//*[@id="cookie-banner"]/div/div[2]/a[1]').click()
                    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Successfully Accepted Cookies'} {reset_color}")
                    break
                except:
                    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Failed Accepting Cookies'} {reset_color}")
                    time.sleep(2)

            
            driver.find_element(By.XPATH, '//*[@id="choose-later-link"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="submitButton"]').click()
            time.sleep(1)
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Adding Information'} {reset_color}")
            driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(firstname)
            driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(lastname)
            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(email)
            driver.find_element(By.XPATH, '//*[@id="line1"]').send_keys(addy1)
            driver.find_element(By.XPATH, '//*[@id="line2"]').send_keys(addy2)
            driver.find_element(By.XPATH, '//*[@id="city"]').send_keys(city)
            driver.find_element(By.XPATH, '//*[@id="postcode"]').send_keys(postcode)
            time.sleep(2)

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Submitting Information'} {reset_color}")
            driver.find_element(By.XPATH, '//*[@id="submitButton"]').click()
            time.sleep(2)
        
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Browser Error!'} {reset_color}")

        try:
            driver.find_element(By.XPATH, '//*[@id="submitButton"]').click()
        except:
            None
        time.sleep(5)
        
        try:
            success = driver.find_element(By.XPATH, '//*[@id="register-top"]/div[1]/h1').text
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Ordered Giff Gaff Sim Card (shitty website): '}{success} {reset_color}")
            order_success = 'Giff Gaff'
            log_success(order_success)
            break
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Giff Gaff Sim: Failed to Order Sim Card'} {reset_color}")
            time.sleep(2)


def o2_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key):

        phone = '0'
        for i in range(10):
            number = random.randint(1,9)
            phone = phone + str(number)

        email = firstname + lastname
        for i in range(3):
            number = random.randint(1,9)
            email = email + str(number)
        email = email + "@gmail.com"

        code = solver(api_key, count, '6Ldu0RETAAAAAFRTCzycHREmOKJzX3ZCutyhHjEc', 'https://www.o2.co.uk/shop/sim-cards/pay-as-you-go/delivery?planId=2c87f734-a2c0-4903-855e-55714d08a75d', 'O2')

        payload = {
            "email": email,
            "title": "Mr",
            "firstName": firstname,
            "lastName": lastname,
            "mobile": phone,
            "address.officeOrFlat": "",
            "address.houseNameOrNumber": addy1,
            "address.line1": addy2,
            "address.line2": "",
            "address.town": city,
            "address.postcode": postcode,
            "simType": "TSIM",
            "simCount": "1",
            "campaign": "Direct",
            "tariffType": "PAYG",
            "country": "",
            "tariffPlan": "rolling-plan",
            "sku": "24GRROVN",
            "tariffId": "2c87f734-a2c0-4903-855e-55714d08a75d",
            "tariffCost": "20",
            "marketingInfo": "1",
            "accessibilityPreference": "Standard format",
            "recaptchaResponse": code 
        }

        headers = {
            "origin": "https://www.o2.co.uk",
            "referer": "https://www.o2.co.uk/shop/sim-cards/pay-as-you-go/delivery?planId=2c87f734-a2c0-4903-855e-55714d08a75d",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        

        res = requests.post("https://www.o2.co.uk/shop/ajax/sim-cards/pay-as-you-go/order/submit", data=payload, headers=headers)

        if str(res.status_code) == '200':
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'02 Sim: Successfully Ordered 02 Sim Card'} {reset_color}")
            order_success = '02'
            log_success(order_success)

        else:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'02 Sim: Failed to Order Sim Card'} {reset_color}")


def vodaphone(addy1, addy2, postcode, city, count, firstname, lastname):

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    for i in range(1):

        email = firstname + lastname
        for i in range(3):
            number = random.randint(1,9)
            email = email + str(number)
        email = email + "@gmail.com"
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        try:
            driver = webdriver.Chrome(options=chrome_options, executable_path=PATH_CHROME_DRIVER)
        except:
            jsonerrorlogs.updateChromeDriver()
            driver = webdriver.Chrome(options=chrome_options, executable_path=PATH_CHROME_DRIVER)
        
        try:

            driver.get('https://freesim.vodafone.co.uk/check-out-payasyougo-campaign')

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Getting URL'} {reset_color}")

            time.sleep(2)
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Accepting Cookies..'} {reset_color}")
            driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

            time.sleep(2)
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Adding Information'} {reset_color}")
            driver.switch_to.frame(0)
            driver.find_element(By.XPATH, '//*[@id="txtFirstName"]').send_keys(firstname)
            driver.find_element(By.XPATH, '//*[@id="txtLastName"]').send_keys(lastname)
            driver.find_element(By.XPATH, '//*[@id="txtEmail"]').send_keys(email)
            driver.find_element(By.XPATH, '//*[@id="txtPostCodeLookup"]').send_keys('W9 1PN')
            driver.find_element(By.XPATH, '//*[@id="l-trigger-find-address"]').click()
            driver.find_element(By.XPATH, '//*[@id="addressLookup"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="addressLookup"]/option[2]').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="txtAddress1"]').clear()
            driver.find_element(By.XPATH, '//*[@id="txtAddress2"]').clear()
            driver.find_element(By.XPATH, '//*[@id="txtTownCity"]').clear()
            driver.find_element(By.XPATH, '//*[@id="txtPostCode"]').clear()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="txtAddress1"]').send_keys(addy1)
            driver.find_element(By.XPATH, '//*[@id="txtAddress2"]').send_keys(addy2)
            driver.find_element(By.XPATH, '//*[@id="txtTownCity"]').send_keys(city)
            driver.find_element(By.XPATH, '//*[@id="txtPostCode"]').send_keys(postcode)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="chkPrivacy"]').click()

            time.sleep(1)
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Submitting Information'} {reset_color}")
            driver.find_element(By.XPATH, '//*[@id="ibSubmit"]').click()

            time.sleep(1)

        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Browser Error!'} {reset_color}")

        try:
            driver.find_element(By.XPATH, '//*[@id="ibSubmit"]').click()
        except:
            None

        time.sleep(4)

        try:
            success = driver.find_element(By.XPATH, '//*[@id="normal_thanks"]/div/div/div[1]/div[1]/h2').text
            if str(success) == 'Your order is on the way':
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Successfully Ordered Sim'} {reset_color}")
                order_success = 'Vodaphone'
                log_success(order_success)

        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Vodaphone Sim: Failed to Order Vodaphone Sim'} {reset_color}")

        
def tesco_simgen(addy1, addy2, postcode, city, count, firstname, lastname, api_key):
    phone = '0'
    for i in range(10):
        number = random.randint(1,9)
        phone = phone + str(number)

    email = firstname + lastname
    for i in range(3):
        number = random.randint(1,9)
        email = email + str(number)
    email = email + "@gmail.com"

    code = solver(api_key, count, 'sitekey', 'url', 'TESCO')

    headers = {
        "origin": "https://www.tescomobile.com",
        "referer": "https://www.tescomobile.com/order-sim",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    payload = {
        "success_url": "https://www.tescomobile.com/sim-order-confirmation",
        "title": "Mr",
        "firstname": firstname,
        "surname": lastname,
        "email": email,
        "confirm_email": email,
        "buildRef": addy1,
        "postcode-lookup": postcode,
        "addresses-options": "0",
        "postcode": postcode,
        "addressline1": addy1,
        "addressline2": "",
        "addressline3": addy2,
        "town": city,
        "telephone": phone,
        "g-recaptcha-response": code,
        "token": code,
        "form_key": "xarMt2ITucfLz4dn"
    }

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    res = requests.post("https://www.tescomobile.com/freesim/form/submit/", data=payload, headers=headers)
    if str(res.status_code) == "200":
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'TESCO Sim: Successfully Ordered Tesco Sim Card'} {reset_color}")
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'TESCO Sim: Failed to Order Sim Card'} {reset_color}")

#VODAPHONE
#O2
#THREE
#VOXI
#GIFFGAFF
#TESCO

def start():

    global webhook
    webhook = jsonerrorlogs.jsonwebhook()

    print("Which info input: ")
    print("")
    print("1. CSV Input")
    print("2. CLI Input")
    print("")
    option = int(input("Option: "))

    if option == 1:

        count = 0

        with open(PATH_SIMCARDS_PROFILES) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                store = row[0]
                firstname = row[1]
                lastname = row[2]
                addy1 = row[3]
                addy2 = row[4]
                city = row[5]
                postcode = row[6]

                if store == 'THREE':
                    api_key = jsonerrorlogs.json2captcha()
                    three_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key)
                    count+=1

                elif store == 'GIFFGAFF':
                    giffgaff(addy1, addy2, postcode, city, count, firstname, lastname)
                    count+=1

                elif store == 'O2':
                    api_key = jsonerrorlogs.json2captcha()
                    o2_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key)
                    count+=1

                elif store == 'VODAPHONE':
                    vodaphone(addy1, addy2, postcode, city, count, firstname, lastname)
                    count+=1

    elif option == 2:

        count = 0
        print("Choose the website: ")
        print("")
        print("1. Three")
        print("2. GiffGaff")
        print("3. O2")
        print("4. Vodaphone")
        print("5. Tesco")
        print("")
        store = int(input("Option: "))

        amount = int(input('How many sims: '))
        addy1 = input('Address Line 1: ')
        addy2 = input('Address Line 2: ')
        postcode = input('Postcode:  ')
        city = input('City: ')

        for i in range(amount):

            firstname = names.get_first_name()
            lastname = names.get_last_name()

            if store == 1:
                api_key = jsonerrorlogs.json2captcha()
                three_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key)
                count+=1

            elif store == 2:
                giffgaff(addy1, addy2, postcode, city, count, firstname, lastname)
                count+=1

            elif store == 3:
                api_key = jsonerrorlogs.json2captcha()
                o2_sim(addy1, addy2, city, postcode, count, firstname, lastname, api_key)
                count+=1

            elif store == 4:
                vodaphone(addy1, addy2, postcode, city, count, firstname, lastname)
                count+=1

            elif store == 5:
                api_key = jsonerrorlogs.json2captcha()
                tesco_simgen(addy1, addy2, postcode, city, count, firstname, lastname, api_key)
                count+=1
