import requests, os, sys, time, csv, random, threading
import pandas as pd 
from Paths.paths import PATH_AFEW_LOGS, PATH_AFEW_FOLDER, MAIN_PATH, PATH_PROXIES
import RaffleModules.webhook_management as webhooks
from os import path
from RaffleModules.jsonerrorlogs import jsonwebhook, jsonthreads, jsonretrylimit, jsonentrydelay, proxiesfile

success_entry_count = 0
failed_entry_count = 0

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def write_success_logs(email):

    fieldnames = ['Email', 'Raffle']

    with open(PATH_AFEW_LOGS) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_AFEW_LOGS, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Email':email, 'Raffle':raffle_name}
        ]
        if not has_newline:
            f.write('\n')

        writer.writerows(rows)

def send_webhook(EMAIL, size):

    webhooks.afew_entry_webhook(raffle_name, EMAIL, size, webhook)

    webhooks.astro_logs("Entered Raffle!", "Afew Launches")

def checkout(size, EMAIL, PASSWORD, FIRSTNAME, LASTNAME, ADDRESS1, ADDRESS2, CITY, POSTCODE, PHONE, instagram, sizes_list, main_count):

    status = "NOT ENTERED"

    sizes_count=0
    for i in range(len(sizes_list)):
        varient_id = sizes_list[sizes_count]['id']
        title = sizes_list[sizes_count]['title']
        if title == size:
            break
        else:
            sizes_count+=1
            None    

    for i in range(int(retrylimit)):

        if status == "ENTERED":
            break

        for i in range(1):

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
                    
                    break
                except:
                    None

            session = requests.Session()

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Adding to cart..'} {reset_color}")
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "referer": "https://en.afew-store.com/",
                "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-site",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }

            res = session.get(f"https://raffles.afew-store.com/cart/{varient_id}:1?locale=en&attributes%5Blocale%5D=en&attributes%5Binstagram%5D={instagram}&utm_source=", headers=headers)
            try:
                checkout_url = "https://" + str(res.text).split('pageurl":"')[1].split('"')[0].replace('\\', "")
                authtoken = str(res.text).split('name="authenticity_token" value="')[1].split('"')[0]
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Added to Cart!'} {reset_color}")
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Adding to Cart'} {reset_color}")
                break

            res = session.get(checkout_url, headers=headers)

            new_url = checkout_url.split("?")[0]

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Submitting Shipping Info'} {reset_color}")
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "contact_information",
                "step": "shipping_method",
                "checkout[email]": EMAIL,
                "checkout[attributes][locale]": "en",
                "checkout[attributes][instagram]": "J A Maytorena Cuevas",
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
                "checkout[remember_me]": "",
                "checkout[remember_me]": "0",
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            res = session.post(new_url, data=payload, headers=headers)

            try:
                authtoken = str(res.text).split('name="authenticity_token" value="')[1].split('"')[0]
                courier_id = str(res.text).split('data-shipping-method="')[1].split('"')[0]
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Added Shipping Info!'} {reset_color}")
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Adding Shipping Info'} {reset_color}")
                break

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Adding Courier Info'} {reset_color}")
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "shipping_method",
                "step": "payment_method",
                "checkout[shipping_rate][id]": courier_id,
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            res = session.post(new_url, data=payload, headers=headers)

            try:
                authtoken = str(res.text).split('name="authenticity_token" value="')[1].split('"')[0]
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Added Courier Info!'} {reset_color}")
            except:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Adding Courier Info'} {reset_color}")
                break
            
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Submitting Order'} {reset_color}")
            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "previous_step": "payment_method",
                "step": "review",
                "s":"",
                "checkout[payment_gateway]": "39963820118",
                "checkout[different_billing_address]": "false",
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            res = session.post(new_url, data=payload, headers=headers)

            try:
                total_price = (str(res.text).split("Shopify.Checkout.totalPrice = ")[1].split(";")[0]).replace(".","")
                authtoken = str(res.text).split('name="authenticity_token" value="')[1].split('"')[0]
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Submitting Order 1'} {reset_color}")
                break

            payload = {
                "_method": "patch",
                "authenticity_token": authtoken,
                "checkout[total_price]": total_price,
                "complete": "1",
                "checkout[client_details][browser_width]": "1121",
                "checkout[client_details][browser_height]": "969",
                "checkout[client_details][javascript_enabled]": "1",
                "checkout[client_details][color_depth]": "24",
                "checkout[client_details][java_enabled]": "false",
                "checkout[client_details][browser_tz]": "300"
            }

            res = session.post(new_url, data=payload, headers=headers)

            if str(res.status_code) == '200':
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Successfully Submitted Order!'} {reset_color}")
                write_success_logs(EMAIL)
                send_webhook(EMAIL, size)
                status = "ENTERED"
                break
            else:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}][{EMAIL}][{main_count}] {'Failed Submitting Order 2'} {reset_color}")
                break

def set_csvs():

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_AFEW_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    PROFILES_CSV = path.join(PATH_AFEW_FOLDER, choose_csv[option])
    print("")
    return PROFILES_CSV

def set_proxies_file():

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


def get_products():

    global raffle_name, sizes_list

    res = requests.get("https://en.afew-store.com/collections/sneaker-releases/products.json").json()

    products_list = []
    count=0
    for i in range(len(res['products'])):
        name = res['products'][count]['title']
        print(str(count)+ '.', name)

        products_list.append(res['products'][count])
        
        count+=1

    print("")

    option = int(input("Option: "))

    raffle_name = res['products'][option]['title']
    handle = res['products'][option]['handle']

    res = requests.get(f"https://raffles.afew-store.com/products/{handle}.json").json()
    sizes_list = res['product']['variants']

    print("")

    return sizes_list 


def CheckEntryStatus(): # Opens accounts csv and gets account

    global amount_of_proxy_lines, webhook, retrylimit
    main_count = 0

    webhook = jsonwebhook()
    delay = int(jsonentrydelay())
    threads = int(jsonthreads())
    retrylimit = int(jsonretrylimit())
    
    #gets current open raffles
    os.system(f'title Afew Entry Module - Success: {success_entry_count} - Failed: {failed_entry_count}')
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{0}] {'Getting Open Releases..'} {reset_color}")
    
    sizes_list = get_products()

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

    results_entered = pd.read_csv(PATH_AFEW_LOGS)
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
                            instagram = row[10]
                    except IndexError:
                        finished_entering = True
                        break

                    with open(PATH_AFEW_LOGS) as entered:
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
                    if finished_entering == False:
                        try:
                            thread = threading.Thread(target=checkout, args=[size, email, password, firstname, lastname, addressline1, addressline2, city, postcode, phonenumber, instagram, sizes_list, main_count])
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

        if error == 1 or finished_entering == 1:
            None
        else:
            thread.join()
            time.sleep(delay)

