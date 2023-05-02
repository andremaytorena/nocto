import os, csv, json, requests, zipfile, sys
from os import path

def get_desktop_path():

    cwd = os.getcwd()
    return cwd


def settings_file():
    data = {

        "LicenseKey":"",
        
        "Stripe": {
            "API_Key": "",
            "CardHolder_ID": ""
        },

        "GmailGenerator": {
            "Phone_Verification_Mode": "smsactivateru",
            "Country_Code":"",
            "browser_mode":"headfull",
            "SMSactivateAPI_KEY": ""
        },

        "revolutnormal": {
            "solve_delay": "2"
        },
        "revolutbusiness": {
            "solve_delay": "2",
            "email": "",
            "password": ""
        },

        "RetryLimit": "3",
        "2captcha_key": "",
        "EntryDelay": "30",
        "Threads": "1",

        "Webhook": ""
    }
    
    return data


def set_paths_noctotools():

    #settings json
    global PATH_SETTINGS
    PATH_SETTINGS = path.join(MAIN_PATH, "settings.json")
    if os.path.exists(PATH_SETTINGS):
        False  
    else:
        writeToJSONFile() #change this to write actual json file

    try:
        updated_settings = settings_file()
        jsonfile = open(PATH_SETTINGS)
        current_settings = json.load(jsonfile)

        if current_settings == updated_settings:
            None
        else:

            keys_to_add = set(updated_settings.keys()) - set(current_settings.keys())

            # add the keys from the second file to the first file
            for key in keys_to_add:
                current_settings[key] = updated_settings[key]

            # save the modified file
            with open(PATH_SETTINGS, 'w') as f:
                json.dump(current_settings, f, indent=4)
    except:

        os.system("cls")
        print("Settings File Corrupted: Delete the settings.json and re run the bot.")
        input("Press enter to exit: ")
        sys.exit()

    #proxies txt
    global PATH_PROXIES
    PATH_PROXIES = path.join(MAIN_PATH, "proxies.txt")
    if os.path.exists(PATH_PROXIES):
        False  
    else:
        with open(PATH_PROXIES, 'w', newline=''):
            False

    #address jigger
    global PATH_ADDRESSJIGGER_FOLDER, PATH_BDAY_FOLDER, PATH_ADDRESSJIGGER_ADDRESSES, PATH_ADDRESSJIGGER_RESULT, PATH_SPLITTER_FOLDER, PATH_SIZE_RANDOMIZER_FOLDER, PATH_NAME_FOLDER, PATH_CATCHALL_FOLDER, PATH_PASSWORD_FOLDER, PATH_PHONE_FOLDER, PATH_POSTCODE_FOLDER

    PATH_CREDENTIALGENERATOR_FOLDER = path.join(MAIN_PATH, "CredentialGenerator")
    PATH_CARDGENERATOR_FOLDER = path.join(MAIN_PATH, "CardGenerator")
    PATH_EMAILGENERATOR_FOLDER = path.join(MAIN_PATH, "EmailGenerator")
    PATH_REVOLUTSOLVERS_FOLDER = path.join(MAIN_PATH, "RevolutSolvers")
    PATH_ORDERTRACKERS_FOLDER = path.join(MAIN_PATH, "OrderTrackers")
    PATH_RANDOMGENERATORS_FOLDER = path.join(MAIN_PATH, "RandomGenerators")

    PATH_ADDRESSJIGGER_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "AddressJigger")
    PATH_ADDRESSJIGGER_ADDRESSES = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "AddressJigger", "addresses.csv")
    PATH_ADDRESSJIGGER_RESULT = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "AddressJigger", "result.csv")

    PATH_NAME_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "NameGenerator")
    PATH_CATCHALL_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "CatchallGenerator")
    PATH_PASSWORD_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "PasswordGenerator")
    PATH_PHONE_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "PhoneGenerator")
    PATH_BDAY_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "BirthdateGenerator")
    PATH_POSTCODE_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "PostcodeGenerator")
    PATH_SIZE_RANDOMIZER_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "SizeRandomizer")
    PATH_SPLITTER_FOLDER = path.join(PATH_CREDENTIALGENERATOR_FOLDER, "CSVsplitter")

    if os.path.exists(PATH_CREDENTIALGENERATOR_FOLDER):
        False  
    else:
        os.mkdir(PATH_CREDENTIALGENERATOR_FOLDER)

    if os.path.exists(PATH_CARDGENERATOR_FOLDER):
        False  
    else:
        os.mkdir(PATH_CARDGENERATOR_FOLDER)

    if os.path.exists(PATH_EMAILGENERATOR_FOLDER):
        False  
    else:
        os.mkdir(PATH_EMAILGENERATOR_FOLDER)

    if os.path.exists(PATH_REVOLUTSOLVERS_FOLDER):
        False  
    else:
        os.mkdir(PATH_REVOLUTSOLVERS_FOLDER)
    
    if os.path.exists(PATH_ORDERTRACKERS_FOLDER):
        False  
    else:
        os.mkdir(PATH_ORDERTRACKERS_FOLDER)

    if os.path.exists(PATH_RANDOMGENERATORS_FOLDER):
        False  
    else:
        os.mkdir(PATH_RANDOMGENERATORS_FOLDER)

    directories_folder = {
        "CredentialGenerator": "",
        "CardGenerator": "",
    }

    for folder, files in directories_folder.items():
        path_folder = os.path.join(MAIN_PATH, folder)
        if os.path.exists(path_folder):
            False
        else:
            os.mkdir(path_folder)

    directories_credentials = {
        "NameGenerator": "names.csv",
        "CatchallGenerator": "emails.csv",
        "PasswordGenerator": "passwords.csv",
        "PhoneGenerator": "phones.csv",
        "BirthdateGenerator": "birthdates.csv",
        "PostcodeGenerator": "postcodes.csv",
        "SizeRandomizer": "sizes.csv",
        "CSVsplitter": "main.csv",
        "AddressJigger": ["addresses.csv", "result.csv"]
    }

    for folder, files in directories_credentials.items():
        path_folder = os.path.join(PATH_CREDENTIALGENERATOR_FOLDER, folder)
        if os.path.exists(path_folder):
            False
        else:
            os.mkdir(path_folder)

        for file in files:
            path_file = os.path.join(path_folder, file)
            if os.path.exists(path_file):
                False
            else:
                print("File not exist, creating one...")
                headers = ['Address1', 'Address2']
                create_csv(headers, path_file)
    
    #Stripe Card Generator
    global PATH_STRIPE
    PATH_STRIPE = path.join(PATH_CARDGENERATOR_FOLDER, "StripeGenerator")
    if os.path.exists(PATH_STRIPE):
        False  
    else:
        os.mkdir(PATH_STRIPE)

    #snkrs/emailpassword
    global PATH_SNKRSEMAIL_PASSWORD_FOLDER, PATH_SNKRS_1, PATH_SNKRS_2, PATH_SNKRS_3
    PATH_SNKRSEMAIL_PASSWORD_FOLDER = path.join(PATH_RANDOMGENERATORS_FOLDER, "SNKRSEmailPasswordConverter")
    PATH_SNKRS_1 = path.join(PATH_RANDOMGENERATORS_FOLDER, "SNKRSEmailPasswordConverter", "EMAILPASSWORD.csv")
    PATH_SNKRS_2 = path.join(PATH_RANDOMGENERATORS_FOLDER, "SNKRSEmailPasswordConverter", "EMAILPROFILESIZEPROXY.csv")
    PATH_SNKRS_3 = path.join(PATH_RANDOMGENERATORS_FOLDER, "SNKRSEmailPasswordConverter", "FULL_PROFILE.csv")
    if os.path.exists(PATH_SNKRSEMAIL_PASSWORD_FOLDER):
        False  
    else:
        os.mkdir(PATH_SNKRSEMAIL_PASSWORD_FOLDER)

    if os.path.exists(PATH_SNKRS_1):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password'] 
        CSV_PATH = PATH_SNKRS_1
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_SNKRS_2):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Profile', 'Size', 'Proxy'] 
        CSV_PATH = PATH_SNKRS_2
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_SNKRS_3):
        False
    else:
        print("File not exist, creating one..")
        headers = ['First Name', 'Middle Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Country', 'Zip', 'State', 'Phone Number', 'CC Number', 'Expiry Month', 'Expiry Year', 'CVV', 'Profile Name'] 
        CSV_PATH = PATH_SNKRS_3
        create_csv(headers, CSV_PATH)

    #icloud email gen
    global PATH_ICLOUD_GEN_FOLDER, PATH_ICLOUD_GEN
    PATH_ICLOUD_GEN_FOLDER = path.join(PATH_EMAILGENERATOR_FOLDER, "iCloud")
    PATH_ICLOUD_GEN = path.join(PATH_EMAILGENERATOR_FOLDER, "iCloud", "emails.csv")
    if os.path.exists(PATH_ICLOUD_GEN_FOLDER):
        False  
    else:
        os.mkdir(PATH_ICLOUD_GEN_FOLDER)

    #sims
    global PATH_SIMCARDS_FOLDER, PATH_SIMCARDS_PROFILES
    PATH_SIMCARDS_FOLDER = path.join(PATH_RANDOMGENERATORS_FOLDER, "SimCards")
    PATH_SIMCARDS_PROFILES = path.join(PATH_RANDOMGENERATORS_FOLDER, "SimCards", "profiles.csv")
    if os.path.exists(PATH_SIMCARDS_FOLDER):
        False  
    else:
        os.mkdir(PATH_SIMCARDS_FOLDER)
    if os.path.exists(PATH_SIMCARDS_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Store', 'First Name', 'Last Name', 'addy1', 'addy2', 'city', 'postcode']
        CSV_PATH = PATH_SIMCARDS_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_GMAIL_EMAILS_FOLDER, PATH_GMAIL_EMAILS, PATH_GMAIL_CREATED
    PATH_GMAIL_EMAILS_FOLDER = path.join(PATH_EMAILGENERATOR_FOLDER, "GmailGenerator")
    PATH_GMAIL_EMAILS = path.join(PATH_EMAILGENERATOR_FOLDER, "GmailGenerator", "profiles.csv")
    PATH_GMAIL_CREATED = path.join(PATH_EMAILGENERATOR_FOLDER, "GmailGenerator", "generated_emails.csv")
    if os.path.exists(PATH_GMAIL_EMAILS_FOLDER):
        False  
    else:
        os.mkdir(PATH_GMAIL_EMAILS_FOLDER)

    if os.path.exists(PATH_GMAIL_EMAILS):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password', 'First Name', 'Last Name', 'Recovery Email', 'Birthdate Day', 'Birthdate Month', 'Birthdate Year', 'Gender (M/F)', 'Phone'] 
        CSV_PATH = PATH_GMAIL_EMAILS
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_GMAIL_CREATED):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password'] 
        CSV_PATH = PATH_GMAIL_CREATED
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)
    
    global PATH_PROFILECHECKER_FOLDER, PATH_PROFILECHECKER_PROFILES, PATH_PROFILECHECKER_PREFETCHED, PATH_PROFILECHECKER_NEW
    PATH_PROFILECHECKER_FOLDER = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProfileChecker")
    PATH_PROFILECHECKER_PROFILES = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProfileChecker", "profiles.csv")
    PATH_PROFILECHECKER_PREFETCHED = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProfileChecker", "prefetched.csv")
    PATH_PROFILECHECKER_NEW = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProfileChecker", "new.csv")
    if os.path.exists(PATH_PROFILECHECKER_FOLDER):
        False  
    else:
        os.mkdir(PATH_PROFILECHECKER_FOLDER)

    if os.path.exists(PATH_PROFILECHECKER_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password'] 
        CSV_PATH = PATH_PROFILECHECKER_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_PROFILECHECKER_PREFETCHED):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email']
        CSV_PATH = PATH_PROFILECHECKER_PREFETCHED
        create_csv(headers, CSV_PATH)


    global PATH_WEBDE_FOLDER, PATH_WEBDE_PROFILES
    PATH_WEBDE_FOLDER = path.join(PATH_EMAILGENERATOR_FOLDER, "WebDeGenerator")
    PATH_WEBDE_PROFILES = path.join(PATH_EMAILGENERATOR_FOLDER, "WebDeGenerator", "profiles.csv")
    if os.path.exists(PATH_WEBDE_FOLDER):
        False  
    else:
        os.mkdir(PATH_WEBDE_FOLDER)
    
    if os.path.exists(PATH_WEBDE_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password', 'FirstName', 'LastName', 'AddressLine1', 'City', 'Postcode', 'CountryCode', 'PhoneNumber', 'Birthday', 'Gender'] 
        CSV_PATH = PATH_WEBDE_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_REV_FOLDER, PATH_REV_PROFILES, PATH_REV_CARDS
    PATH_REV_FOLDER = path.join(PATH_CARDGENERATOR_FOLDER, "RevolutBusiness")
    PATH_REV_PROFILES = path.join(PATH_CARDGENERATOR_FOLDER, "RevolutBusiness", "profiles.csv")
    PATH_REV_CARDS = path.join(PATH_CARDGENERATOR_FOLDER, "RevolutBusiness", "cards.csv")
    if os.path.exists(PATH_REV_FOLDER):
        False  
    else:
        os.mkdir(PATH_REV_FOLDER)

    if os.path.exists(PATH_REV_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password', 'Employee Email'] 
        CSV_PATH = PATH_REV_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_REV_CARDS):
        False
    else:
        print("File not exist, creating one..")
        headers = ['name', 'ccnum', 'month', 'year', 'cvv'] 
        CSV_PATH = PATH_REV_CARDS
        create_csv(headers, CSV_PATH)

    global PATH_PRODIRECT_FOLDER, PATH_PRODIRECT_PROFILES
    PATH_PRODIRECT_FOLDER = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProDirect")
    PATH_PRODIRECT_PROFILES = path.join(PATH_RANDOMGENERATORS_FOLDER, "ProDirect", "profiles.csv")
    if os.path.exists(PATH_PRODIRECT_FOLDER):
        False  
    else:
        os.mkdir(PATH_PRODIRECT_FOLDER)

    if os.path.exists(PATH_PRODIRECT_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password', 'First Name', 'Last Name', 'Bday (25-10-2000)'] 
        CSV_PATH = PATH_PRODIRECT_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_NIKEORDERTRACKER_FOLDER, PATH_NIKEORDERTRACKER_PROFILES
    PATH_NIKEORDERTRACKER_FOLDER = path.join(PATH_ORDERTRACKERS_FOLDER, "NikeOrderTracker")
    PATH_NIKEORDERTRACKER_PROFILES = path.join(PATH_ORDERTRACKERS_FOLDER, "NikeOrderTracker", "profiles.csv")
    if os.path.exists(PATH_NIKEORDERTRACKER_FOLDER):
        False  
    else:
        os.mkdir(PATH_NIKEORDERTRACKER_FOLDER)

    if os.path.exists(PATH_NIKEORDERTRACKER_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Order Number'] 
        CSV_PATH = PATH_NIKEORDERTRACKER_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_COURIERTRACKER_FOLDER, PATH_COURIERTRACKER_DPD_FOLDER, PATH_COURIERTRACKER_EVRI_FOLDER, PATH_COURIERTRACKER_DPD_PROFILES, PATH_COURIERTRACKER_EVRI_PROFILES
    PATH_COURIERTRACKER_FOLDER = path.join(PATH_ORDERTRACKERS_FOLDER, "CourierBulkTracker")
    PATH_COURIERTRACKER_DPD_FOLDER = path.join(PATH_ORDERTRACKERS_FOLDER, "CourierBulkTracker", "DPD")
    PATH_COURIERTRACKER_EVRI_FOLDER = path.join(PATH_ORDERTRACKERS_FOLDER, "CourierBulkTracker", "EVRI")
    PATH_COURIERTRACKER_DPD_PROFILES = path.join(PATH_ORDERTRACKERS_FOLDER, "CourierBulkTracker", "DPD", "profiles.csv")
    PATH_COURIERTRACKER_EVRI_PROFILES = path.join(PATH_ORDERTRACKERS_FOLDER, "CourierBulkTracker", "EVRI", "profiles.csv")
    if os.path.exists(PATH_COURIERTRACKER_FOLDER):
        False  
    else:
        os.mkdir(PATH_COURIERTRACKER_FOLDER) 

    if os.path.exists(PATH_COURIERTRACKER_DPD_FOLDER):
        False  
    else:
        os.mkdir(PATH_COURIERTRACKER_DPD_FOLDER)

    if os.path.exists(PATH_COURIERTRACKER_EVRI_FOLDER):
        False  
    else:
        os.mkdir(PATH_COURIERTRACKER_EVRI_FOLDER)

    if os.path.exists(PATH_COURIERTRACKER_DPD_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Tracking URL/Number', 'Postcode'] 
        CSV_PATH = PATH_COURIERTRACKER_DPD_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_COURIERTRACKER_EVRI_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Tracking URL/Number', 'Postcode'] 
        CSV_PATH = PATH_COURIERTRACKER_EVRI_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_MESHTRACKER_FOLDER, PATH_MESHTRACKER_PROFILES
    PATH_MESHTRACKER_FOLDER = path.join(PATH_ORDERTRACKERS_FOLDER, "MeshOrderTracker")
    PATH_MESHTRACKER_PROFILES = path.join(PATH_ORDERTRACKERS_FOLDER, "MeshOrderTracker", "profiles.csv")
    if os.path.exists(PATH_MESHTRACKER_FOLDER):
        False  
    else:
        os.mkdir(PATH_MESHTRACKER_FOLDER)

    if os.path.exists(PATH_MESHTRACKER_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Store', 'Order ID', 'Postcode'] 
        CSV_PATH = PATH_MESHTRACKER_PROFILES
        create_csv(headers, CSV_PATH)
    

    global PATH_REV_PERSONAL_PROFILES, PATH_REV_PERSONAL_FOLDER
    PATH_REV_PERSONAL_FOLDER = path.join(PATH_REVOLUTSOLVERS_FOLDER, 'RevolutPersonal')
    PATH_REV_PERSONAL_PROFILES = path.join(PATH_REV_PERSONAL_FOLDER, 'profiles.csv')
    if os.path.exists(PATH_REV_PERSONAL_FOLDER):
        False  
    else:
        os.mkdir(PATH_REV_PERSONAL_FOLDER)

    if os.path.exists(PATH_REV_PERSONAL_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Phone Number', 'Passcode', 'Token', 'DeviceID']
        CSV_PATH = PATH_REV_PERSONAL_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_REV_BUSINESS_PROFILES, PATH_REV_BUSINESS_FOLDER
    PATH_REV_BUSINESS_FOLDER = path.join(PATH_REVOLUTSOLVERS_FOLDER, 'RevolutBusiness')
    PATH_REV_BUSINESS_PROFILES = path.join(PATH_REV_BUSINESS_FOLDER, 'profiles.csv')
    if os.path.exists(PATH_REV_BUSINESS_FOLDER):
        False  
    else:
        os.mkdir(PATH_REV_BUSINESS_FOLDER)

    if os.path.exists(PATH_REV_BUSINESS_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Email', 'Password', 'Token', 'DeviceID']
        CSV_PATH = PATH_REV_BUSINESS_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_NIKEGEN_FOLDER, PATH_NIKE_PROFILES, PATH_PROXYEXTENSION, PATH_NIKE_GENNERATED_ACCOUNTS
    PATH_NIKEGEN_FOLDER = path.join(PATH_EMAILGENERATOR_FOLDER, 'NikeGen')
    PATH_NIKE_PROFILES = path.join(PATH_NIKEGEN_FOLDER, 'profiles.csv')
    PATH_NIKE_GENNERATED_ACCOUNTS = path.join(PATH_NIKEGEN_FOLDER, 'generated_accounts.csv')
    PATH_PROXYEXTENSION = path.join(PATH_NIKEGEN_FOLDER, 'proxy_auth_plugin.zip')
    if os.path.exists(PATH_NIKEGEN_FOLDER):
        False  
    else:
        os.mkdir(PATH_NIKEGEN_FOLDER)

    if os.path.exists(PATH_NIKE_PROFILES):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Region', 'Email', 'Password', 'First Name', 'Last Name', 'Birthdate', 'Phone', 'Proxy']
        CSV_PATH = PATH_NIKE_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_NIKE_GENNERATED_ACCOUNTS):
        False
    else:
        print("File not exist, creating one..")
        headers = ['Region', 'Email', 'Password', 'First Name', 'Last Name', 'Birthdate', 'Phone', 'Proxy', 'Status']
        CSV_PATH = PATH_NIKE_GENNERATED_ACCOUNTS
        create_csv(headers, CSV_PATH)

    global PATH_PLATFORMCOMPARATOR_CSV
    PATH_PLATFORMCOMPARATOR_CSV = path.join(MAIN_PATH, 'ignore.csv')

    global PATH_CHROME_DRIVER, PATH_CHROME_ZIP
    PATH_CHROME_DRIVER = path.join(MAIN_PATH, "chromedriver.exe")
    PATH_CHROME_ZIP = path.join(MAIN_PATH, 'chromedriver.zip')

    version = requests.get("https://noctotools.herokuapp.com/chrome_version").text
    if os.path.exists(PATH_CHROME_DRIVER):
        None
    else:
        try:
            url = 'https://chromedriver.storage.googleapis.com/{0}/{1}'.format(version, 'chromedriver_win32.zip')
            r = requests.get(url, allow_redirects=True)
            open(PATH_CHROME_ZIP, 'wb').write(r.content)
            with zipfile.ZipFile(PATH_CHROME_ZIP, "r") as zip_ref:
                zip_ref.extractall(MAIN_PATH)
        except:
            None

        try:
            os.remove(PATH_CHROME_ZIP)
        except:
            None
        try:
            os.remove(path.join(MAIN_PATH, "LICENSE.chromedriver"))
        except:
            None
    

def set_paths_noctoraffles():

    PATH_NOCTORAFLES_FOLDER = path.join(MAIN_PATH, "RaffleSites")
    if os.path.exists(PATH_NOCTORAFLES_FOLDER):
        False  
    else:
        os.mkdir(PATH_NOCTORAFLES_FOLDER)

    global PATH_LOGS, PATH_FOOTPATROL_LOGS, PATH_SIZE_LOGS, PATH_HIPSTORE_LOGS, PATH_FLATSPOT_LOGS, PATH_AFEW_LOGS, PATH_ROUTEONE_LOGS, PATH_JDX_LOGS
    PATH_LOGS = path.join(MAIN_PATH, "Logs")
    PATH_FOOTPATROL_LOGS = path.join(MAIN_PATH, "Logs", "fp_logs.csv")
    PATH_SIZE_LOGS = path.join(MAIN_PATH, "Logs", "size_logs.csv")
    PATH_HIPSTORE_LOGS = path.join(MAIN_PATH, "Logs", "hipstore_logs.csv")
    PATH_FLATSPOT_LOGS = path.join(MAIN_PATH, "Logs", "flatspot_logs.csv")
    PATH_ROUTEONE_LOGS = path.join(MAIN_PATH, "Logs", "routeone_logs.csv")
    PATH_AFEW_LOGS = path.join(MAIN_PATH, "Logs", "afew_logs.csv")
    PATH_JDX_LOGS = path.join(MAIN_PATH, "Logs", "jdx_logs.csv")
    
    if os.path.exists(PATH_LOGS):
        False  
    else:
        os.mkdir(PATH_LOGS)
    
    if os.path.exists(PATH_FOOTPATROL_LOGS):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_FOOTPATROL_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)
    
    if os.path.exists(PATH_SIZE_LOGS):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_SIZE_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)

    if os.path.exists(PATH_HIPSTORE_LOGS):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_HIPSTORE_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)

    if os.path.exists(PATH_FLATSPOT_LOGS):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_FLATSPOT_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)

    if os.path.exists(PATH_ROUTEONE_LOGS):
        False
    else: 
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_ROUTEONE_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)

    if os.path.exists(PATH_AFEW_LOGS):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_AFEW_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)

    if os.path.exists(PATH_JDX_LOGS):
        False
    else: 
        headers = ['Email', 'Raffle']
        CSV_PATH = PATH_JDX_LOGS
        create_csv(headers, CSV_PATH)
        write_rows(headers, CSV_PATH)


    global PATH_FOOTPATROL_FOLDER, PATH_FOOTPATROL_PROFILES, PATH_FOOTPATROL_ACCGENPROFILES
    PATH_FOOTPATROL_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Footpatrol Launches")
    PATH_FOOTPATROL_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Footpatrol Launches", "profiles.csv")
    PATH_FOOTPATROL_ACCGENPROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Footpatrol Launches", "account_gen.csv")
    if os.path.exists(PATH_FOOTPATROL_FOLDER):
        False  
    else:
        os.mkdir(PATH_FOOTPATROL_FOLDER)

    if os.path.exists(PATH_FOOTPATROL_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_FOOTPATROL_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_FOOTPATROL_ACCGENPROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Password', 'First Name', 'Last Name']
        CSV_PATH = PATH_FOOTPATROL_ACCGENPROFILES
        create_csv(headers, CSV_PATH)

    global PATH_SIZE_FOLDER, PATH_SIZE_PROFILES, PATH_SIZE_ACCGENPROFILES
    PATH_SIZE_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Size Launches")
    PATH_SIZE_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Size Launches", "profiles.csv")
    PATH_SIZE_ACCGENPROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Size Launches", "account_gen.csv")
    if os.path.exists(PATH_SIZE_FOLDER):
        False  
    else:
        os.mkdir(PATH_SIZE_FOLDER)

    if os.path.exists(PATH_SIZE_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_SIZE_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_SIZE_ACCGENPROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Password', 'First Name', 'Last Name']
        CSV_PATH = PATH_SIZE_ACCGENPROFILES
        create_csv(headers, CSV_PATH)

    global PATH_HIPSTORE_FOLDER, PATH_HIPSTORE_PROFILES, PATH_HIPSTORE_ACCGENPROFILES
    PATH_HIPSTORE_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Hipstore Launches")
    PATH_HIPSTORE_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Hipstore Launches", "profiles.csv")
    PATH_HIPSTORE_ACCGENPROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Hipstore Launches", "account_gen.csv")
    if os.path.exists(PATH_HIPSTORE_FOLDER):
        False  
    else:
        os.mkdir(PATH_HIPSTORE_FOLDER)

    if os.path.exists(PATH_HIPSTORE_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_HIPSTORE_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_HIPSTORE_ACCGENPROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Email', 'Password', 'First Name', 'Last Name']
        CSV_PATH = PATH_HIPSTORE_ACCGENPROFILES
        create_csv(headers, CSV_PATH)

    global PATH_FLATSPOT_FOLDER, PATH_FLATSPOT_PROFILES
    PATH_FLATSPOT_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Flatspot")
    PATH_FLATSPOT_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Flatspot", "profiles.csv")
    if os.path.exists(PATH_FLATSPOT_FOLDER):
        False  
    else:
        os.mkdir(PATH_FLATSPOT_FOLDER)

    if os.path.exists(PATH_FLATSPOT_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_FLATSPOT_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_ROUTEONE_FOLDER, PATH_ROUTEONE_PROFILES
    PATH_ROUTEONE_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Route One")
    PATH_ROUTEONE_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Route One", "profiles.csv")
    if os.path.exists(PATH_ROUTEONE_FOLDER):
        False  
    else:
        os.mkdir(PATH_ROUTEONE_FOLDER)

    if os.path.exists(PATH_ROUTEONE_PROFILES):
        False
    else: 
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_ROUTEONE_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_SHOPIFY_FOLDER, PATH_SHOPIFY_PROFILES
    PATH_SHOPIFY_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Shopify")
    PATH_SHOPIFY_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Shopify", "profiles.csv")
    if os.path.exists(PATH_SHOPIFY_FOLDER):
        False  
    else:
        os.mkdir(PATH_SHOPIFY_FOLDER)

    if os.path.exists(PATH_SHOPIFY_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Base URL', 'Varient ID', 'Quantity', 'Email', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'CC Number', 'CC Month', 'CC Year', 'CVV']
        CSV_PATH = PATH_SHOPIFY_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_AFEW_FOLDER, PATH_AFEW_PROFILES
    PATH_AFEW_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "Afew")
    PATH_AFEW_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "Afew", "profiles.csv")
    if os.path.exists(PATH_AFEW_FOLDER):
        False  
    else:
        os.mkdir(PATH_AFEW_FOLDER)

    if os.path.exists(PATH_AFEW_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'Instagram']
        CSV_PATH = PATH_AFEW_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_JDX_FOLDER, PATH_JDX_PROFILES
    PATH_JDX_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "JDX")
    PATH_JDX_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "JDX", "profiles.csv")
    if os.path.exists(PATH_JDX_FOLDER):
        False  
    else:
        os.mkdir(PATH_JDX_FOLDER)

    if os.path.exists(PATH_JDX_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone']
        CSV_PATH = PATH_JDX_PROFILES
        create_csv(headers, CSV_PATH)

    global PATH_BSTN_FOLDER, PATH_BSTN_PROFILES
    PATH_BSTN_FOLDER = path.join(PATH_NOCTORAFLES_FOLDER, "BSTN")
    PATH_BSTN_PROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "BSTN", "profiles.csv")
    PATH_BSTN_ACCGENPROFILES = path.join(PATH_NOCTORAFLES_FOLDER, "BSTN", "account_gen.csv")
    if os.path.exists(PATH_BSTN_FOLDER):
        False  
    else:
        os.mkdir(PATH_BSTN_FOLDER)

    if os.path.exists(PATH_BSTN_PROFILES):
        False
    else: 
        print("File doesn't exist, creating one..")
        headers = ['Size', 'Email', 'Password', 'First Name', 'Last Name', 'Address Line 1', 'Address Line 2', 'City', 'Postcode', 'Phone', 'Instagram']
        CSV_PATH = PATH_BSTN_PROFILES
        create_csv(headers, CSV_PATH)

    if os.path.exists(PATH_BSTN_ACCGENPROFILES):
        False
    else: 
        headers = ['Email', 'Password', 'First Name', 'Last Name', 'Gender']
        CSV_PATH = PATH_BSTN_ACCGENPROFILES
        create_csv(headers, CSV_PATH)


def create_csv(headers, CSV_PATH):
    with open(CSV_PATH, 'w', newline='') as file:
        fieldnames = headers
        thewriter = csv.DictWriter(file, fieldnames=fieldnames)
        thewriter.writeheader()

def write_rows(headers, CSV_PATH):
    fieldnames = headers
    with open(CSV_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        rows = ['DO NOT DELETE', 'DO NO DELETE']
        writer.writerow(rows)


def writeToJSONFile():

    data = settings_file()

    filePathNameWExt = PATH_SETTINGS
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, indent=2)


def check_for_file():

    global MAIN_PATH
    MAIN_PATH = path.join(get_desktop_path(), 'Nocto')

    if os.path.exists(MAIN_PATH):
        False
    else:
        os.mkdir(MAIN_PATH)

    set_paths_noctotools()
    set_paths_noctoraffles()

    os.system('cls')   
    
check_for_file()

