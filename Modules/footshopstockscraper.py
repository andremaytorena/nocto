from Paths.paths import PATH_SETTINGS
import json, sys, requests
from colorama import Fore

def log_stock(size_list, stock_list, title, subtitle, total_stock):

    web_json = {
    "content": None,
    "embeds": [
        {
        "title": "Footshop Stock",
        "description": f"{title}\n{subtitle}",
        "color": None,
        "fields": [
            {
            "name": "Sizes",
            "value": f"```{size_list}```",
            "inline": True
            },
            {
            "name": "Stock",
            "value": f"```{stock_list}```",
            "inline": True
            },
            {
            "name": "Total Stock",
            "value": f"```{total_stock}```"
            }
        ],
        "footer": {
            "text": "Powered by Ghost",
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1020022534541955113/ghost_high_res_centred.png"
        }
        }
    ],
    "attachments": []
    }

    requests.post(webhook, json=web_json)


def scrape_stock():

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    global webhook

    if len(settings["Webhook"])==0:
        print(f'{Fore.RED}ERROR; Go on settings.json and fill in the Webhook')
        input(f'{Fore.RESET}Press any key to close this window...')
        sys.exit()
    else:
        webhook = settings['Webhook']
    
    raffle_code = input("raffle sku number: ")

    url = f'https://releases.footshop.com/api/raffles/{raffle_code}'

    res = requests.get(url)
    
    jsonresponse = res.json()['sizeSets']

    fullresponse = res.json()

    title = fullresponse['translations']['en']['title']
    subtitle = fullresponse['translations']['en']['subtitle']

    womensizing = jsonresponse['Women']
    mensizing = jsonresponse['Men']
    kidssizing = jsonresponse['Kids']
    unisexsizing = jsonresponse['Unisex']


    if str(womensizing['sizes']) != "[]":
        gender_size = "Women"
        
    elif str(mensizing['sizes']) != "[]":
        gender_size = 'Men'

    elif str(kidssizing['sizes']) != "[]":
        gender_size = 'Kids'

    elif str(unisexsizing['sizes']) != "[]":
        gender_size = 'Unisex'

    size_stock = jsonresponse[gender_size]['sizes']

    count = 0
    size_list = ""
    stock_list = ""
    total_stock = 0
    for i in range(len(size_stock)):
        size = size_stock[count]['uk']
        stock = size_stock[count]['pieces']

        total_stock = total_stock + int(stock)

        size_list = size_list + '\n' + size
        stock_list = stock_list + '\n' + str(stock)

        count+=1

    log_stock(size_list, stock_list, title, subtitle, total_stock)


