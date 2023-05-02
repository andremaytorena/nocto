import requests
from bs4 import BeautifulSoup
import time, os, csv
from os import path 
import sys
from colorama import Fore
import json
from Paths.paths import PATH_SETTINGS, PATH_MESHTRACKER_FOLDER
import Modules.jsonerrorlogs as jsonerrorlogs


green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def log_win(tracking_url, store, orderid, postcode, status):
    webhook_json = {
    "content": None,
    "embeds": [
        {
        "title": "Mesh Shipment Tracking",
        "url": "https://twitter.com/NoctoTools",
        "color": None,
        "fields": [
            {
            "name": "Tracking URL",
            "value": f"[URL]({tracking_url})",
            "inline": True
            },
            {
            "name": "Postcode",
            "value": postcode,
            "inline": True
            },
            {
            "name": "Status",
            "value": status
            },
            {
            "name": "Store",
            "value": store,
            "inline": True
            },
            {
            "name": "OrderID",
            "value": orderid,
            "inline": True
            }
        ],
        "footer": {
            "text": "Powered by NoctoTools",
            "icon_url": "https://media.discordapp.net/attachments/1003847126083711076/1027265274371649596/Noctono4.png?width=567&height=567"
        },
        "thumbnail": {
            "url": "https://media.discordapp.net/attachments/1003847126083711076/1027265274371649596/Noctono4.png?width=567&height=567"
        }
        }
    ],
    "attachments": []
    }

    requests.post(webhook, json=webhook_json)

def createCSV(CHOSEN_CSV):

    
    global NEW_PATH

    new = str(CHOSEN_CSV).split(".")
    new_csv = new[0] + "_result.csv"

    NEW_PATH = path.join(PATH_MESHTRACKER_FOLDER, new_csv)

    global fieldnames
    
    with open(NEW_PATH, 'w', newline='') as file:
        fieldnames = ['Store', 'Tracking URL', 'OrderID', 'Postcode', 'Status']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()


def writetracking(store, orderid, postcode, status):

    with open(NEW_PATH) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(NEW_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Store':store, 'Tracking URL':'URL', 'OrderID':orderid, 'Postcode':postcode, 'Status':status}
        ]

        if not has_newline:
            f.write('\n')
    
        writer.writerows(rows)



def meshtrack(store, orderid, postcode, count):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Hipstore Tracker: Checking Order..'} {reset_color}")

    s = requests.Session()

    if store == 'hipstore.uk':
        site_region = 'https://www.thehipstore.co.uk'
    elif store == 'jd.fr':
        site_region = 'https://www.jdsports.fr'
    
    postcode_main = str(postcode).replace(" ", "")
    
    tracking_url = f'{site_region}/track-my-order/?orderID={orderid}&email=&postcode={postcode_main}'

    for i in range(3):
        try:
            res = s.get(tracking_url)
            page = (res.text)

            soup = BeautifulSoup(page, 'html.parser')

            status = soup.find(class_="longDescription").text

            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {site_region}{': Successfully Tracked Order: '}{status} {reset_color}")
            
            writetracking(store, orderid, postcode, status)

            log_win(tracking_url, store, orderid, postcode, status)

            break
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Hipstore Tracker: Failed to Track Order'} {reset_color}")
            time.sleep(2)



def start():

    global webhook

    webhook = jsonerrorlogs.jsonwebhook()

    choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_MESHTRACKER_FOLDER)))
    amount_csvs = (len(choose_csv))
    line = 0
    for i in range(amount_csvs):
        print(str(line) + ('. ') + choose_csv[line])
        line+=1

    option = int(input('Option: '))
    CHOSEN_CSV = path.join(PATH_MESHTRACKER_FOLDER, choose_csv[option])

    createCSV(CHOSEN_CSV)

    count = 1
    try: 
        with open(CHOSEN_CSV) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                store = row[0]
                orderid = row[1]
                postcode = row[2]

                meshtrack(store, orderid, postcode, count)
                count+=1
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Error with your csv, make sure you have filled out all of the columns in the csv located inside the bulk tracker folder'} {reset_color}")
        input('Press enter to exit..')
        sys.exit()