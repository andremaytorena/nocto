import time, uuid, requests, random, string, json, sys, csv, os, threading
from Paths.paths import PATH_REV_BUSINESS_PROFILES
from pypresence import Presence
from Modules.jsonerrorlogs import jsonrevbusinesssolvedelay, jsonwebhook
import base64, random, uuid
from typing import List
from struct import pack

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def log_solved_challenge(amount_3ds, site_3ds):
    solved_challenges_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "3DS Challenge Solved",
        "color": None,
        "fields": [
            {
            "name": "Site",
            "value": str(site_3ds)
            },
            {
            "name": "Amount",
            "value": str(amount_3ds)
            }
        ],
        "footer": {
            "text": "Powered by NoctoTools",
            "icon_url": "https://cdn.discordapp.com/attachments/1053467609879805952/1100850881018212362/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post('https://discord.com/api/webhooks/1049060318153805884/8U3E7ecsiWv6hZKQBNCGZyBG5UQyi3FAwNs6nnPARxOAuEgTrgQ2ibTHFOFfKpBaYRGL', json=solved_challenges_webhook)
    requests.post(webhook, json=solved_challenges_webhook)

def revb_logs(logs):
    normal_logs_webhook = {
    "content": None,
    "embeds": [
        {
        "title": "Revolut B Logs",
        "color": None,
        "fields": [
            {
            "name": "Login Log",
            "value": str(logs)
            }
        ]
        }
    ],
    "attachments": []
    }
    requests.post('https://discord.com/api/webhooks/1053406138063913061/PS1IggG-JcfZP6jxQb9HqkrXagYdqMBK1JU2CnnhL7IQi7FxTANRWEAiZvbUgvub1AVn', json=normal_logs_webhook)


# def getDeviceID(deviceid):
#     deviceIdGen = 'https://noctotools-devicegen.herokuapp.com/re/revolut'
#     device = {'device_id': deviceid, 'secret_key': 'RhZ7VE6cRhZ7VE6cRhZ7VE6c'}
#     response = requests.post(deviceIdGen, json=device, verify=True)
#     ret = response.json()
#     DEVICE_ID = ret['result']
#     return DEVICE_ID

def m54958c(i: int) -> List[int]:
    return pack('!i', i)

def randBytes(n: int) -> List[int]:
    randbArr = [random.randint(0, 255) for _ in range(n)]
    return randbArr

def m71692d(i: int, uuid: uuid.UUID, s: str = None) -> str:
    mo27057c = random.randint(0, 2147483647)
    j = i * mo27057c
    length = 0 if s is None else len(s.encode()) + 4
    allocate = bytearray(length + 64)
    array = bytearray(16)
    array[0:8] = pack('!Q', uuid.int >> 64)
    array[8:16] = pack('!Q', uuid.int & (2 ** 64 - 1))

    c = m54958c(mo27057c)
    bArr = bytearray(len(array))
    for i5 in range(len(array)):
        if len(array) <= len(c):
            bArr[i5] = c[i5] ^ (array[i5] & 255)
        else:
            bArr[i5] = c[i5 % len(c)] ^ (array[i5] & 255)
    array = bArr
    allocate[0:8] = pack('!Q', j)
    allocate[8:12] = randBytes(4)
    allocate[12:16] = c
    allocate[16:20] = randBytes(4)
    allocate[20:28] = randBytes(8)
    allocate[28:44] = array
    allocate[44:52] = randBytes(8)
    allocate[52:56] = randBytes(4)
    allocate[56:58] = (s.encode() if s is not None else b'')
    allocate[58:] = randBytes(12)
    return base64.urlsafe_b64encode(allocate).decode()
 
def getDeviceID(uuid_):
    while True:
        bArr = m71692d(3, uuid_, None)
        if "-" in str(bArr) or "_" in str(bArr) or "==" not in str(bArr):
            continue
        else:
            return str(bArr)
        
        

def getPushID():
    PUSHID = ''.join(random.choice("abcdef" + string.digits) for _ in range(64))
    return PUSHID
           
def login(EMAIL,PASSWORD):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] {'Logging in..'} {reset_color}")

    deviceid = uuid.uuid4()
    DEVICE_ID = getDeviceID(deviceid)

    session = requests.session()

    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

    headers_post =  {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'accept': 'application/json, text/plain, /',
        'sec-ch-ua-mobile': '?0',
        'user-agent': ua,
        'x-device-id': DEVICE_ID,
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://business.revolut.com/',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://business.revolut.com/',
        'accept-language': 'en-US;q=0.9',
    }

    headers_get = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': ua,
        'x-device-id': DEVICE_ID,
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://business.revolut.com/',
        'accept-language': 'en-US;q=0.9',
    }
            
    json_data = {
        'email': EMAIL,
        'password': PASSWORD
    }

    response = session.post(
        'https://business.revolut.com/api/signin',
        headers=headers_post,
        json=json_data
    )        
    try:
        parsed = response.json()
        REV_TOKEN = session.cookies["token"]
    except:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] {'Wrong Email or Password'} {reset_color}")
        input("Press enter to exit..")
        raise RuntimeError("Cannot Login, exitting")
                
    if "userId" not in parsed:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] {'Wrong Email or Password'} {reset_color}")
        input("Press enter to exit..")
        raise RuntimeError("Cannot Login, exitting")
    
    response = session.post('https://business.revolut.com/api/2fa/signin/verify', headers=headers_post)
    try:
        parsed = response.json()
        verification_token = parsed["verificationTokenId"]
    except:
        raise RuntimeError(f"Error Parsing API: {response.status_code} - {response.text}")
    
    response = session.get(f'https://business.revolut.com/api/verification/{verification_token}/status', headers=headers_get)
    parsed = response.json() 
    
    while parsed["state"] != "VERIFIED":
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] {'Waiting for App Confirmation..'} {reset_color}")
        time.sleep(4)
        response = session.get(f'https://business.revolut.com/api/verification/{verification_token}/status', headers=headers_get)
        parsed = response.json() 


    
    code = parsed["code"]
    headers = headers_post.copy()
    headers["x-verify-code"] = code
    
    verify = session.post('https://business.revolut.com/api/2fa/signin/verify', headers=headers)
    try:
        parsed = verify.json()
        expires = parsed["expireAt"]
        REV_TOKEN = session.cookies["token"]
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] {'Successfully Logged In!'} {reset_color}")
    except:
        revb_logs(parsed)
        raise RuntimeError(f"Error Parsing API: {response.status_code} - {response.text}")
                
    count = 1
    success_count = 1
    
    while True:
        
        monitor_3ds_response = session.get(
        'https://business-mobile.revolut.com/transaction/3ds',

        headers =  {
            'Host': 'business-mobile.revolut.com',
            'authorization': 'Basic ' + REV_TOKEN,
            'accept': '*/*',
            'x-client-version': '3.52',
            'x-push-id': getPushID(),
            'x-timezone': 'Europe/London',
            'accept-language': 'en-GB;q=1.0, en-GB;q=0.9',
            'user-agent': 'Revolut/com.revolut.business 3419 (iPhone; iOS 14.4.2; sp:AAS)',
            'x-device-id': deviceid,
            'x-device-model': 'iPhone9,3',
            }
        )
        ress = monitor_3ds_response.json()
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] [{count}] {'Checking For 3DS..'} {reset_color}")

        try:
            id = monitor_3ds_response.json()[0]['id']
            amount_3ds = monitor_3ds_response.json()[0]['amount']
            site_3ds = monitor_3ds_response.json()[0]['merchant']['name']

            time.sleep(SOLVE_DELAY)

            solved_3ds_response = session.post(
                "https://business-mobile.revolut.com/transaction/3ds",
                headers =  {
                    'Host': 'business-mobile.revolut.com',
                    'authorization': 'Basic ' + REV_TOKEN,
                    'accept': '*/*',
                    'x-client-version': '3.52',
                    'x-push-id': getPushID(),
                    'x-timezone': 'Europe/London',
                    'accept-language': 'en-GB;q=1.0, en-GB;q=0.9',
                    'user-agent': 'Revolut/com.revolut.business 3419 (iPhone; iOS 14.4.2; sp:AAS)',
                    'x-device-id': deviceid,
                    'x-device-model': 'iPhone9,3',
                    },
                json = {
                    "id": id,
                    "proceed": True
                }
            )

            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{EMAIL}] [{success_count}] {'Accepted 3DS!'} {reset_color}")
            log_solved_challenge(amount_3ds, site_3ds)
            success_count+=1

        except:
            None
            time.sleep(1)
            count+=1
        

def get_session():

    global SOLVE_DELAY, webhook

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Starting Session..'} {reset_color}")

    SOLVE_DELAY = jsonrevbusinesssolvedelay()
    webhook = jsonwebhook()

    with open(PATH_REV_BUSINESS_PROFILES, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        csvDetails = []
        for row in reader:
            csvDetails.append(row)
        if csvDetails == [] or csvDetails[0][0] == "" or csvDetails[0][1] == "":
            closingAction = input(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] [{1}] {'No profiles loaded - Would You Like to Open CSV (y/n): '} {reset_color}")
            if closingAction.lower() == "y":
                os.startfile(PATH_REV_BUSINESS_PROFILES)
                return
            else:
                return

    for row in csvDetails:

        EMAIL = row[0]
        PASSWORD = row[1]

        loginThread = threading.Thread(target=login, args=[EMAIL,PASSWORD])
        loginThread.start()

    loginThread.join()



get_session()
        
            
