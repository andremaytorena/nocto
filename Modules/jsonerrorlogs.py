import json, time, sys, requests, zipfile, os
from Paths.paths import PATH_SETTINGS, MAIN_PATH, PATH_CHROME_ZIP, PATH_CHROME_DRIVER
from os import path

jsonfile = open(PATH_SETTINGS)
settings = json.load(jsonfile)

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def add_value(key, value):

    with open(PATH_SETTINGS, "r") as configFile:
        data = json.load(configFile)

    data[key] = value
    with open(PATH_SETTINGS, "w") as configFile:
        json.dump(data, configFile, indent=4)

def double_add_value(key1, key2,  value):

    with open(PATH_SETTINGS, "r") as configFile:
        data = json.load(configFile)

    data[key1][key2] = value
    with open(PATH_SETTINGS, "w") as configFile:
        json.dump(data, configFile, indent=4)

def jsonwebhook():

    webhook = settings['Webhook']
    if webhook:
        return webhook
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a discord webhook saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your discord webhook: '} {reset_color}")
        add_value("Webhook", value)
        return value

def json2captcha():

    captchakey = settings['2captcha_key']
    if captchakey:
        return captchakey
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a 2captcha key saved in your settings file, please follow instructions below:'} {reset_color}")
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Make an account on https://2captcha.com then add 3-5 quid into the account,'} {reset_color}")
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'your 2captcha key is on your dashboard and its called api key'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your 2captcha key: '} {reset_color}")
        add_value("2captcha_key", value)
        return value

def jsonretrylimit():

    retrylimit = settings['RetryLimit']
    if retrylimit:
        return retrylimit
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a retry limit saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your retry limit: '} {reset_color}")
        add_value("RetryLimit", value)
        return value

def jsongmailcountrycode():

    countrycode = settings['GmailGenerator']['Country_Code']
    if countrycode:
        return countrycode
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a country code saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your country code (16 for UK): '} {reset_color}")
        double_add_value("GmailGenerator", "Country_Code", value)
        return value

def jsongmailphoneauth():

    phoneverification = settings['GmailGenerator']['Phone_Verification_Mode']
    if phoneverification:
        return phoneverification
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a phone verification mode saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your phone verification mode (manual or smsactivateru): '} {reset_color}")
        double_add_value("GmailGenerator", "Phone_Verification_Mode", value)
        return value

def jsonsmsactivatekey():

    smsactivatekey = settings['GmailGenerator']['SMSactivateAPI_KEY']
    if smsactivatekey:
        return smsactivatekey
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have an smsactivate key saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your smsactivate key: '} {reset_color}")
        double_add_value("GmailGenerator", "SMSactivateAPI_KEY", value)
        return value

def jsongmailbrowsermode():

    browsermode = settings['GmailGenerator']['browser_mode']
    if browsermode:
        return browsermode
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a browser mode saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your browser mode (headless or headfull): '} {reset_color}")
        double_add_value("GmailGenerator", "browser_mode", value)
        return value

def jsonrevpersonalsolvedelay():

    solvedelay = settings['revolutnormal']['solve_delay']
    if solvedelay:
        return int(solvedelay)
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a solve delay saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your solve delay in seconds (advised: 2): '} {reset_color}")
        double_add_value("revolutnormal", "solve_delay", value)
        return value

def jsonrevbusinesssolvedelay():

    solvedelay = settings['revolutbusiness']['solve_delay']
    if solvedelay:
        return int(solvedelay)
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a solve delay saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your solve delay in seconds (advised: 2): '} {reset_color}")
        double_add_value("revolutbusiness", "solve_delay", value)
        return value


def updateChromeDriver():

    print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Your chromedriver is out of date, follow instructions below: '} {reset_color}")
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Go to google and type this in: chrome://version/ then at the top the first 3 numbers is your version:  '} {reset_color}")
    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Then go to https://chromedriver.chromium.org/downloads and copy the version which has the same first 3 numbers:  '} {reset_color}")
    version = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input the chromedriver version: '} {reset_color}")

    try:
        url = 'https://chromedriver.storage.googleapis.com/{0}/{1}'.format(version, 'chromedriver_win32.zip')
        r = requests.get(url, allow_redirects=True)
        open(PATH_CHROME_ZIP, 'wb').write(r.content)
        with zipfile.ZipFile(PATH_CHROME_ZIP, "r") as zip_ref:
            zip_ref.extractall(MAIN_PATH)
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Sucessfully Updated Chromedriver!'} {reset_color}")
    except:
        None








        


        