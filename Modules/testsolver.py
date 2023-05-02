import requests, uuid, string, random
import sys, time, base64, requests, json, uuid, random, string, pickle, os, threading
from Paths.paths import PATH_SETTINGS, PATH_REV_BUSINESS_PROFILES, PATH_REV_BUSINESS_FOLDER
import Modules.jsonerrorlogs as jsonerrorlogs
from os import path
import pandas as pd

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


def clean_tokens(account_num, email):

    df = pd.read_csv(PATH_REV_BUSINESS_PROFILES)
    df.at[account_num-1, 'Token'] = ""
    df.to_csv(PATH_REV_BUSINESS_PROFILES, index=False)

    df.at[account_num-1, 'DeviceID'] = ""
    df.to_csv(PATH_REV_BUSINESS_PROFILES, index=False)

    os.remove(path.join(PATH_REV_BUSINESS_FOLDER, f"personalsession_{str(account_num)}.pkl"))

    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Please close the bot immediately and run the re load the accounts: '} {reset_color}")

    time.sleep(10)

    sys.exit()



def solve_challenges(authtoken, DEVICE_ID, session, email, account_num, password, deviceid):

    count = 1
    success_count = 1
    
    while True:
        monitor_3ds_response = requests.get(
            'https://business-mobile.revolut.com/transaction/3ds',
            headers = {
                'accept': '*/*',
                'x-client-version': '3.52',
                'x-timezone': 'Europe/London',
                'accept-language': 'en-GB;q=1.0, en-US;q=0.9',
                'user-agent': 'Revolut/com.revolut.business 3419 (iPhone; iOS 14.4.2; sp:AAS)',
                'x-device-id': DEVICE_ID,
                'x-device-model': 'iPhone9,3',
                'authorization': f'Basic {authtoken}'
            }
        )
        print(authtoken)
        print(monitor_3ds_response.json())
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{count}] {'Checking For 3DS..'} {reset_color}")

        try:
            if monitor_3ds_response.json()['message'] == 'The request should be authorized.':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{count}] {'Auth Token Expired, clearing tokens..'} {reset_color}")
                clean_tokens(account_num, email)
        except:
            None
        
        try:
            if monitor_3ds_response.json()['message'] == 'Access token expired':
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{count}] {'Auth Token Expired, clearing tokens..'} {reset_color}")
                clean_tokens(account_num, email)
        except:
            None

        try:
            id = monitor_3ds_response.json()[0]['id']
            amount_3ds = monitor_3ds_response.json()[0]['amount']
            site_3ds = monitor_3ds_response.json()[0]['merchant']['name']

            time.sleep(SOLVE_DELAY)

            solved_3ds_response = session.post(
                "https://business-mobile.revolut.com/transaction/3ds",
                headers =  {
                    'Host': 'business-mobile.revolut.com',
                    'authorization': 'Basic ' + str(authtoken),
                    'accept': '*/*',
                    'x-client-version': '3.52',
                    'x-push-id': getPushID(),
                    'x-timezone': 'Europe/London',
                    'accept-language': 'en-GB;q=1.0, en-GB;q=0.9',
                    'user-agent': 'Revolut/com.revolut.business 3419 (iPhone; iOS 14.4.2; sp:AAS)',
                    'x-device-id': DEVICE_ID,
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


def login(DEVICE_ID, email, password, session, account_num):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Sending SMS Code..'} {reset_color}")

    login_response = session.post(
        "https://business-mobile.revolut.com/auth/verify",
        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Basic YXBwOk44R3dTaW1yS0JMUFJQd1U=',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/London',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': DEVICE_ID,
            'X-device-model': 'iPhone9,3',
        },
        json = {
            'email': email,
        }
    )
    
    if str(login_response.status_code) == "200":
        None
    else:
        print("Error, wrong email!")
        input("press any key to close the bot...")
        sys.exit()
    
    confirm_url = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Input confirm email url: '} {reset_color}")

    try:
        signin64 = confirm_url.split('SIGNIN&q=')[1].split('&isMagicLinkEmail')[0]
        signid_token = base64.b64decode(signin64).decode('utf-8')
        global received_code
        received_code = signid_token.split("|")[1]
    except:
        print("Error, wrong url!")
        input("press any key to close the bot...")
        sys.exit()

    login_sms_response = session.post(
        "https://business-mobile.revolut.com/auth/confirm",
        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Basic YXBwOk44R3dTaW1yS0JMUFJQd1U=',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/London',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': DEVICE_ID,
            'X-device-model': 'iPhone9,3',
        },
        json = {
            'email': email,
            'code': received_code,
        }
    )
    login_sms_responsejson = login_sms_response.json()
    print(login_sms_responsejson)
    try:
        employeeId = login_sms_responsejson['employeeId']
        accessToken = login_sms_responsejson['accessToken']
        auth_token64 = str(employeeId) + ":" + str(accessToken)
        auth_token = base64.b64encode(auth_token64.encode("utf-8")).decode('utf-8')
    except:
        print("Error, wrong code!")
        input("press any key to close the bot...")
        sys.exit()
    
    login_employee_auth = session.post(
        "https://business-mobile.revolut.com/signin/auth",
        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'Basic {auth_token}',
            'X-Verify-Password': password,
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': DEVICE_ID,
            'X-device-model': 'iPhone9,3',
        },
        json = {}
    ).json()
    print(login_employee_auth)
    try:
        biometricAccessToken = login_employee_auth['biometricAccessToken']
        individualId = login_employee_auth['individualId']
        auth_token64 = str(individualId) + ":" + str(biometricAccessToken)
        auth_token = base64.b64encode(auth_token64.encode("utf-8")).decode('utf-8')
    except:
        print("Error, wrong employee auth code!")
        input("press any key to close the bot...")
        sys.exit()

    try:
        if str(login_employee_auth['method']) == 'SELFIE':
            NEED_SELFIE = True
    except:
        None
        NEED_SELFIE = False

    def selfie_login(authtoken, password, DEVICE_ID, account_num):

        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Sending Selfie Image'} {reset_color}")

        headers = {
            'Host': 'business-mobile.revolut.com',
            'Accept': '*/*',
            'Authorization': f'Basic {authtoken}',
            'X-Verify-Password': password,
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': DEVICE_ID,
            'X-device-model': 'iPhone9,3',
        }
        try:
            file = open(path.join(PATH_REV_BUSINESS_FOLDER, f"selfie_{str(account_num)}.jpg"), "rb")
            files = {
                'selfie': file,
            }
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Failed to get Selfie File'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'If you are on windows 11 or 10 try removing the .jpg from the image file'} {reset_color}")
            input("Press enter to exit...")
            sys.exit()

        selfie_response = session.post("https://business-mobile.revolut.com/biometric/selfie/signin", files=files, headers=headers).json()
        print(selfie_response)

        try:
            accessToken = selfie_response['accessToken']
            employeeid = selfie_response['employee']['id']
            auth_token64 = str(employeeid) + ":" + str(accessToken)
            auth_token = base64.b64encode(auth_token64.encode("utf-8")).decode('utf-8')
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Successfully Logged In!'} {reset_color}")
            print(auth_token)
            return authtoken
        
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Failed to Log In: Selfie Issue'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Make sure you use the selfie of the owner of the account, not the face ID'} {reset_color}")
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Press enter to exit..'} {reset_color}")
            sys.exit()

    if NEED_SELFIE == True:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Selfie Required!'} {reset_color}")
        authtoken = selfie_login(auth_token, password, DEVICE_ID, account_num)

    elif NEED_SELFIE == False:
        None
    
    with open(path.join(PATH_REV_BUSINESS_FOLDER, f"personalsession_{str(account_num)}.pkl"), 'wb') as f: #save session
        pickle.dump(session, f) 

    return authtoken 


def create_new_session_file(account_num, email):

    with open(path.join(PATH_REV_BUSINESS_FOLDER, f"personalsession_{str(account_num)}.pkl"),'wb') as file:
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Created New Session File'} {reset_color}")


def log_authtoken(authtoken, DEVICE_ID, account_num):

    df = pd.read_csv(PATH_REV_BUSINESS_PROFILES)
    df.at[account_num-1, 'Token'] = authtoken
    df.to_csv(PATH_REV_BUSINESS_PROFILES, index=False)

    df.at[account_num-1, 'DeviceID'] = DEVICE_ID
    df.to_csv(PATH_REV_BUSINESS_PROFILES, index=False)


def get_session(email, password, row, account_num):

    if option == 1:
        try: 
            tokenrev = row[2]
            DEVICE_ID = row[3]
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Missing columns in csv..'} {reset_color}")
            input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Press enter to exit: '} {reset_color}")
            sys.exit()


        if len(tokenrev)==0:

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Starting Session..'} {reset_color}")
            
            session = requests.Session() 

            create_new_session_file(account_num, email)
            
            deviceid = str(uuid.uuid4())
            DEVICE_ID = getDeviceID(deviceid)
            
            authtoken = login(DEVICE_ID, email, password,  session, account_num)

            log_authtoken(authtoken, DEVICE_ID, account_num)

            solve_challenges(authtoken, DEVICE_ID, session, email, account_num, password, deviceid)

        else:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Open Session Found!'} {reset_color}")

            try:
                with open(path.join(PATH_REV_BUSINESS_FOLDER, f"personalsession_{str(account_num)}.pkl"), 'rb') as f: 
                    session = pickle.load(f) 

                authtoken = tokenrev

            except EOFError:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{1}] {'No Current Requests Session Found, creating one..'} {reset_color}")
                session = requests.Session() 

                create_new_session_file(account_num)

                deviceid = str(uuid.uuid4())
                DEVICE_ID = getDeviceID(deviceid)
                
                authtoken = login(DEVICE_ID, email, password,  session, account_num)

                log_authtoken(authtoken, DEVICE_ID, account_num)
            
            solve_challenges(authtoken, DEVICE_ID, session, email, account_num, password, deviceid)

    elif option == 2:

        try: 
            tokenrev = row[2]
            DEVICE_ID = row[3]
        except:
            print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Missing columns in csv..'} {reset_color}")
            input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Press enter to exit: '} {reset_color}")
            sys.exit()


        if len(tokenrev)==0:

            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Starting Session..'} {reset_color}")
            
            session = requests.Session() 

            create_new_session_file(account_num, email)
            
            deviceid = str(uuid.uuid4())
            DEVICE_ID = getDeviceID(deviceid)
            
            authtoken = login(DEVICE_ID, email, password,  session, account_num)

            log_authtoken(authtoken, DEVICE_ID, account_num)

            solve_challenges(authtoken, DEVICE_ID, session, email, account_num, password, deviceid)

        else:
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Open Session Found Already!'} {reset_color}")


def setup_profiles(account_num):

    try:
        with open(PATH_REV_BUSINESS_PROFILES) as accounts:
            mycsv = accounts.readlines()
            y = mycsv[account_num].rstrip('\n')
            row = y.split(",")
            email = row[0]
            password = row[1]

            if len(email)==0:
                print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'No Phone Number or Passcode Found in CSV'} {reset_color}")
                input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Press enter to exit: '} {reset_color}")
                sys.exit() 
        
    except:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'No profiles loaded, please add them.'} {reset_color}")
        input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{email}] [{1}] {'Press enter to exit: '} {reset_color}")
        
    get_session(email, password, row, account_num)


def thread_sessions():

    global SOLVE_DELAY, webhook, option

    SOLVE_DELAY = jsonerrorlogs.jsonrevpersonalsolvedelay()
    webhook = jsonerrorlogs.jsonwebhook()

    amount_profiles = len(pd.read_csv(PATH_REV_BUSINESS_PROFILES))

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


        

