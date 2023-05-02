import time, uuid, requests, random, string, json, sys
from Paths.paths import PATH_SETTINGS
from pypresence import Presence

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
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post('https://discord.com/api/webhooks/1049060318153805884/8U3E7ecsiWv6hZKQBNCGZyBG5UQyi3FAwNs6nnPARxOAuEgTrgQ2ibTHFOFfKpBaYRGL', json=solved_challenges_webhook)

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

def discord_rpc():
    client_id = "1052038607227068476"
    start = int(time.time())
    try:
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(
            large_image = "ghost",
            large_text = "Ghost",
            details = "Solving 3DS",
            # state = "NOCTO",
            buttons = [{'label': 'Discord', 'url': 'https://discord.gg/FKd4SUJTqU'}],
            start = start
        )
    except:
        pass

def getDeviceID(deviceid):
    deviceIdGen = 'https://noctotools-devicegen.herokuapp.com/re/revolut'
    device = {'device_id': deviceid, 'secret_key': 'RhZ7VE6cRhZ7VE6cRhZ7VE6c'}
    response = requests.post(deviceIdGen, json=device, verify=True)
    ret = response.json()
    DEVICE_ID = ret['result']
    return DEVICE_ID

def getPushID():
    PUSHID = ''.join(random.choice("abcdef" + string.digits) for _ in range(64))
    return PUSHID

class RevGen:

    def __init__(self) -> None:
        
        self.session = requests.session()

        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"

        if EMAIL == "" or PASSWORD == "":
            print("No email and password found in settings file.")
            print("Read the guide before asking.")
            input("Press enter to exit..")
            sys.exit()
        
        if EMAIL != "" and PASSWORD != "":
            self.login()  
            
           
    def login(self):

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Logging in..'} {reset_color}")

        deviceid = str(uuid.uuid4())
        DEVICE_ID = getDeviceID(deviceid)

        self.headers_post =  {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'accept': 'application/json, text/plain, /',
            'sec-ch-ua-mobile': '?0',
            'user-agent': self.ua,
            'x-device-id': DEVICE_ID,
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://business.revolut.com/',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://business.revolut.com/',
            'accept-language': 'en-US;q=0.9',
        }

        self.headers_get = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': self.ua,
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

        response = self.session.post(
            'https://business.revolut.com/api/signin',
            headers=self.headers_post,
            json=json_data
        )        
        try:
            parsed = response.json()
            REV_TOKEN = self.session.cookies["token"]
        except:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Wrong Email or Password'} {reset_color}")
            input("Press enter to exit..")
            raise RuntimeError("Cannot Login, exitting")
                    
        if "userId" not in parsed:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Wrong Email or Password'} {reset_color}")
            input("Press enter to exit..")
            raise RuntimeError("Cannot Login, exitting")
        
        response = self.session.post('https://business.revolut.com/api/2fa/signin/verify', headers=self.headers_post)
        try:
            parsed = response.json()
            verification_token = parsed["verificationTokenId"]
        except:
            raise RuntimeError(f"Error Parsing API: {response.status_code} - {response.text}")
        
        response = self.session.get(f'https://business.revolut.com/api/verification/{verification_token}/status', headers=self.headers_get)
        parsed = response.json() 
        
        while parsed["state"] != "VERIFIED":
                # self.log_info(f"Waiting for App confirmation")
            time.sleep(4)
            response = self.session.get(f'https://business.revolut.com/api/verification/{verification_token}/status', headers=self.headers_get)
            parsed = response.json() 


        
        code = parsed["code"]
        headers = self.headers_post.copy()
        headers["x-verify-code"] = code
        
        verify = self.session.post('https://business.revolut.com/api/2fa/signin/verify', headers=headers)
        try:
            parsed = verify.json()
            self.expires = parsed["expireAt"]
            REV_TOKEN = self.session.cookies["token"]
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Successfully Logged In!'} {reset_color}")
        except:
            revb_logs(parsed)
            raise RuntimeError(f"Error Parsing API: {response.status_code} - {response.text}")
                    
        count = 1
        success_count = 1
        
        while True:
            
            monitor_3ds_response = self.session.get(
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
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Checking For 3DS..'} {reset_color}")

            try:
                id = monitor_3ds_response.json()[0]['id']
                amount_3ds = monitor_3ds_response.json()[0]['amount']
                site_3ds = monitor_3ds_response.json()[0]['merchant']['name']

                time.sleep(SOLVE_DELAY)

                solved_3ds_response = self.session.post(
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
    
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{success_count}] {'Accepted 3DS!'} {reset_color}")
                log_solved_challenge(amount_3ds, site_3ds)
                success_count+=1

            except:
                None
                time.sleep(1)
                count+=1

    
def start():

    if __name__ == "__main__":
        pass
    
    global EMAIL, PASSWORD, SOLVE_DELAY
    try:
        EMAIL = settings['revolutbusiness']['email']
        PASSWORD = settings['revolutbusiness']['password']
        SOLVE_DELAY = int(settings['revolutbusiness']['solve_delay'])
    except:
        print('Fill in your credentials in the settings file')
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Loaded Credentials!'} {reset_color}")

    RevGen()
        

def get_session():

    discord_rpc()

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'Starting Session..'} {reset_color}")

    global settings
    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    start()
 
    
        
            
