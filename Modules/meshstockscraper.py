import requests, time
from Modules.jsonerrorlogs import jsonwebhook

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def record_stock(stocklist,sizelist,title,image, totalstock, sitename):

    discohook = {
    "content": None,
    "embeds": [
        {
        "title": sitename,
        "description": title,
        "color": None,
        "fields": [
            {
            "name": "Sizes",
            "value": f"```{sizelist}```",
            "inline": True
            },
            {
            "name": "Stock",
            "value": f"```{stocklist}```",
            "inline": True
            },
            {
            "name": "Total Stock",
            "value": f"```{totalstock}```"
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
    requests.post(webhook, json=discohook)


def sizelaunches(raffleid):

    for i in range(1):

        url = f'https://mosaic-platform.jdmesh.co/admin/stores/size/products/{raffleid}?MESHKey=B26DC670995711E3A5E20800200C9A66'

        res = requests.get(url).json()

        try:
            image = res['product']['mainImage']['original']
            title = res['product']['name']
            sitename = 'Size? Launches Stock'
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {'Failed to find SKU!'} {reset_color}")
            break

        count = 0
        stocklist = ''
        sizelist = ''
        totalstock = 0
        for i in range(len(res['product']['options'])):
            stock = (res['product']['options'][count]['availableCount'])
            size = (res['product']['options'][count]['name'])

            stocklist = stocklist + '\n' + str(stock)
            sizelist = sizelist + '\n' + str(size)
            totalstock = totalstock + int(stock)

            count+=1

        record_stock(stocklist,sizelist,title,image, totalstock, sitename)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Successfully Scraped Stock!'} {reset_color}")


def footpatrollaunches(raffleid):

    for i in range(1):

        url = f'https://mosaic-platform.jdmesh.co/admin/stores/footpatrolgb/products/{raffleid}?MESHKey=B26DC670995711E3A5E20800200C9A66'

        res = requests.get(url).json()

        try:
            image = res['product']['mainImage']['original']
            title = res['product']['name']
            sitename = 'Footpatrol Launches Stock'
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {'Failed to find SKU!'} {reset_color}")
            break
        
        count = 0
        stocklist = ''
        sizelist = ''
        totalstock = 0
        for i in range(len(res['product']['options'])):
            stock = (res['product']['options'][count]['availableCount'])
            size = (res['product']['options'][count]['name'])

            stocklist = stocklist + '\n' + str(stock)
            sizelist = sizelist + '\n' + str(size)
            totalstock = totalstock + int(stock)

            count+=1

        record_stock(stocklist,sizelist,title,image, totalstock, sitename)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Successfully Scraped Stock!'} {reset_color}")

def hipstorelaunches(raffleid):

    for i in range(1):

        url = f'https://mosaic-platform.jdmesh.co/admin/stores/thehipstore/products/{raffleid}?MESHKey=B26DC670995711E3A5E20800200C9A66'

        res = requests.get(url).json()

        try:
            image = res['product']['mainImage']['original']
            title = res['product']['name']
            sitename = 'Hipstore Launches Stock'
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {'Failed to find SKU!'} {reset_color}")
            break

        count = 0
        stocklist = ''
        sizelist = ''
        totalstock = 0
        for i in range(len(res['product']['options'])):
            stock = (res['product']['options'][count]['availableCount'])
            size = (res['product']['options'][count]['name'])

            stocklist = stocklist + '\n' + str(stock)
            sizelist = sizelist + '\n' + str(size)
            totalstock = totalstock + int(stock)

            count+=1

        record_stock(stocklist,sizelist,title,image, totalstock, sitename)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Successfully Scraped Stock!'} {reset_color}")

def start():

    global webhook
    webhook = jsonwebhook()

    print("1. Size? Launches")
    print("2. Footpatrol Launches")
    print("3. Hipstore Launches")
    print("")
    option = int(input("Option: "))

    raffleid = input("Input raffle pid: ")

    if option==1:
        sizelaunches(raffleid)
    elif option==2:
        footpatrollaunches(raffleid)
    elif option==3:
        hipstorelaunches(raffleid)

    print("")
    while True:
        another_pid = input("Would you like to scrape another pid (y/n)? ")
        if another_pid == 'y':
            raffleid = input("Input raffle pid: ")
            if option==1:
                sizelaunches(raffleid)
            elif option==2:
                footpatrollaunches(raffleid)
            elif option==3:
                hipstorelaunches(raffleid)
        else:
            break

