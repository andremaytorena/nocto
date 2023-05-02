import requests
import time, csv, sys, json
from colorama import Fore
from Paths.paths import PATH_NIKEORDERTRACKER_PROFILES, PATH_PROXIES
import Modules.jsonerrorlogs as jsonerrorlogs
import Modules.proxieserrorlogs as proxieserrorlogs

def log_win(releasename, retail, sku, email, tracking, status, name, address, postcode, image):
    log_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Nike Shipment Tracking",
        "url": "https://twitter.com/NoctoTools",
        "color": None,
        "fields": [
            {
            "name": "Release Name",
            "value": releasename
            },
            {
            "name": "Retail",
            "value": str(retail),
            "inline": True
            },
            {
            "name": "SKU",
            "value": sku,
            "inline": True
            },
            {
            "name": "Email",
            "value": email
            },
            {
            "name": "Tracking URL",
            "value": f"[URL]({tracking})",
            "inline": True
            },
            {
            "name": "Status",
            "value": status,
            "inline": True
            },
            {
            "name": "Name",
            "value": name
            },
            {
            "name": "Address",
            "value": address,
            "inline": True
            },
            {
            "name": "Postcode",
            "value": postcode,
            "inline": True
            }
        ],
        "footer": {
            "text": "Powered by NoctoTools",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        },
        "thumbnail": {
            "url": image
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=log_webhook)



def get_order(email, order, proxies):

    red_color = '\033[91m' #red
    reset_color = '\033[0m' #reset color
    green_color = '\033[92m' #light green

    url = f"https://api.nike.com/orders/summary/v1/{order}?locale=en_gb&country=GB&language=en-GB&email={email}&timezone=Europe%2FLondon"

    payload = {
        "locale": "en_gb",
        "country": "GB",
        "language": "en-GB",
        "email": email,
        "timezone": "Europe/London"
        }

    headers = {
        "nike-api-caller-id": "com.nike:sse.orders",
        "origin": "https://www.nike.com",
        "referer": "https://www.nike.com/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Nike Order Tracker: Finding Order...'} {reset_color}")
    for i in range(5):
        try: 
            res = requests.get(f"https://api.nike.com/orders/summary/v1/{order}?locale=en_gb&country=GB&language=en-GB&email={email}&timezone=Europe%2FLondon", json=payload, headers=headers)
            jsonresponse = res.json()
            releasename = jsonresponse['group'][0]['orderItems'][0]['product']['title'] + ' ' + jsonresponse['group'][0]['orderItems'][0]['product']['color']
            retail = jsonresponse['group'][0]['orderItems'][0]['lineItemTransaction']['lineItemChargedPrice']
            sku = jsonresponse['group'][0]['orderItems'][0]['product']['styleColor']
            email = jsonresponse['shippingAddress'][4]
            status = jsonresponse['group'][0]['heading']
            name = jsonresponse['shippingAddress'][0]
            address = jsonresponse['shippingAddress'][1]
            postcode = jsonresponse['shipFrom']['address']['zipCode']
            image = jsonresponse['group'][0]['orderItems'][0]['product']['productImage']

            try:
                tracking = jsonresponse['group'][0]['actions']['trackShipment']['webLink']
            except:
                tracking = "None Loaded"

            log_win(releasename, retail, sku, email, tracking, status, name, address, postcode, image)
            break
        except:
            time.sleep(1)


def start():

    global count

    proxy_count = 0
    count = 1

    global webhook

    webhook = jsonerrorlogs.jsonwebhook()
    proxieserrorlogs.checkproxies()

    with open(PATH_NIKEORDERTRACKER_PROFILES) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            email = row[0]
            order = row[1]


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
        
            get_order(email, order, proxies)

            proxy_count+=1
            count+=1

