import requests, time, os, json, threading, random, sys, csv
from os import path
from selenium import webdriver
from Paths.paths import PATH_CHROME_DRIVER, PATH_SETTINGS, PATH_FLATSPOT_LOGS, PATH_PROXIES, PATH_FLATSPOT_FOLDER
import RaffleModules.webhook_management as webhooks
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

success_entry_count = 0
failed_entry_count = 0

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def write_success_logs(email):

    fieldnames = ['Email', 'Raffle']

    with open(PATH_FLATSPOT_LOGS) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_FLATSPOT_LOGS, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Email':email, 'Raffle':raffle_name}
        ]
        if not has_newline:
            f.write('\n')

        writer.writerows(rows)

def send_discord_log(email, size):

    webhooks.flatspot_entry_webhook(raffle_name, email, size, webhook)

    webhooks.astro_logs("Entered Raffle!", "Flatspot Launches")

def waiting_solved(stripe_url, email, main_count):

    ser = Service(PATH_CHROME_DRIVER)
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=ser, options=options, service_log_path='/dev/null')

    driver.get(stripe_url)

    while True:
        if 'flatspot.com' in driver.current_url:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Solved 3DS Challenge'} {reset_color}")
            break

    for i in range(20):
        try:
            s = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[1]/div/form/div[1]/div[2]/div[2]/div/p').text
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Enter Raffle: '}{s} {reset_color}")
            driver.quit()
            checked_out = 'Failed Entry'
            return checked_out 
        except:
            None

        time.sleep(2)


def checkout(size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, main_count, proxies):
    
    for i in range(3):

        session = requests.Session()

        for i in range(1):

            res = requests.get(raffle_name)
            s = (res.text.split("json_product = ")[1].split("};")[0] + "}")

            re = json.loads(s)
            sizes_list = (re['variants'])

            if "UK" not in size:
                size = "UK " + str(size)

            sizes_count=0
            for i in range(len(sizes_list)):
                varient_id = sizes_list[sizes_count]['id']
                title = sizes_list[sizes_count]['option1']
                if title == size:
                    break
                else:
                    sizes_count+=1
                    None

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Adding to cart'} {reset_color}")

            url = 'https://releases.flatspot.com/cart/add.js'

            headers = {
                "origin": "https://releases.flatspot.com",
                "referer": raffle_name,
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            payload = {
                "id": varient_id,
                "quantity": "1"
            }

            carting_response = session.post(url, json=payload, headers=headers, proxies=proxies).json()
            try:
                if carting_response['status'] == 'bad_request':
                    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Add to Card: '}{carting_response['message']} {reset_color}")
            except:
                None

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Checking out..'} {reset_color}")
            goingtocheckout_response = session.get('https://releases.flatspot.com/checkout', headers=headers, proxies=proxies)

            try:
                new_url = goingtocheckout_response.text.split('path":"\/checkout\/contact_information","search":"","url":"')[1].split('"')[0].replace('\\', "")
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Checkout'} {reset_color}")
                break

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Adding Shipping Information'} {reset_color}")
            get_shipping_response = session.get(new_url + '?step=contact_information', headers=headers, proxies=proxies)
            try:
                authtoken = str(get_shipping_response.text).split('name="authenticity_token" value="')[1].split('"')[0]
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Generate Auth Token'} {reset_color}")

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://releases.flatspot.com",
                "referer": "https://releases.flatspot.com",
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
                "checkout[email]": email,
                "checkout[buyer_accepts_marketing]": "1",
                "checkout[shipping_address][first_name]": firstname,
                "checkout[shipping_address][last_name]": lastname,
                "checkout[shipping_address][company]": "",
                "checkout[shipping_address][address1]": addressline1,
                "checkout[shipping_address][address2]": addressline2,
                "checkout[shipping_address][city]": city,
                "checkout[shipping_address][country]": "GB",
                "checkout[shipping_address][province]": "",
                "checkout[shipping_address][zip]": postcode,
                "checkout[shipping_address][phone]": phonenumber,
                "checkout[shipping_address][country]": "United Kingdom",
                "checkout[shipping_address][first_name]": firstname,
                "checkout[shipping_address][last_name]": lastname,
                "checkout[shipping_address][company]": "",
                "checkout[shipping_address][address1]": addressline1,
                "checkout[shipping_address][address2]": addressline2,
                "checkout[shipping_address][city]": city,
                "checkout[shipping_address][zip]": postcode,
                "checkout[shipping_address][phone]": phonenumber,
                "checkout[client_details][browser_width]": "634",
                "checkout[client_details][browser_height]": "764",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "30",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            send_shipping_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)

            if 'Shipping - Releases.Flatspot - Checkout' in send_shipping_response.text:
                None
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Add Shipping Information'} {reset_color}")

            authtoken = str(send_shipping_response.text).split('name="authenticity_token" value="')[1].split('"')[0]
            courier_id = str(send_shipping_response.text).split('data-shipping-method="')[1].split('"')[0]
            # str(res.text).split('data-backup="')[1].split('"')[0]

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "dnt": "1",
                "origin": "https://releases.flatspot.com/",
                "referer": "https://releases.flatspot.com/",
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
                "checkout[shipping_rate][id]": courier_id,
                "checkout[client_details][browser_width]": "634",
                "checkout[client_details][browser_height]": "764",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "30",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            get_shipping_method_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Shipping Information'} {reset_color}")
            if 'Payment - Releases.Flatspot - Checkout' in get_shipping_method_response.text:
                None
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed to Submit Shipping Information'} {reset_color}")

            total_price = (str(get_shipping_method_response.text).split("Shopify.Checkout.totalPrice = ")[1].split(";")[0]).replace(".","")
            payment_gateway = str(get_shipping_method_response.text).split('data-gateway-name="credit_card"')[1].split("data-submit")[0]
            payment_gateway_id = payment_gateway.split('data-select-gateway="')[1].split('"')[0]
            authtoken = str(get_shipping_method_response.text).split('name="authenticity_token" value="')[1].split('"')[0]

            if ' ' not in cardnumber:
                updated_card_number = ""
                for i, char in enumerate(cardnumber):
                    updated_card_number += char
                    if (i + 1) % 4 == 0:
                        updated_card_number += " "

                cardnumber = updated_card_number
            else:
                None

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
                    "month": cardmonth,
                    "name": firstname + ' ' + lastname,
                    "number": cardnumber,
                    "start_month": "null",
                    "start_year": "null",
                    "verification_value": cardcvv,
                    "year": cardyear
                },
                "payment_session_scope": "releases.flatspot.com"
            }

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Sending Card Data'} {reset_color}")
            send_payment_response = session.post('https://deposit.us.shopifycs.com/sessions', json=payload, headers=headers, proxies=proxies).json()
            try:
                west_id = send_payment_response['id']
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed Sending Card Data'} {reset_color}")

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "content-length": "1557",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://releases.flatspot.com/",
                "referer": "https://releases.flatspot.com/",
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
                "step": "",
                "s": west_id,
                "checkout[payment_gateway]": payment_gateway_id,
                "checkout[credit_card][vault]": "false",
                "checkout[different_billing_address]": "false",
                "checkout[remember_me]": "false",
                "checkout[remember_me]": "0",
                "checkout[vault_phone]": phonenumber,
                "checkout[total_price]": total_price,
                "complete": "1",
                "checkout[client_details][browser_width]": "795",
                "checkout[client_details][browser_height]": "796",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "30",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Card Details'} {reset_color}")
            next_paymentstep_response = session.post(new_url, data=payload, headers=headers, proxies=proxies)
            
            if 'Processing order - Releases.Flatspot - Checkout' in next_paymentstep_response.text:
                None
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed Submitting Card Details'} {reset_color}")
                break

            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "dnt": "1",
                "referer": "https://releases.flatspot.com/",
                "sec-ch-ua":'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Getting 3DS Browser..'} {reset_color}")

            processing_response = session.get(new_url + '/processing', headers=headers, proxies=proxies)
            
            time.sleep(2)

            time.sleep(1)

            for i in range(3):
                get_stripe_url_response = session.get(new_url + '/processing?from_processing_page=1', headers=headers, proxies=proxies)

                stripe_url = str(get_stripe_url_response.text).split('<a href="')[1].split('"')[0]
                
                if stripe_url == '#main-header':
                    None

                else:
                    checked_out = '3DS'
                    return stripe_url, checked_out


            get_stripe_url_response = session.get(new_url + '/thank_you', headers=headers, proxies=proxies)
            if str(get_stripe_url_response.status_code) == '200':
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Entered Raffle'} {reset_color}")
                write_success_logs(email)
                checked_out = 'Entered'
                stripe_url = 'null'
                return stripe_url, checked_out
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Failed Entering Raffle'} {reset_color}")
                checked_out = 'Failed Entry'
                stripe_url = 'null'
                return stripe_url, checked_out
    

def start(size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, main_count):

    global success_entry_count, failed_entry_count

    ENTERED_RAFFLE = False

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
                    None

            stripe_url, checked_out = checkout(size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, main_count, proxies)
            if checked_out == '3DS':
                checked_out = waiting_solved(stripe_url, email, main_count) 
            elif checked_out == 'Entered':
                ENTERED_RAFFLE = True
            elif checked_out == 'Failed Entry':
                ENTERED_RAFFLE = False

        if checked_out == 'Entered':
            ENTERED_RAFFLE = True
            break
        elif checked_out == 'Failed Entry':
            ENTERED_RAFFLE = False

    if ENTERED_RAFFLE == True:
        success_entry_count+=1
        os.system(f'title Flatspot Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
        send_discord_log(email, size)

    elif ENTERED_RAFFLE == False:
        failed_entry_count+=1
        os.system(f'title Flatspot Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')




def set_csvs():

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_FLATSPOT_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_FLATSPOT_FOLDER, choose_csv[option])
    print("")
    return PROFILES_CSV


def CheckEntryStatus(): # Opens accounts csv and gets account

    global amount_of_proxy_lines, webhook, retrylimit, raffle_name
    main_count = 0

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    webhook = settings['Webhook']
    delay = int(settings['EntryDelay'])
    threads = int(settings['Threads'])
    retrylimit = int(settings['RetryLimit'])
    
    #gets current open raffles
    os.system(f'title Flatspot Launches Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')

    raffle_name = input("Raffle URL: ")

    PROFILES_CSV = set_csvs()

    account_num = 1
    entered_num = 1

    proxy_line = 0
    account_number = 1

    finished_entering = False
    
    results_accounts = pd.read_csv(PROFILES_CSV)
    _linesaccounts = int((len(results_accounts)))

    results_entered = pd.read_csv(PATH_FLATSPOT_LOGS)
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

                    with open(PATH_FLATSPOT_LOGS) as entered:
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
                        if finished_entering  == False:
                            thread = threading.Thread(target=start, args=[size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, cardnumber, cardmonth, cardyear, cardcvv, main_count])
                            thread.start()
                        else:
                            None
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
        elif finished_entering  == True:
            None
        else:
            thread.join()
            time.sleep(delay)
