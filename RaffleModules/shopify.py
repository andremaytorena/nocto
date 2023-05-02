import requests, time, os, json, threading, random, sys, csv
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from Paths.paths import MAIN_PATH, PATH_SHOPIFY_FOLDER
import threading

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red
OKBLUE = '\033[94m'


def waiting_solved(stripe_url, EMAIL, main_count):

    ser = Service()
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=ser, options=options, service_log_path='/dev/null')

    driver.get(stripe_url)

    while True:
        if 'trapstarlondon.com' in driver.current_url:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Solved 3DS Challenge'} {reset_color}")
            break

    for i in range(20):
        try:
            s = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div/p').text
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Enter Raffle: '}{s} {reset_color}")
            driver.quit()
            checked_out = 'Failed Entry'
            return checked_out 
        except:
            None

        time.sleep(2)


def checkout(BASE_URL, VARIENT_ID, QUANTITY, EMAIL, FIRSTNAME, LASTNAME, ADDRESS1, ADDRESS2, CITY, POSTCODE, PHONE, CCNUMBER, CCMONTH, CCYEAR, CVV, main_count, amount_of_proxy_lines, PATH_PROXIES):

    for i in range(10000):

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

        session = requests.Session()

        for i in range(1):
            
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Solving Password'} {reset_color}")

            headers = {
                "referer": "https://drinkprime.uk/password",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }

            payload = {
                "form_type": "storefront_password",
                "password": site_password,
                "commit": ""
            }
            res = session.post("https://drinkprime.uk/password", json=payload, headers=headers)

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Adding to cart'} {reset_color}")

            url = f'{BASE_URL}/cart/add.js'

            headers = {
                "origin": BASE_URL,
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }

            payload = {
                "id": VARIENT_ID,
                "quantity": QUANTITY
            }

            carting_response = session.post(url, json=payload, headers=headers, proxies=proxies)
            try:
                carting_response = carting_response.json()
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Add to Card'}{reset_color}")
                break
            try:
                if carting_response['status'] == 'bad_request' or carting_response['status'] == 404:
                    try:
                        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Add to Card: '}{carting_response['message']} {reset_color}")
                    except: 
                        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Add to Card: '}{carting_response['message']}: {carting_response['description']} {reset_color}")
                    break
            except:
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Added to Card'} {reset_color}")

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Checking out..'} {reset_color}")
            goingtocheckout_response = session.get(f'{BASE_URL}/checkout', headers=headers, proxies=proxies)
            try:
                new_url = goingtocheckout_response.text.split('path":"\/checkout\/contact_information","search":"","url":"')[1].split('"')[0].replace('\\', "")
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Checking Out'} {reset_color}")
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Checkout'} {reset_color}")
                break


            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Adding Shipping Information'} {reset_color}")
            get_shipping_response = session.get(new_url + '?step=contact_information', headers=headers, proxies=proxies)
            try:
                authtoken = str(get_shipping_response.text).split('name="authenticity_token" value="')[1].split('"')[0]
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Generate Auth Token'} {reset_color}")
                break



            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "origin": BASE_URL,
                "referer": BASE_URL + '/',
                "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "contact_information",
                "step": "shipping_method",
                "checkout[email_or_phone]": EMAIL,
                "checkout[buyer_accepts_marketing]": "0",
                "checkout[buyer_accepts_marketing]": "1",
                "checkout[shipping_address][first_name]": FIRSTNAME,
                "checkout[shipping_address][last_name]": LASTNAME,
                "checkout[shipping_address][company]": "",
                "checkout[shipping_address][address1]": ADDRESS1,
                "checkout[shipping_address][address2]": ADDRESS2,
                "checkout[shipping_address][city]": CITY,
                "checkout[shipping_address][country]": "GB",
                "checkout[shipping_address][province]": "",
                "checkout[shipping_address][zip]": POSTCODE,
                "checkout[shipping_address][phone]": PHONE,
                "checkout[shipping_address][country]": "United Kingdom",
                "checkout[shipping_address][first_name]": FIRSTNAME,
                "checkout[shipping_address][last_name]": LASTNAME,
                "checkout[shipping_address][company]": "",
                "checkout[shipping_address][address1]": ADDRESS1,
                "checkout[shipping_address][address2]": ADDRESS2,
                "checkout[shipping_address][city]": CITY,
                "checkout[shipping_address][zip]": POSTCODE,
                "checkout[shipping_address][phone]": PHONE,
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            send_shipping_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)

            with open('readme.txt', 'w') as f:
                f.write(str(send_shipping_response.text))


            if '<title>    Shipping' in send_shipping_response.text:
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Added Shipping Information'} {reset_color}")
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Add Shipping Information'} {reset_color}")
                break

            dpd_id = str(send_shipping_response.text).split('data-shipping-method="')[1].split('"')[0]

            try:
                authtoken = str(get_shipping_response.text).split('name="authenticity_token" value="')[1].split('"')[0]
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Generate Auth Token'} {reset_color}")
                break

            authtoken = str(send_shipping_response.text).split('name="authenticity_token" value="')[1].split('"')[0]
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "dnt": "1",
                "origin": BASE_URL + "/",
                "referer": BASE_URL + "/",
                "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "shipping_method",
                "step": "payment_method",
                "checkout[shipping_rate][id]": dpd_id,
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            get_shipping_method_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Submitting Shipping Information'} {reset_color}")
            if '<title>    Payment' in get_shipping_method_response.text:
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Submitted Shipping Information'} {reset_color}")
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed to Submit Shipping Information'} {reset_color}")
                break

            total_price = (str(get_shipping_method_response.text).split("Shopify.Checkout.totalPrice = ")[1].split(";")[0]).replace(".","")

            authtoken = str(get_shipping_method_response.text).split('name="authenticity_token" value="')[1].split('"')[0]

            payment_gateway = str(get_shipping_method_response.text).split('data-gateway-name="credit_card"')[1].split("data-submit")[0]
            payment_gateway_id = payment_gateway.split('data-select-gateway="')[1].split('"')[0]

            if ' ' not in CCNUMBER:
                updated_card_number = ""
                for i, char in enumerate(CCNUMBER):
                    updated_card_number += char
                    if (i + 1) % 4 == 0:
                        updated_card_number += " "

                CCNUMBER = updated_card_number
            else:
                None

            SCOPE = str(BASE_URL).split("https://")[1]

            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                "Content-Length": "221",
                "Content-Type": "application/json",
                "dnt": "1",
                "Host": "deposit.us.shopifycs.com",
                "Origin": "https://checkout.shopifycs.com",
                "Referer": "https://checkout.shopifycs.com/",
                "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            payload = {
                "credit_card": {
                    "issue_number": "",
                    "month": CCMONTH,
                    "name": FIRSTNAME + ' ' + LASTNAME,
                    "number": CCNUMBER,
                    "start_month": "null",
                    "start_year": "null",
                    "verification_value": CVV,
                    "year": CCYEAR
                },
                "payment_session_scope": SCOPE
            }

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Sending Card Data'} {reset_color}")
            send_payment_response = session.post('https://deposit.us.shopifycs.com/sessions', json=payload, headers=headers, proxies=proxies).json()
            try:
                west_id = send_payment_response['id']
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Sent Card Data'} {reset_color}")
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Sending Card Data'} {reset_color}")
                break

            

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "origin": BASE_URL + "/",
                "referer": BASE_URL + "/",
                "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "payment_method",
                "step": "review",
                "s": west_id,
                "checkout[payment_gateway]": payment_gateway_id,
                "checkout[credit_card][vault]": "false",
                "checkout[different_billing_address]": "false",
                "checkout[remember_me]": "false",
                "checkout[remember_me]": "0",
                "checkout[vault_phone]": PHONE,
                "checkout[total_price]": total_price,
                "complete": "1",
                "checkout[client_details][browser_width]": "795",
                "checkout[client_details][browser_height]": "796",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "30",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Submitting Card Details'} {reset_color}")
            next_paymentstep_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)
            
            if '<title>    Processing order' in next_paymentstep_response.text:
                print(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Submitted Card Details'} {reset_color}")
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Submitting Card Details'} {reset_color}")
                # break
                

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "dnt": "1",
                "referer": BASE_URL + "/",
                "sec-ch-ua":'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Getting 3DS Browser..'} {reset_color}")

            processing_response = session.get(new_url + '/processing', headers=headers, proxies=proxies)
            
            time.sleep(2)

            time.sleep(1)

            for i in range(3):
                get_stripe_url_response = session.get(new_url + '/processing?from_processing_page=1', headers=headers, proxies=proxies)

                stripe_url = str(get_stripe_url_response.text).split('<a href="')[1].split('"')[0]
                
                if stripe_url == '#main-header':
                    None

                else:
                    waiting_solved(stripe_url, EMAIL, main_count)
                    return ''


            get_stripe_url_response = session.get(new_url + '/thank_you', headers=headers, proxies=proxies)
            if str(get_stripe_url_response.status_code) == '200':
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Checked Out Item'} {reset_color}")
                urll = new_url + '/processing?from_processing_page=1'
                waiting_solved(urll, EMAIL, main_count)
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Checking Out Item'} {reset_color}")
                break



def set_csvs():

    print("")

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_SHOPIFY_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_SHOPIFY_FOLDER, choose_csv[option])
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

    global site_password
    success_entry_count = 0
    failed_entry_count = 0
    #gets current open raffles
    os.system(f'title Shopify Module - Checked Out: {success_entry_count} - Failed: {failed_entry_count}')

    PROFILES_CSV = set_csvs()

    PATH_PROXIES = set_proxies_file()

    amount_threads = int(input("Amount of threads: "))
    print("")
    site_password = input("Site password: ")

    account_num = 1

    main_count = 1

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())

    while True:

        for i in range(amount_threads):
            try:
                with open(PROFILES_CSV) as accounts:
                    mycsv = accounts.readlines()
                    y = mycsv[account_num].rstrip('\n')
                    row = y.split(",")
                    BASE_URL = row[0]
                    VARIENT_ID = row[1]
                    QUANTITY = row[2]
                    EMAIL = row[3]
                    FIRSTNAME = row[4]
                    LASTNAME = row[5]
                    ADDRESS1 = row[6]
                    ADDRESS2 = row[7]
                    CITY = row[8]
                    POSTCODE = row[9]
                    PHONE = row[10]
                    CCNUMBER = row[11]
                    CCMONTH = row[12]
                    CCYEAR = row[13]
                    CVV = row[14]
            except IndexError:
                break   
            
            thread = threading.Thread(target=checkout, args=[BASE_URL, VARIENT_ID, QUANTITY, EMAIL, FIRSTNAME, LASTNAME, ADDRESS1, ADDRESS2, CITY, POSTCODE, PHONE, CCNUMBER, CCMONTH, CCYEAR, CVV, main_count, amount_of_proxy_lines, PATH_PROXIES])
            thread.start()
            account_num+=1
            main_count+=1

        thread.join()

