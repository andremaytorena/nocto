import requests, re,time
from Modules.jsonerrorlogs import jsonwebhook

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def log_stock(totalstock,image,name,color,web_sizes,web_stock):
    web = {
    "content": None,
    "embeds": [
        {
        "title": "END. Launches Stock",
        "description": name + '\n' + color,
        "color": None,
        "fields": [
            {
            "name": "Sizes",
            "value": f"```{str(web_sizes)}```",
            "inline": True
            },
            {
            "name": "Stock",
            "value": f"```{str(web_stock)}```",
            "inline": True
            },
            {
            "name": "Total Stock",
            "value":f"```{totalstock}```"
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
    
    requests.post(webhook, json=web)

def scrape_stock(releasename):

    for i in range(1):

        url = "https://search1web.endclothing.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=KO4W2GBINK&x-algolia-api-key=dfa5df098f8d677dd2105ece472a44f8"
        
        headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "1283",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://launches.endclothing.com",
        "referer": "https://launches.endclothing.com/",
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        pay = {"requests":[{"indexName":"catalog_products_launches_en","params":f"analyticsTags=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&ruleContexts=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&page=0&facets=%5B%22*%22%5D&facetFilters=%5B%5B%22websites_available_at%3A1%22%5D%2C%5B%22url_key%3A{releasename}%22%5D%5D&clickAnalytics=true&filters="},{"indexName":"catalog_products_launches_en","params":"analyticsTags=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&ruleContexts=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&page=0&facets=%5B%22*%22%5D&facetFilters=%5B%5B%22websites_available_at%3A1%22%5D%5D&clickAnalytics=true"},{"indexName":"catalog_products_launches_en","params":"analyticsTags=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&ruleContexts=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&page=0&facets=websites_available_at&facetFilters=%5B%5B%22url_key%3Anike-dunk-low-sp-cu1726-101-dec%22%5D%5D&analytics=false&filters="},{"indexName":"catalog_products_launches_en","params":"analyticsTags=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&ruleContexts=%5B%22browse%22%2C%22web%22%2C%22v3%22%2C%22gb%22%5D&page=0&facets=url_key&facetFilters=%5B%5B%22websites_available_at%3A1%22%5D%5D&analytics=false&filters="}]}
        
        resp = requests.post(url, headers=headers, json=pay)
        jsonresponse = resp.json()

        try:
            totalstock = jsonresponse['results'][0]['hits'][0]['stock']
            skustock = jsonresponse['results'][0]['hits'][0]['sku_stock']
            image = jsonresponse['results'][0]['hits'][0]['launches_image_landscape']
            name = jsonresponse['results'][0]['hits'][0]['name']
            color = jsonresponse['results'][0]['hits'][0]['actual_colour']
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {'Failed to find SKU!'} {reset_color}")
            break
        
        stock = (list(skustock.values()))

        sizeorder = jsonresponse['results'][0]['hits'][0]['size']
        
        web_sizes = ''
        web_stock = 'demo'

        sizes_stock = dict(zip(sizeorder, stock))

        def get_size(size: str):

            return float(re.findall(r"\d*\.\d+|\d+", size)[0])

        sizes_sorted = sorted(sizeorder, key=get_size)

        sizes_stock_sorted = {}

        for size in sizes_sorted:

            stock = sizes_stock[size]

            sizes_stock_sorted[size] = stock


        # print(sizes_stock_sorted)

        siz_list = (list(sizes_stock_sorted.keys()))
        stock_list = (list(sizes_stock_sorted.values()))

        for i in range(len(sizeorder)):
            # print(i)

            if web_stock == "":
                web_stock = web_stock + str(stock_list[i]) 
                web_sizes = web_sizes + str(siz_list[i])
            else: 
                web_stock = web_stock + '\n' +  str(stock_list[i]) 
                web_sizes = web_sizes + '\n' + str(siz_list[i])

        log_stock(totalstock,image,name,color,web_sizes,web_stock)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {'Successfully Scraped Stock!'} {reset_color}")


def start():

    global webhook
    webhook = jsonwebhook()

    releasename = input("Input release pid: ")
    scrape_stock(releasename)

    print("")
    while True:
        another_pid = input("Would you like to scrape another pid (y/n)? ")
        if another_pid == 'y':
            releasename = input("Input release pid: ")
            scrape_stock(releasename)
        else:
            break
