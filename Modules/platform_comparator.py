import requests, re, csv
from Paths.paths import PATH_PLATFORMCOMPARATOR_CSV

def platform_main():

    user_sku = input("Input SKU: ")
    print("Loading payouts...")
    print("")

    def laced_scrape_sales(user_sku):

        session = requests.Session()
        res = session.get("https://www.laced.com/users/sign_in")
        authtoken = str(res.text).split('csrf-token" content="')[1].split('"')[0]

        payload = {
            "utf8": "✓",
            "authenticity_token": authtoken,
            "user[email]": "testingaccount@gmail.com",
            "user[password]": "TestingAccount123$",
            "user[remember_me]": "0",
            "commit": "Log in"
        }

        res = session.post("https://www.laced.com/users/sign_in", data=payload)

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "f-none-match": 'W/"ecaff30d53be4e44de01ce015271e93d"',
            "referer": f"https://www.laced.com/account/selling/new?style_codes={user_sku}",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        res = session.get(f"https://www.laced.com/account/selling/new/{user_sku}", headers=headers)

        productid = str(res.text).split("products&quot;:[{&quot;id&quot;:")[1].split(",")[0]
        image = str(res.text).split("image_url&quot;:&quot;")[1].split("&quot")[0]
        name = str(str(res.text).split("products&quot;:[{&quot;id&quot;:")[1].split("quot;brand&quot")).split("title&quot;:&quot;")[1].split("&quot")[0]
        active_count = str(res.text).split("active_count&quot;:")[1].split(",")[0]
        sold_count = str(res.text).split("sold_count&quot;:")[1].split(",")[0]


        conversion_sizes = str(res.text).split("productSizes&quot;:[")[1].split('data-react-cache-id="selling/SaleCollectionMultipleItems')[0]

        id_numbers = []
        start = conversion_sizes.find("id")
        while start != -1:
            end = conversion_sizes.find(",", start)
            number = conversion_sizes[start+9:end]
            id_numbers.append(number)
            start = conversion_sizes.find("id", end)


        productSizes = str(res.text).split("productSizes&quot;:[")[1].split('data-react-cache-id="selling/SaleCollectionMultipleItems')[0]

        uk_sizes = [x[0] for x in re.findall(r'UK (\d+(\.\d+)?)', productSizes)]


        count = 0
        sizes_list = ''
        lowestask_list = ''
        sales = ''
        sizes_object = []
        payouts_object =[]
        for i in range(len(uk_sizes)):

            size = uk_sizes[count]
            id = id_numbers[count]

            lowest_ask_response = session.get(f"https://www.laced.com/api/selling/queue_placement?product_id={productid}&price=15&size_conversion_id={id}").json()['lowest_price']

            sizes_list = sizes_list + '\n' + str(size)
            lowestask_list = lowestask_list + '\n' + str(lowest_ask_response)

            payout_num = int(str(lowest_ask_response).split(".")[0])
            
            payout_num *= 1 - 0.12
            payout_num *= 1 - 0.03

            if payout_num == 0:
                payout_num = round(payout_num, 1)
            else:
                payout_num = payout_num - 6.99
                payout_num = round(payout_num, 1) 

            
            sizes_object.append(str(size))
            payouts_object.append(str(payout_num))

            count+=1

        return sizes_object, payouts_object

    def stockx(user_sku
               ):

        session = requests.Session()

        cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "stockx_device_id=90555ad5-9bbd-4bf6-970a-d5b8453dea84; _pxvid=a1cd833f-dc59-11ec-89d4-525869524a6b; _ga=undefined; __ssid=f3a559fb6625ab82eac45d30c6ad602; rskxRunCookie=0; rCookie=r8z9zphkphp4bb6v3uvdl3lxh4f2; QuantumMetricUserID=554985218fb7bf2df587ac77b5785511; __pdst=d91f4d28bf2549d0ac651e53a2955aa8; _scid=3fbe27e4-8a9b-462a-8c12-66b25e43316b; _tt_enable_cookie=1; _ttp=719ecb1b-d450-4ac4-bbd1-3849cb0b6dda; __pxvid=67f7c5c7-dc5b-11ec-b21f-0242ac120002; ajs_anonymous_id=87dc7332-f4a3-4abf-9894-b8bcd48c7baf; OptanonAlertBoxClosed=2022-05-26T21:21:59.010Z; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2022-06-17T10%3A43%3A58.897Z; stockx_dismiss_modal_expiration=2023-06-17T10%3A43%3A58.896Z; stockx_seen_ask_new_info=true; _ga=GA1.2.2017993397.1663414035; _clck=cjrn0k|1|f50|0; __lt__cid=3cfb9c21-7ea5-4968-abde-9dda17cebb41; tracker_device=20feeea7-73cf-4f09-b4bc-f5e80f98f63a; language_code=en; IR_PI=a5001a30-dc59-11ec-ba66-4778787d65c3%7C1674171351162; _uetvid=a4ea77a0dc5911ec9b0a3f947bfbae57; stockx_homepage=sneakers; _pin_unauth=dWlkPVlqRTBPREk1TTJVdE1HWXhNaTAwWTJJekxXSXlNV1l0WXpFME5ETmhPV05tT1dZNA; stockx_session_id=4f9b46a1-d92e-4e3a-9af2-3b1645e5b667; stockx_session=c943f2d0-b7f0-4453-854d-39578783dff6; __cf_bm=Oqa6kx5qZeC8f.Q0WqW_4ldiSC4Hfe7cyNgHyIPAC9U-1682617873-0-AU/0MrXApohXQCSRDpecsOljyAgE41ZyDdopFScrnscMGkUwFZBd8crnkBu7vH1zFGMzfl6dFt/n+CTEe7IQPBM=; stockx_selected_region=GB; stockx_preferred_market_activity=sales; pxcts=1b4f834f-e524-11ed-9401-744c6a654954; ftr_blst_1h=1682617876510; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Apr+27+2023+18%3A51%3A33+GMT%2B0100+(British+Summer+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=4011215d-de64-4db6-a83c-d0f7efea5be4&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0005%3A0%2CC0003%3A0&geolocation=GB%3BENG&AwaitingReconsent=false; forterToken=ccbde83a6aa94e30b65fd149d880d38d_1682617892932__UDF43-m4_13ck; stockx_product_visits=3; lastRskxRun=1682618247495; _pxde=03d231939669e914eb215f27fc5c3938adcc66d41d7eb3e0b1b85eaefeba08cb:eyJ0aW1lc3RhbXAiOjE2ODI2MTgzNzQwNDksImZfa2IiOjB9; _dd_s=rum=0&expire=1682619272172",
            "if-none-match": 'W/"67j22ozfp7isq"',
            "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"

        }

        res = session.get(f"https://stockx.com/api/browse?&_search={user_sku}&dataType=product", headers=headers)

        name = res.json()['Products'][0]['shortDescription']
        image = res.json()['Products'][0]['media']['imageUrl']
        retailPrice = res.json()['Products'][0]['retailPrice']
        urlkey = res.json()['Products'][0]['urlKey']

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "cookie": "stockx_device_id=90555ad5-9bbd-4bf6-970a-d5b8453dea84; _pxvid=a1cd833f-dc59-11ec-89d4-525869524a6b; _ga=undefined; __ssid=f3a559fb6625ab82eac45d30c6ad602; rskxRunCookie=0; rCookie=r8z9zphkphp4bb6v3uvdl3lxh4f2; QuantumMetricUserID=554985218fb7bf2df587ac77b5785511; __pdst=d91f4d28bf2549d0ac651e53a2955aa8; _scid=3fbe27e4-8a9b-462a-8c12-66b25e43316b; _tt_enable_cookie=1; _ttp=719ecb1b-d450-4ac4-bbd1-3849cb0b6dda; __pxvid=67f7c5c7-dc5b-11ec-b21f-0242ac120002; ajs_anonymous_id=87dc7332-f4a3-4abf-9894-b8bcd48c7baf; OptanonAlertBoxClosed=2022-05-26T21:21:59.010Z; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2022-06-17T10%3A43%3A58.897Z; stockx_dismiss_modal_expiration=2023-06-17T10%3A43%3A58.896Z; stockx_seen_ask_new_info=true; _ga=GA1.2.2017993397.1663414035; _clck=cjrn0k|1|f50|0; __lt__cid=3cfb9c21-7ea5-4968-abde-9dda17cebb41; tracker_device=20feeea7-73cf-4f09-b4bc-f5e80f98f63a; language_code=en; IR_PI=a5001a30-dc59-11ec-ba66-4778787d65c3%7C1674171351162; _uetvid=a4ea77a0dc5911ec9b0a3f947bfbae57; stockx_homepage=sneakers; _pin_unauth=dWlkPVlqRTBPREk1TTJVdE1HWXhNaTAwWTJJekxXSXlNV1l0WXpFME5ETmhPV05tT1dZNA; stockx_session_id=4f9b46a1-d92e-4e3a-9af2-3b1645e5b667; stockx_session=c943f2d0-b7f0-4453-854d-39578783dff6; __cf_bm=Oqa6kx5qZeC8f.Q0WqW_4ldiSC4Hfe7cyNgHyIPAC9U-1682617873-0-AU/0MrXApohXQCSRDpecsOljyAgE41ZyDdopFScrnscMGkUwFZBd8crnkBu7vH1zFGMzfl6dFt/n+CTEe7IQPBM=; stockx_selected_region=GB; stockx_preferred_market_activity=sales; pxcts=1b4f834f-e524-11ed-9401-744c6a654954; ftr_blst_1h=1682617876510; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Apr+27+2023+18%3A51%3A33+GMT%2B0100+(British+Summer+Time)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=4011215d-de64-4db6-a83c-d0f7efea5be4&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0005%3A0%2CC0003%3A0&geolocation=GB%3BENG&AwaitingReconsent=false; forterToken=ccbde83a6aa94e30b65fd149d880d38d_1682617892932__UDF43-m4_13ck; stockx_product_visits=3; lastRskxRun=1682618247495; _pxde=03d231939669e914eb215f27fc5c3938adcc66d41d7eb3e0b1b85eaefeba08cb:eyJ0aW1lc3RhbXAiOjE2ODI2MTgzNzQwNDksImZfa2IiOjB9; _dd_s=rum=0&expire=1682619272172",
            "apollographql-client-name": "Iron",
            "apollographql-client-version": "2023.01.01.05",
            "app-platform": "Iron",
            "app-version": "2023.01.01.05",
            "content-length": "3289",
            "content-type": "application/json",
            "origin": "https://stockx.com",
            "referer": "https://stockx.com/" + urlkey,
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "selected-country": "GB",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "x-operation-name": "GetMarketData",
            "x-stockx-device-id": res.json()['Products'][0]['id']
        }

        payload = {
            "operationName": "GetMarketData",

            "query": "query GetMarketData($id: String!, $currencyCode: CurrencyCode, $countryCode: String!, $marketName: String) {\n  product(id: $id) {\n    id\n    urlKey\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        highestBidSize\n        lowestAsk\n        lowestAskSize\n      }\n    }\n    variants {\n      id\n      market(currencyCode: $currencyCode) {\n        bidAskData(country: $countryCode, market: $marketName) {\n          highestBid\n          highestBidSize\n          lowestAsk\n          lowestAskSize\n        }\n      }\n    }\n    ...BidButtonFragment\n    ...BidButtonContentFragment\n    ...BuySellFragment\n    ...BuySellContentFragment\n  }\n}\n\nfragment BidButtonFragment on Product {\n  id\n  title\n  urlKey\n  sizeDescriptor\n  productCategory\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      highestBidSize\n      lowestAsk\n      lowestAskSize\n    }\n  }\n  media {\n    imageUrl\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        highestBidSize\n        lowestAsk\n        lowestAskSize\n      }\n    }\n  }\n}\n\nfragment BidButtonContentFragment on Product {\n  id\n  urlKey\n  sizeDescriptor\n  productCategory\n  lockBuying\n  lockSelling\n  minimumBid(currencyCode: $currencyCode)\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      highestBidSize\n      lowestAsk\n      lowestAskSize\n      numberOfAsks\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        highestBidSize\n        lowestAsk\n        lowestAskSize\n        numberOfAsks\n      }\n    }\n  }\n}\n\nfragment BuySellFragment on Product {\n  id\n  title\n  urlKey\n  sizeDescriptor\n  productCategory\n  lockBuying\n  lockSelling\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      highestBidSize\n      lowestAsk\n      lowestAskSize\n    }\n  }\n  media {\n    imageUrl\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        highestBidSize\n        lowestAsk\n        lowestAskSize\n      }\n    }\n  }\n}\n\nfragment BuySellContentFragment on Product {\n  id\n  urlKey\n  sizeDescriptor\n  productCategory\n  lockBuying\n  lockSelling\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      highestBidSize\n      lowestAsk\n      lowestAskSize\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        highestBidSize\n        lowestAsk\n        lowestAskSize\n      }\n    }\n  }\n}\n",


            "variables": {
                "countryCode": "GB",
                "currencyCode": "GBP",
                "id": urlkey,
                "marketName": ""
            }
        }

        res = session.post("https://stockx.com/api/p/e", json=payload, headers=headers)
        count = 0
        sizes = ""
        lowest_ask = ""
        numberOfAsks = ""
        payout = ""
        sizes_object = []
        payouts_object =[]
        for i in range(len(res.json()['data']['product']['variants'])):

            sizes = sizes + '\n' + str(res.json()['data']['product']['variants'][count]['market']['bidAskData']['lowestAskSize'])
            lowest_ask = lowest_ask + '\n' + '£' + str(res.json()['data']['product']['variants'][count]['market']['bidAskData']['lowestAsk'])

            try:
                payout_num = (res.json()['data']['product']['variants'][count]['market']['bidAskData']['lowestAsk'])
                payout_num *= 1 - 0.09
                payout_num *= 1 - 0.03
                payout_num = round(payout_num, 1) - 4
            except:
                payout_num = 'None'

            payout = payout + '\n' + '£' + str(payout_num)

            sizes_object.append(str(res.json()['data']['product']['variants'][count]['market']['bidAskData']['lowestAskSize']))
            payouts_object.append(str(payout_num))

            count+=1

        return sizes_object, payouts_object

    stockx_sizes, stockx_prices = stockx(user_sku)

    laced_sizes, laced_prices = laced_scrape_sales(user_sku)

    # Create a list of dictionaries with the data for each row
    data = []
    for i in range(len(laced_sizes)):
        # Skip None values
        if laced_sizes[i] == 'None':
            continue
        
        # Check if the size exists in the stockx_sizes list
        if laced_sizes[i] in stockx_sizes:
            # Add a row for this size
            row = {
                'Sizes': "UK " + laced_sizes[i],
                'Stockx': stockx_prices[stockx_sizes.index(laced_sizes[i])],
                'Laced': laced_prices[i]
            }
            data.append(row)

    # Define the filename for the CSV file
    filename = PATH_PLATFORMCOMPARATOR_CSV

    # Open the file for writing
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=['Sizes', 'Stockx', 'Laced'])
        
        # Write the header row
        writer.writeheader()
        
        # Write the data rows
        for row in data:
            writer.writerow(row)

    import pandas as pd
    from tabulate import tabulate

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)

    # Print the DataFrame as a table using tabulate
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
    print("")
    restart = input("Would you like to check another pair? (y/n)")
    if restart.lower() == "y":
        print("")
        platform_main()
    else:
        None



