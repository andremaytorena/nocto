import sys, time, base64, requests, json, uuid, random, string, pickle, os, threading
from Paths.paths import PATH_SETTINGS, PATH_REV_PERSONAL_PROFILES, PATH_REV_PERSONAL_FOLDER
import Modules.jsonerrorlogs as jsonerrorlogs
from os import path
import pandas as pd
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
            "icon_url": "https://cdn.discordapp.com/attachments/1003847126083711076/1027265274371649596/Noctono4.png"
        }
        }
    ],
    "attachments": []
    }
    requests.post('https://discord.com/api/webhooks/1049060318153805884/8U3E7ecsiWv6hZKQBNCGZyBG5UQyi3FAwNs6nnPARxOAuEgTrgQ2ibTHFOFfKpBaYRGL', json=solved_challenges_webhook)
    requests.post(webhook, json=solved_challenges_webhook)


# def getDeviceID():
#     deviceIdGen = 'https://noctotools-devicegen.herokuapp.com/re/revolut'
#     deviceid = str(uuid.uuid4())
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
 
def getDeviceID():
    while True:
        uuid_ = uuid.uuid4()
        bArr = m71692d(3, uuid_, None)
        if "-" in str(bArr) or "_" in str(bArr) or "==" not in str(bArr):
            continue
        else:
            return str(bArr)

def getPushID():
    PUSHID = ''.join(random.choice("abcdef" + string.digits) for _ in range(64))
    return PUSHID

def getRevolutVersion_UserAgent():

    global revolutVersion, revolutUserAgent
    
    for i in range(3):
        try:
            revolutVersion = requests.get("https://noctotools.herokuapp.com/revolut_personal_version").text 
            revolutUserAgent = requests.get("https://noctotools.herokuapp.com/revolut_personal_useragent").text 
            return revolutVersion, revolutUserAgent
        except:
            None

def clean_tokens(account_num, phone_number):

    df = pd.read_csv(PATH_REV_PERSONAL_PROFILES)
    df.at[account_num-1, 'Token'] = ""
    df.to_csv(PATH_REV_PERSONAL_PROFILES, index=False)

    df.at[account_num-1, 'DeviceID'] = ""
    df.to_csv(PATH_REV_PERSONAL_PROFILES, index=False)

    os.remove(path.join(PATH_REV_PERSONAL_FOLDER, f"personalsession_{str(account_num)}.pkl"))

    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Please close the bot immediately and run the re load the accounts: '} {reset_color}")

    time.sleep(10)

    sys.exit()



def solve_challenges(authtoken, DEVICE_ID, session, phone_number, account_num):

    count = 1
    success_count = 1
    
    while True:
    
        monitor_3ds_response = session.get(
            "https://api.revolut.com/transaction/3ds",
            headers =  {
                'Host': 'api.revolut.com',
                'Authorization':"Basic " + authtoken,
                'accept': '*/*',
                'x-client-version': revolutVersion,
                'x-push-id': getPushID(),
                'x-timezone': 'Europe/London',
                'accept-language': 'en-GB;q=1.0',
                'user-agent': revolutUserAgent,
                'x-device-id': DEVICE_ID,
            }
        )
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{count}] {'Checking For 3DS..'} {reset_color}")
        try:
            if monitor_3ds_response.json()['message'] == 'The request should be authorized.':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{count}] {'Auth Token Expired, clearing tokens..'} {reset_color}")
                clean_tokens(account_num, phone_number)
        except:
            None
        
        try:
            if monitor_3ds_response.json()['message'] == 'Access token expired':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{count}] {'Auth Token Expired, clearing tokens..'} {reset_color}")
                clean_tokens(account_num, phone_number)
        except:
            None

        try:
            id = monitor_3ds_response.json()[0]['id']
            holder = monitor_3ds_response.json()[0]['cardholder_id']
            site_3ds = monitor_3ds_response.json()[0]['merchant']['name']
            amount_3ds = monitor_3ds_response.json()[0]['amount']

            time.sleep(SOLVE_DELAY)
        
            solved_3ds_response = session.post(
                "https://api.revolut.com/transaction/3ds",
                headers =  {
                    'Host': 'api.revolut.com',
                    'Authorization':"Basic " + authtoken,
                    'accept': '*/*',
                    'x-client-version': revolutVersion,
                    'x-push-id': getPushID(),
                    'x-timezone': 'Europe/London',
                    'accept-language': 'en-GB;q=1.0',
                    'user-agent': revolutUserAgent,
                    'x-device-id': DEVICE_ID,
                },
                json = {
                    "cardholder_id": holder,
                    "proceed": "true",
                    "id": id
                }
            )
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{success_count}] {'Accepted 3DS!'} {reset_color}")
            success_count+=1
            log_solved_challenge(amount_3ds, site_3ds)

        except:
            time.sleep(1)
            count+=1


def login(DEVICE_ID, phone_number, passcode, session, account_num):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Sending SMS Code..'} {reset_color}")
    
    login_response = session.post(
        "https://api.revolut.com/signin",
        headers =  {
            'Host': 'api.revolut.com',
            'accept': '*/*',
            'x-client-version': revolutVersion,
            'x-push-id': getPushID(),
            'x-timezone': 'Europe/London',
            'accept-language': 'en-GB;q=1.0',
            'user-agent': revolutUserAgent,
            'x-device-id': DEVICE_ID,
            'x-integrity-check': "Y29tLnJldm9sdXQuY29yZS5tb2JpbGVfc2VydmljZXMuYXBpLmV4Y2VwdGlvbnMuTXNBcGlFeGNlcHRpb246IC04OiBJbnRlZ3JpdHkgQVBJIGVycm9yICgtOCk6IFRoZSBjYWxsaW5nIGFwcCBpcyBtYWtpbmcgdG9vIG1hbnkgcmVxdWVzdHMgdG8gdGhlIEFQSSBhbmQgaGVuY2UgaXMgdGhyb3R0bGVkLgpSZXRyeSB3aXRoIGFuIGV4cG9uZW50aWFsIGJhY2tvZmYuCiAoaHR0cHM6Ly9kZXZlbG9wZXIuYW5kcm9pZC5jb20vcmVmZXJlbmNlL2NvbS9nb29nbGUvYW5kcm9pZC9wbGF5L2NvcmUvaW50ZWdyaXR5L21vZGVsL0ludGVncml0eUVycm9yQ29kZS5odG1sI1RPT19NQU5ZX1JFUVVFU1RTKS4="
        },
        json = {
            "phone": phone_number,
            "password": passcode
        }
    )
    print(login_response.text)
    print(login_response.status_code)
    if str(login_response.status_code) == "200":
        None
    else:
        print("Error sending login post request, contact staff/support")
        input("press any key to close the bot...")
        sys.exit()
    
    smscode = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Input SMS Code: '} {reset_color}")

    login_sms_response = session.post(
        "https://api.revolut.com/signin",
        headers =  {
            'Host': 'api.revolut.com',
            'accept': '*/*',
            'x-client-version': revolutVersion,
            'x-push-id': getPushID(),
            'x-timezone': 'Europe/London',
            'accept-language': 'en-GB;q=1.0',
            'user-agent': revolutUserAgent,
            'x-device-id': DEVICE_ID,
            'x-integrity-check': "Y29tLnJldm9sdXQuY29yZS5tb2JpbGVfc2VydmljZXMuYXBpLmV4Y2VwdGlvbnMuTXNBcGlFeGNlcHRpb246IC04OiBJbnRlZ3JpdHkgQVBJIGVycm9yICgtOCk6IFRoZSBjYWxsaW5nIGFwcCBpcyBtYWtpbmcgdG9vIG1hbnkgcmVxdWVzdHMgdG8gdGhlIEFQSSBhbmQgaGVuY2UgaXMgdGhyb3R0bGVkLgpSZXRyeSB3aXRoIGFuIGV4cG9uZW50aWFsIGJhY2tvZmYuCiAoaHR0cHM6Ly9kZXZlbG9wZXIuYW5kcm9pZC5jb20vcmVmZXJlbmNlL2NvbS9nb29nbGUvYW5kcm9pZC9wbGF5L2NvcmUvaW50ZWdyaXR5L21vZGVsL0ludGVncml0eUVycm9yQ29kZS5odG1sI1RPT19NQU5ZX1JFUVVFU1RTKS4="
        },
        json = {
            "phone": phone_number,
            "password": passcode,
            "code": smscode
        }
    )
    
    login_sms_responsejson = login_sms_response.json()

    try:
        if str(login_sms_responsejson['nextStep']) == 'SELFIE':
            NEED_SELFIE = True
    except:
        None
        NEED_SELFIE = False
    
    try:
        accessToken = login_sms_responsejson['token']['accessCode']
        userId = login_sms_responsejson['user']['id']
    except:
        print('failed step 1 of logging in')
        input("press any key to close the bot...")
        sys.exit()

    selfieAuthToken = userId + ":" + accessToken
    authtokenuncoded = base64.b64encode(selfieAuthToken.encode('utf-8'))
    authtoken = str(authtokenuncoded)[2:-1]
    
    def selfie_login(authtoken):

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Sending Selfie Image'} {reset_color}")

        headers =  {
            'Host': 'api.revolut.com',
            'Authorization':"Basic " + authtoken,
            'accept': '*/*',
            'x-client-version': revolutVersion,
            'x-push-id': getPushID(),
            'x-timezone': 'Europe/London',
            'accept-language': 'en-GB;q=1.0',
            'user-agent': revolutUserAgent,
            'x-device-id': DEVICE_ID,
            'x-integrity-check': "Y29tLnJldm9sdXQuY29yZS5tb2JpbGVfc2VydmljZXMuYXBpLmV4Y2VwdGlvbnMuTXNBcGlFeGNlcHRpb246IC04OiBJbnRlZ3JpdHkgQVBJIGVycm9yICgtOCk6IFRoZSBjYWxsaW5nIGFwcCBpcyBtYWtpbmcgdG9vIG1hbnkgcmVxdWVzdHMgdG8gdGhlIEFQSSBhbmQgaGVuY2UgaXMgdGhyb3R0bGVkLgpSZXRyeSB3aXRoIGFuIGV4cG9uZW50aWFsIGJhY2tvZmYuCiAoaHR0cHM6Ly9kZXZlbG9wZXIuYW5kcm9pZC5jb20vcmVmZXJlbmNlL2NvbS9nb29nbGUvYW5kcm9pZC9wbGF5L2NvcmUvaW50ZWdyaXR5L21vZGVsL0ludGVncml0eUVycm9yQ29kZS5odG1sI1RPT19NQU5ZX1JFUVVFU1RTKS4="
        }
        try:
            files = {'selfie': ('selfie', open(path.join(PATH_REV_PERSONAL_FOLDER, f"selfie_{str(account_num)}.jpg"), 'rb'), 'image/jpg')}
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Failed to get Selfie File'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'If you are on windows 11 or 10 try removing the .jpg from the image file'} {reset_color}")
            input("Press enter to exit...")
            sys.exit()

        selfie_response = session.post("https://api.revolut.com/biometric-signin/selfie", files=files, headers=headers)

        selfie_id = selfie_response.json()['id']

        selfie_response_post = session.post("https://api.revolut.com/biometric-signin/confirm/" + selfie_id, headers=headers)
        selfie_response_json = selfie_response_post.json()
        print(selfie_response_json)

        estimatedTimeToComplete = str(selfie_response_json['estimatedTimeToComplete'])
        waitTime = int(estimatedTimeToComplete[2:4])
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Waiting for Selfie to be Confirmed..'} {reset_color}")
        time.sleep(waitTime)
        fully_confirmed_response = session.post("https://api.revolut.com/biometric-signin/confirm/" + selfie_id, headers=headers)
        fully_confirmed_json = fully_confirmed_response.json()

        print(fully_confirmed_json)

        try:
            accessToken = fully_confirmed_json['token']['accessCode']
            userId = fully_confirmed_json['user']['id']
            selfieAuthToken = userId + ":" + accessToken
            authtokenuncoded = base64.b64encode(selfieAuthToken.encode('utf-8'))
            authtoken = str(authtokenuncoded)[2:-1]

            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Successfully Logged In!'} {reset_color}")

            return authtoken
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Failed to Log In: Selfie Issue'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Make sure you use the selfie of the owner of the account, not the face ID'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Press enter to exit..'} {reset_color}")
            sys.exit()

    if NEED_SELFIE == True:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Selfie Required!'} {reset_color}")
        authtoken = selfie_login(authtoken)

    elif NEED_SELFIE == False:
        None
    
    with open(path.join(PATH_REV_PERSONAL_FOLDER, f"personalsession_{str(account_num)}.pkl"), 'wb') as f: #save session
        pickle.dump(session, f) 

    return authtoken 


def create_new_session_file(account_num, phone_number):

    with open(path.join(PATH_REV_PERSONAL_FOLDER, f"personalsession_{str(account_num)}.pkl"),'wb') as file:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Created New Session File'} {reset_color}")


def log_authtoken(authtoken, DEVICE_ID, account_num):

    df = pd.read_csv(PATH_REV_PERSONAL_PROFILES)
    df.at[account_num-1, 'Token'] = authtoken
    df.to_csv(PATH_REV_PERSONAL_PROFILES, index=False)

    df.at[account_num-1, 'DeviceID'] = DEVICE_ID
    df.to_csv(PATH_REV_PERSONAL_PROFILES, index=False)


def get_session(phone_number, passcode, row, account_num):

    if option == 1:
        try: 
            tokenrev = row[2]
            DEVICE_ID = row[3]
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Missing columns in csv..'} {reset_color}")
            input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Press enter to exit: '} {reset_color}")
            sys.exit()


        if len(tokenrev)==0:

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Starting Session..'} {reset_color}")
            
            session = requests.Session() 

            create_new_session_file(account_num, phone_number)
            
            DEVICE_ID = getDeviceID()
            
            authtoken = login(DEVICE_ID, phone_number, passcode, session, account_num)

            log_authtoken(authtoken, DEVICE_ID, account_num)

            solve_challenges(authtoken, DEVICE_ID, session, phone_number, account_num)

        else:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Open Session Found!'} {reset_color}")

            try:
                with open(path.join(PATH_REV_PERSONAL_FOLDER, f"personalsession_{str(account_num)}.pkl"), 'rb') as f: 
                    session = pickle.load(f) 

                authtoken = tokenrev

            except EOFError:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'No Current Requests Session Found, creating one..'} {reset_color}")
                session = requests.Session() 

                create_new_session_file(account_num)

                DEVICE_ID = getDeviceID()
                
                authtoken = login(DEVICE_ID, phone_number, passcode, session, account_num)

                log_authtoken(authtoken, DEVICE_ID, account_num)

            solve_challenges(authtoken, DEVICE_ID, session, phone_number, account_num)

    elif option == 2:

        try: 
            tokenrev = row[2]
            DEVICE_ID = row[3]
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Missing columns in csv..'} {reset_color}")
            input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Press enter to exit: '} {reset_color}")
            sys.exit()


        if len(tokenrev)==0:

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Starting Session..'} {reset_color}")
            
            session = requests.Session() 

            create_new_session_file(account_num, phone_number)
            
            DEVICE_ID = getDeviceID()
            
            authtoken = login(DEVICE_ID, phone_number, passcode, session, account_num)

            log_authtoken(authtoken, DEVICE_ID, account_num)

        else:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Open Session Found Already!'} {reset_color}")


def setup_profiles(account_num):

    try:
        with open(PATH_REV_PERSONAL_PROFILES) as accounts:
            mycsv = accounts.readlines()
            y = mycsv[account_num].rstrip('\n')
            row = y.split(",")
            phone_number = row[0]
            passcode = row[1]

            if len(phone_number)==0 or len(passcode)==0:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'No Phone Number or Passcode Found in CSV'} {reset_color}")
                input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Press enter to exit: '} {reset_color}")
                sys.exit() 
        
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'No profiles loaded, please add them.'} {reset_color}")
        input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{phone_number}] [{1}] {'Press enter to exit: '} {reset_color}")
        
    get_session(phone_number, passcode, row, account_num)


def thread_sessions():

    global SOLVE_DELAY, webhook, option

    SOLVE_DELAY = jsonerrorlogs.jsonrevpersonalsolvedelay()
    webhook = jsonerrorlogs.jsonwebhook()

    amount_profiles = len(pd.read_csv(PATH_REV_PERSONAL_PROFILES))
    
    getRevolutVersion_UserAgent()

    account_num = 1

    print("Reminder! if you havent loaded your accounts make sure to do so first!")
    print("")
    print("What would you like to do: ")
    print("")
    print("1. Solve 3Ds")
    print("2. Load Revolut Accounts")
    print("")
    print("3. Back")
    print("")
    option = int(input("Option: "))

    if option == 1:
        for i in range(amount_profiles):

            s = threading.Thread(target=setup_profiles, args=[account_num])
            s.start()

            account_num+=1

            time.sleep(2)

        if amount_profiles == 0:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] [{1}] {'No Details Found in CSV'} {reset_color}")
            input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] [{1}] {'Press enter to exit: '} {reset_color}")
        else:
            s.join()

    elif option == 2:

        for i in range(amount_profiles):

            s = threading.Thread(target=setup_profiles, args=[account_num])
            s.start()

            account_num+=1

            time.sleep(2)

            if amount_profiles == 0:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] [{1}] {'No Details Found in CSV'} {reset_color}")
                input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] [{1}] {'Press enter to exit: '} {reset_color}")
            else:
                s.join()

    elif option == 3:
        return "BACK"


        

