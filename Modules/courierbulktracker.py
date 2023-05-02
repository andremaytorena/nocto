import requests
import time
import json
import sys, os, csv
from os import path
from colorama import Fore
from bs4 import BeautifulSoup
from Paths.paths import PATH_COURIERTRACKER_DPD_FOLDER, PATH_COURIERTRACKER_EVRI_FOLDER
import Modules.jsonerrorlogs as jsonerrorlogs

red_color = '\033[91m' #red
reset_color = '\033[0m' #reset color

def DPD_MAIN():

    def log_shipping(url, COMPANY, PARCELSTATUS, postcode):
        log_webhook = {
        "content": None,
        "embeds": [
            {
            "title": "DPD Shipment Tracking",
            "url": "https://twitter.com/NoctoTools",
            "color": None,
            "fields": [
                {
                "name": "Tracking URL",
                "value": f"[URL]({url})",
                "inline": True
                },
                {
                "name": "Postcode",
                "value": postcode,
                "inline": True
                },
                {
                "name": "Company",
                "value": COMPANY
                },
                {
                "name": "Status",
                "value": PARCELSTATUS
                }
            ],
            "footer": {
                "text": "Powered by NoctoTools",
                "icon_url": "https://media.discordapp.net/attachments/1003847126083711076/1027265274371649596/Noctono4.png?width=454&height=454"
            },
            "thumbnail": {
                "url": "https://media.discordapp.net/attachments/1003847126083711076/1027265274371649596/Noctono4.png?width=454&height=454"
            }
            }
        ],
        "attachments": []
        }

        requests.post(webhook, json=log_webhook)
        
    # def log_overall_shipping(count):
    #     overall_trackings_webhook = {
    #     "content": None,
    #     "embeds": [
    #         {
    #         "title": "Evri Shipment Tracking",
    #         "url": "https://twitter.com/NoctoTools",
    #         "color": None,
    #         "fields": [
    #             {
    #             "name": "Summary:",
    #             "value": f":green_circle: **Delivered** - {delivered_amount}/{count}\n\n:orange_circle: **Out for Delivery** - {outfordelivery_amount}/{count}\n\n:orange_circle: **On its Way** - {onitsway_amount}/{count}\n\n:orange_circle: **We've Got It** - {wegotit_amount}/{count}\n\n:orange_circle: **We're Expecting It** - {other_amount}/{count}\n\n:orange_circle: **Other** - 1/9"
    #             },
    #             {
    #             "name": "Total Packages",
    #             "value": f":package: {count} packages"
    #             }
    #         ],
    #         "footer": {
    #             "text": "Powered by NoctoTools",
    #             "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
    #         },
    #         "timestamp": "2022-12-06T00:00:00.000Z",
    #         "thumbnail": {
    #             "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
    #         }
    #         }
    #     ],
    #     "attachments": []
    #     }

    def createCSV():


        global NEW_PATH

        new = CHOSEN_CSV.split(".")
        new_csv = new[0] + "_result.csv"

        NEW_PATH = path.join(PATH_COURIERTRACKER_DPD_FOLDER, new_csv)

        global fieldnames
        
        with open(NEW_PATH, 'w', newline='') as file:
            fieldnames = ['Tracking URL', 'Postcode', 'Status', 'Company']

            writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
            writer.writeheader()


    def writetracking(url, COMPANY, PARCELSTATUS, postcode):

        with open(NEW_PATH) as f:
                for line in f:
                    pass
                has_newline = line.endswith('\n') or line.endswith('\n\r')

        with open(NEW_PATH, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
            rows = [
                {'Tracking URL':url, 'Postcode':postcode, 'Status':PARCELSTATUS, 'Company':COMPANY}
            ]

            if not has_newline:
                f.write('\n')
        
            writer.writerows(rows)

    def scrapedata(count, tracking, postcode):

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red

        tracking = str(tracking)

        if "https" in tracking:
            tracking = (tracking.split("/")[4])
        else:
            tracking = tracking
        
        for i in range(1):

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'DPD Tracker: Checking Details..'} {reset_color}")

            s = requests.Session()
            url = f'https://track.dpd.co.uk/parcels/{tracking}'

            info = s.get(f'https://apis.track.dpd.co.uk/v1/parcels/{tracking}')

            for i in range(3):
                try:
                    data = info.json()
                    PARCELSTATUS = (data["data"])["trackingStatusCurrent"]
                    COMPANY = (data["data"]["shipperDetails"]["organisation"])

                    print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'DPD Tracker: Successfully Logged Parcel: '}{PARCELSTATUS} {reset_color}")

                    writetracking(url, COMPANY, PARCELSTATUS, postcode)

                    log_shipping(url, COMPANY, PARCELSTATUS, postcode)

                    break
                except:
                    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'DPD Tracker: Wrong Tracking Link/Number'} {reset_color}")
                    time.sleep(2)


    def setup(option):

        global CHOSEN_CSV, webhook

        reset_color = '\033[0m' #reset color

        webhook = jsonerrorlogs.jsonwebhook()

        count = 1
        if option == 1:

            choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_COURIERTRACKER_DPD_FOLDER)))
            amount_csvs = (len(choose_csv))
            line = 0
            for i in range(amount_csvs):
                print(str(line) + ('. ') + choose_csv[line])
                line+=1

            option = int(input('Option: '))
            CHOSEN_CSV = path.join(PATH_COURIERTRACKER_DPD_FOLDER, choose_csv[option])

            createCSV()

            try:
                with open(CHOSEN_CSV) as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        tracking = row[0]
                        postcode = row[1]
                        scrapedata(count, tracking, postcode)

                        count+=1
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Error with your csv, make sure you have filled out all of the columns in the csv located inside the bulk tracker folder'} {reset_color}")
                input('Press enter to exit..')
                sys.exit()
            # log_overall_shipping(count)
        
                
    def main():

        print("1. Track Parcels from CSV")
        option = int(input("Option: "))

        setup(option)

    main()


########################################################################################################################################################################################



def EVRI_MAIN():

    def log_shipping_evri(url, postcode, status, creationDate, store):
        log_webhook = {
        "content": None,
        "embeds": [
            {
            "title": "Evri Shipment Tracking",
            "url": "https://twitter.com/NoctoTools",
            "color": None,
            "fields": [
                {
                "name": "Tracking URL",
                "value": f"[URL]({url})",
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
                "name": "creationDate",
                "value": creationDate
                },
                {
                "name": "Store",
                "value": store
                },
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

        requests.post(webhook, json=log_webhook)
        
    # def log_overall_shipping_evri(count):
    #     overall_trackings_webhook = {
    #     "content": None,
    #     "embeds": [
    #         {
    #         "title": "Evri Shipment Tracking",
    #         "url": "https://twitter.com/NoctoTools",
    #         "color": None,
    #         "fields": [
    #             {
    #             "name": "Summary:",
    #             "value": f":green_circle: **Delivered** - {delivered_amount}/{count}\n\n:orange_circle: **Out for Delivery** - {outfordelivery_amount}/{count}\n\n:orange_circle: **On its Way** - {onitsway_amount}/{count}\n\n:orange_circle: **We've Got It** - {wegotit_amount}/{count}\n\n:orange_circle: **We're Expecting It** - {other_amount}/{count}\n\n:orange_circle: **Other** - 1/9"
    #             },
    #             {
    #             "name": "Total Packages",
    #             "value": f":package: {count} packages"
    #             }
    #         ],
    #         "footer": {
    #             "text": "Powered by NoctoTools",
    #             "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
    #         },
    #         "timestamp": "2022-12-06T00:00:00.000Z",
    #         "thumbnail": {
    #             "url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
    #         }
    #         }
    #     ],
    #     "attachments": []
    #     }

    def createCSV_evri():


        global NEW_PATH

        new = CHOSEN_CSV.split(".")
        new_csv = new[0] + "_result.csv"

        NEW_PATH = path.join(PATH_COURIERTRACKER_EVRI_FOLDER, new_csv)

        global fieldnames
        
        with open(NEW_PATH, 'w', newline='') as file:
            fieldnames = ['Tracking URL', 'Postcode', 'Status', 'Description', 'creationDate', 'store']

            writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
            writer.writeheader()


    def writetracking_evri(url, postcode, status, creationDate, store):

        with open(NEW_PATH) as f:
                for line in f:
                    pass
                has_newline = line.endswith('\n') or line.endswith('\n\r')

        with open(NEW_PATH, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
            rows = [
                {'Tracking URL':url, 'Postcode':postcode, 'Status':status, 'Description':status, 'creationDate': creationDate, "store": store}
            ]

            if not has_newline:
                f.write('\n')
        
            writer.writerows(rows)

    def scrapedata_evri(count, tracking, postcode):

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red

        if "https" in tracking:
            url = tracking
        else:
            url = f"https://www.evri.com/track/parcel/{tracking}/details"
        
        for i in range(1):

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Evri Tracker: Checking Details'} {reset_color}")

            headers = {
                "apiKey": "R6xkX4kqK4U7UxqTNraxmXrnPi8cFPZ6",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            }

            res = requests.get(f"https://api.hermesworld.co.uk/enterprise-tracking-api/v1/parcels/search/{tracking}", headers=headers)
            # uniqueid = str(res.text).split("'")[1].split("'")[0]
            uniqueid= (str(res.text).split('"')[1])

            res = requests.get(f"https://api.hermesworld.co.uk/enterprise-tracking-api/v1/parcels/?uniqueIds={uniqueid}", headers=headers)
            jsonresponse = res.json()

            store = jsonresponse['results'][0]['sender']['displayName']
            creationDate = jsonresponse['results'][0]['creationDate']
            status = jsonresponse['results'][0]['trackingEvents'][0]['trackingStage']['description']


            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Evri Tracker: Successfully Logged Parcel: '}{status}{','} {status} {reset_color}")
            log_shipping_evri(url, postcode, status, creationDate, store)
            writetracking_evri(url, postcode, status, creationDate, store)

            if str(status) == 'Delivered':
                delivered_amount = delivered_amount+1
            else:
                other = other + 1



    def setup_evri(option):

        global CHOSEN_CSV, webhook

        webhook = jsonerrorlogs.jsonwebhook()

        count = 1
        if option == 1:

            choose_csv = list(filter(lambda x: '.csv' in x, os.listdir(PATH_COURIERTRACKER_EVRI_FOLDER)))
            amount_csvs = (len(choose_csv))
            line = 0
            for i in range(amount_csvs):
                print(str(line) + ('. ') + choose_csv[line])
                line+=1

            option = int(input('Option: '))
            CHOSEN_CSV = path.join(PATH_COURIERTRACKER_EVRI_FOLDER, choose_csv[option])

            createCSV_evri

            try: 
                with open(CHOSEN_CSV) as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        tracking = row[0]
                        postcode = row[1]
                        scrapedata_evri(count, tracking, postcode)

                        count+=1
            except:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Error with your csv, make sure you have filled out all of the columns in the csv located inside the bulk tracker folder'} {reset_color}")
                input('Press enter to exit..')
                sys.exit()

            # log_overall_shipping_evri(count)
        
        

    def main_evri():

        print("1. Track Parcels from CSV")
        print("")
        option = int(input("Option: "))

        setup_evri(option)

    main_evri()



def start_main():
    print("1. DPD")
    print("2. EVRI")
    print(" ")
    print("3. Back")
    print("")
    opp = int(input("Option: "))

    if opp == 1:
        DPD_MAIN()
    elif opp == 2:
        EVRI_MAIN()
    elif opp == 3:
        return "BACK"
