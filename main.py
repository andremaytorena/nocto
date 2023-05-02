import requests, shutil, os, sys, urllib, json, time
from os import path
from Paths.paths import PATH_SETTINGS
from noctotools import NoctoTools
from noctoraffles import NoctoRaffles
from Loader.osSelector import clearScreen
from pypresence import Presence
import threading

def discord_rpc():
    client_id = "1048579245103919205"
    start = int(time.time())
    try:
        RPC = Presence(client_id)
        RPC.connect()
        RPC.update(
            large_image = "noctotoolslogo",
            large_text = "NOCTO",
            details = "Viewing Modules..",
            # state = "NOCTO",
            buttons = [{'label': 'Discord', 'url': 'https://discord.gg/FKd4SUJTqU'}],
            start = start
        )
    except:
        pass

def logged(username, license_key):

    webhook = 'https://discord.com/api/webhooks/1032997883902967808/sGEFQREhCtu-Wa0db4H7wn_uBLo-z-h7c8Hyw3qRLGf8QDtxva99ROQByLrAdM7MR23X'
    web = {
    "content": None,
    "embeds": [
        {
        "title": "Logged In User",
        "color": None,
        "fields": [
            {
            "name": "License",
            "value": license_key
            },
            {
            "name": "Discord",
            "value": username
            }
        ]
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=web)

currentVersion = "0.2.1"

def main(username, license_key):
    
    clearScreen()
    
    threading.Thread(target=discord_rpc).start()

    logged(username, license_key)
    print("                                                _   __           __        ") 
    print("                                               / | / /___  _____/ /_____   ")
    print("                                              /  |/ / __ \/ ___/ __/ __ \  ")
    print("                                             / /|  / /_/ / /__/ /_/ /_/ /  ")
    print("                                            /_/ |_/\____/\___/\__/\____/   ")
    print("")
    print("")
    print(f"                                                     Version {currentVersion}")
    print(f"                                                Welcome Back",  username)
    print("")
    print("")
    print("                                 1. NoctoTools                           2. NoctoRaffles")
    print("")
    print("")
    option = input("                                                     Option: ")

    if option == "1":
        NoctoTools(username, license_key)
    elif option == "2":
        NoctoRaffles(username, license_key)

#pyarmor pack -e "--onefile --icon logo.ico --add-data 'ca.crt;seleniumwire' --add-data 'ca.key;seleniumwire'" main.py

def checkVersion():
    print("Checking for updates...")
    r = requests.get("https://noctotools.herokuapp.com/version")
    newestVersion = r.text
    if newestVersion == currentVersion:
        print("No updates found")
    else:
        downloadUpdate(newestVersion)

def downloadUpdate(newestVersion):
    print("Update found, downloading...")
    url = "https://noctotools.herokuapp.com/download"

    output_file = f"NoctoTools V{newestVersion}.exe"
    with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    print("Opening new version...")
    cwd = os.getcwd()
    os.startfile(path.join(cwd, f'NoctoTools V{newestVersion}.exe'))
    sys.exit()


def installation(license_key):

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)

    data["LicenseKey"] = license_key
    with open(PATH_SETTINGS, "w") as configFile:
        json.dump(data, configFile, indent=4)

    if len(settings["Webhook"])==0 and len(settings["2captcha_key"]) ==0 :
        print('Installation process..')
        i_webhook = input("[Required] Input your discord webhook: ")
        i_2captcha_key = input("[Optional] Input your 2captcha key: ")

        data["Webhook"] = i_webhook
        with open(PATH_SETTINGS, "w") as configFile:
            json.dump(data, configFile, indent=4)

        data["2captcha_key"] = i_2captcha_key
        with open(PATH_SETTINGS, "w") as configFile:
            json.dump(data, configFile, indent=4)
    else:
        None
                    

def start():

    def verify_license(license_key):
        headers = {"api_key": license_key}
        res = requests.get("https://noctotools.herokuapp.com/authorize_license", headers=headers)
        try: 
            if res.json()['authorized'] == 'Validated':
                print('License is good to go!')      
        except:
            print("License not found!")
            license_key = input('Enter your license key: ')
            verify_license(license_key)

        username = res.json()['discord']
        checkVersion()
        installation(license_key)
        main(username, license_key)

    global data
    with open(PATH_SETTINGS) as json_file:
        settings = json.load(json_file)
    
    with open(PATH_SETTINGS, "r") as configFile:
        data = json.load(configFile)

    license_settings = (bool(settings['LicenseKey']))

    if license_settings == True:
        license_key = (settings['LicenseKey'])
        verify_license(license_key)
    else:
        license_key = input('Enter your license key: ')
        verify_license(license_key)

start()