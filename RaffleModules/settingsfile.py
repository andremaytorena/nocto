from Paths.paths import PATH_SETTINGS
import json, os, time
from Loader.osSelector import clearScreen

def adjust_settings(key, value):
    
    data[key] = value
    with open(PATH_SETTINGS, "w") as configFile:
        json.dump(data, configFile, indent=4)

def load_current(key):

    clearScreen()

    current_value = data[key]
    print("")
    print("Current " + key + ': ' + current_value)
    print("")
    value = input("New key: ")
    print('')
    print("Successfully Changed Value")
    time.sleep(1)
    return value

def main():

    global data

    with open(PATH_SETTINGS, "r") as configFile:
        data = json.load(configFile)

    clearScreen()
    print('')
    print('1. LicenseKey')
    print('2. 2CaptchaKey')
    print('3. RetryLimit')
    print('4. EntryDelay')
    print('5. Threads')
    print('6. Webhook')
    print("")
    print('7. Go back')
    print('')
    option = input('Option: ')

    if option == '1':
        key = 'LicenseKey'
        value = load_current(key)
        adjust_settings(key, value)
        main()

    elif option == '2':
        key = '2CaptchaKey'
        value = load_current(key)
        adjust_settings(key, value)
        main()

    elif option == '3':
        key = 'RetryLimit'
        value = load_current(key)
        adjust_settings(key, value)
        main()

    elif option == '4':
        key = 'EntryDelay'
        value = load_current(key)
        adjust_settings(key, value)
        main()

    elif option == '5':
        key = 'Threads'
        value = load_current(key)
        adjust_settings(key, value)
        main()
        
    elif option == '6':
        key = 'Webhook'
        value = load_current(key)
        adjust_settings(key, value)
        main()

    elif option == '7':
        None

