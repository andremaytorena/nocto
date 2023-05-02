import json, time, sys, os
from Paths.paths import PATH_SETTINGS

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

    try:
        retrylimit = settings['RetryLimit']
    except:
        newdata = {k.replace("Retry_Limit", "RetryLimit"): v for k, v in settings.items()}
        with open(PATH_SETTINGS, "w") as f:
            json.dump(newdata, f, indent=4)
        retrylimit = newdata['RetryLimit']

    if retrylimit:
        return retrylimit
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have a retry limit saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your retry limit: '} {reset_color}")
        add_value("RetryLimit", value)
        return value

def jsonentrydelay():

    retrylimit = settings['EntryDelay']
    if retrylimit:
        return retrylimit
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have an entry delay saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your entry delay: '} {reset_color}")
        add_value("EntryDelay", value)
        return value

def jsonthreads():

    retrylimit = settings['Threads']
    if retrylimit:
        return retrylimit
    else:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You do not have amount of threads saved in your settings file, please follow instructions below:'} {reset_color}")
        value = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Input your amount of threads: '} {reset_color}")
        add_value("Threads", value)
        return value

def proxiesfile(PATH_PROXIES):

    with open(PATH_PROXIES, 'r') as fp:
        amount_of_proxy_lines = len(fp.readlines())
    
    if amount_of_proxy_lines == 0:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You have not added proxies into your proxies.txt file, please follow instructions below:'} {reset_color}")
        input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Press enter to open your proxies file (make sure to press save!): '} {reset_color}")
        os.startfile(PATH_PROXIES)
        input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'Press enter once you have added them and saved the file: '} {reset_color}")
    
    else:
        None

    

        