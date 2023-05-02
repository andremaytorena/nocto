import time, random, csv, random, string, names, os, zipfile, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from Paths.paths import PATH_CHROME_DRIVER, PATH_PROXIES, PATH_PROXYEXTENSION, PATH_NIKE_PROFILES, PATH_NIKE_GENNERATED_ACCOUNTS
from smsactivate.api import SMSActivateAPI
import Modules.jsonerrorlogs as jsonerrorlogs

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def writeDetails(region,email,password,firstName,lastName,birthDate,phone,proxy,status):

    fieldnames = ['Region', 'Email', 'Password', 'First Name', 'Last Name', 'Birthdate', 'Phone', 'Proxy', 'Status']

    with open(PATH_NIKE_GENNERATED_ACCOUNTS) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(PATH_NIKE_GENNERATED_ACCOUNTS, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Region': region, 'Email': email, 'Password': password, 'First Name': firstName, 'Last Name': lastName, 'Birthdate': birthDate, 'Phone': phone, 'Proxy': ":".join(proxy), 'Status': status}
        ]

        if not has_newline:
            f.write('\n')
    
        writer.writerows(rows)

def creationWebhook(email,password,firstName,lastName,phone,proxy,webhook):

    data = {
    "content": None,
    "embeds": [
        {
        "title": "Nike Account Generated",
        "color": None,
        "fields": [
            {
            "name": "Email",
            "value": email,
            "inline": True
            },
            {
            "name": "Password",
            "value": password,
            "inline": True
            },
            {
            "name": "Phone",
            "value": phone
            },
            {
            "name": "First Name",
            "value": firstName,
            "inline": True
            },
            {
            "name": "Last Name",
            "value": lastName,
            "inline": True
            },
            {
            "name": "Proxy",
            "value": ":".join(proxy)
            }
        ],
        "footer": {
            "text": "Powered by NoctoTools",
            "icon_url": "https://cdn.discordapp.com/attachments/1053467609879805952/1100850881018212362/Noctono4.png"
        },
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1053467609879805952/1102585147083214930/nike-logo-black-clothes-design-icon-abstract-football-illustration-with-white-background-free-vector.jpg"
        }
        }
    ],
    "attachments": []
    }
    requests.post(webhook, json=data)

def getSMS(idnum, smsActivateApiKey,main_count,email):
    
    sa = SMSActivateAPI(smsActivateApiKey)

    while True:
        status = sa.getStatus(id=idnum) # STATUS_WAIT_CODE 
        try: 
            status = (sa.activationStatus(status)) # {'status': 'STATUS_WAIT_CODE', 'message': 'Ожидание смс'} 
            messageid = str(status['status'])
            print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Waiting on SMS Activate Code'}{reset_color}")
            if messageid == 'STATUS_WAIT_CODE':
                time.sleep(4)
            else:
                sms_code = messageid.replace("STATUS_OK:", "")
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Received SMS Activate Code: '}{sms_code}{reset_color}")
                return sms_code

        except: 
            print(status['message']) # Error text  

def getWebdriver(proxy,main_count,email):

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Starting Chrome Instance..'}{reset_color}")

    use_proxy=True,
    user_agent=None

    PROXY_HOST = (proxy[0])
    PROXY_PORT = (proxy[1])
    PROXY_USER = (proxy[2])
    PROXY_PASS = (proxy[3])

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    path = os.path.dirname(os.path.abspath(__file__))
    options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = PATH_PROXYEXTENSION

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)
    if user_agent:
        options.add_argument('--user-agent=%s' % user_agent)

    prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.managed_default_content_settings.images": 1}
    
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--no-sandbox')
    options.add_argument("window-size=65,1000")
    options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-blink-features')
    options.add_argument("disable-infobars")
    options.add_argument("test-type")
    options.add_argument("--no-zygote")
    options.add_argument("--no-first-run")
    options.add_argument('--disable-features=IsolateOrigins,site-per-process,OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints')
    options.add_argument('--flag-switches-begin')
    options.add_argument('--flag-switches-end')
    options.add_argument('--remote-debugging-port=0')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(options=options, executable_path=PATH_CHROME_DRIVER)
    
    return driver

def nikeGenerateAccount(region,email,password,firstName,lastName,birthDate,phone,proxy,smsActivateApiKey,main_count):

    driver = getWebdriver(proxy,main_count, email)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Loading Nike Website..'}{reset_color}")

    windows_before = driver.current_window_handle    
    driver.execute_script("window.open('https://accounts.nike.com/error')")
    time.sleep(5)
    driver.switch_to.window(windows_before)
    driver.get(f"https://www.nike.com/{region}/login")
    # start login/gen here
    time.sleep(2)

    act_chain = ActionChains(driver)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Adding Email'}{reset_color}")

    for i in range(5):
        try:
            driver.find_element(By.ID, 'username').click()
            break
        except:
            try:
                driver.find_element(By.XPATH, '//*[@id="username"]').click()
                break
            except:
                try:
                    driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/button').click()
                    break
                except:
                    None
        if i == 4:
            return "Failed Adding Email"
    
    for letter in email:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    try:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[3]').click()
    except:
        pass

    time.sleep(random.randint(110000, 190000)/100000)

    try:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[4]/button').click()
    except:
        act_chain.send_keys(Keys.ENTER).perform()
    
    time.sleep(random.randint(110000, 190000)/100000)
    time.sleep(random.randint(110000, 190000)/100000)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Adding Account Details'}{reset_color}")

    for i in range(5):
        try:
            driver.find_element(By.ID, 'firstName').click()
            break
        except:
            try:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Waiting 30 Seconds...'}{reset_color}")
                time.sleep(30)

                try:
                    driver.find_element(By.ID, 'username').click()
                except:
                    time.sleep(6)
                    try:
                        driver.find_element(By.ID, 'username').click()
                    except:
                        return "Failed Confirming Email"

                try:
                    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div/div[4]/button').click()
                    break
                except:
                    act_chain.send_keys(Keys.ENTER).perform()
                    break
            except:
                None
        if i == 4:
            return "Failed Adding Email"

    time.sleep(random.randint(110000, 190000)/100000)
    time.sleep(1)

    #FIRST NAME
    try:
        driver.find_element(By.ID, 'firstName').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-first-name-input"]').click()
        except:
            return "Failed Finding First Name"
        
    for letter in firstName:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    #LAST NAME
    try:
        driver.find_element(By.ID, 'lastName').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-last-name-input"]').click()
        except:
            return "Failed Finding Last Name"
        
    for letter in lastName:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    #PASSWORD
    try:
        driver.find_element(By.ID, 'password').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-password-input"]').click()
        except:
            return "Failed Finding Password"
        
    for letter in password:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    #SHOPPING PREFERENCE
    try:
        driver.find_element(By.ID, 'l7r-shopping-preference').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-shopping-preference"]').click()
        except:
            return "Failed Finding Shopping Preference"
        
    act_chain.send_keys(Keys.ARROW_DOWN).perform()
    act_chain.send_keys(Keys.ENTER).perform()

    birthDate = birthDate.replace("/", "")

    #BIRTHDATE
    try:
        driver.find_element(By.ID, 'l7r-date-of-birth-input').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-date-of-birth-input"]').click()
        except:
            return "Failed Finding BDate"
        
    for letter in birthDate:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    time.sleep(random.randint(110000, 190000)/100000)

    #CLICK
    try:
        driver.find_element(By.ID, 'privacyTerms').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="privacyTerms"]').click()
        except:
            return "Failed Finding Privacy Terms"
        
    time.sleep(random.randint(110000, 190000)/100000)

    emailcode = input("Email code: ")
    
    #EMAIL CODE
    try:
        driver.find_element(By.ID, 'l7r-code-input').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="l7r-code-input"]').click()
        except:
            return "Failed Finding Email Code"
        
    for letter in emailcode:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    time.sleep(random.randint(110000, 190000)/100000)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting Account Details'}{reset_color}")

    #CLICK SUBMIT
    try:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/form/div/div[10]/button').click()
    except:
        act_chain.send_keys(Keys.ENTER).perform()

    time.sleep(5)

    if 'https://www.nike.com/' in driver.current_url:
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Successfully Generated Nike Account'}{reset_color}")
    else:
        return "Failed Generating Account"

    if phoneVerificationResponse == False:
        return "Generated Account"

    driver.get("https://www.nike.com/gb/member/settings")   

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Adding Phone Number'}{reset_color}")

    for i in range(5):
        try:
            driver.find_element(By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[2]/div[2]/button').click()
            break
        except:
            time.sleep(random.randint(110000, 190000)/100000)
        if i == 4:
            return "Generated Account: Failed Finding Phone Button 1"

    for i in range(5):
        try:
            driver.find_element(By.XPATH, '//*[@id="settings"]/div[3]/div[1]/div[1]/div/div[2]/div/span').click()
            break
        except:
            try:
                driver.find_element(By.XPATH, '//*[@id="settings"]/div[3]/div[1]/div[1]').click()
                break
            except:
                time.sleep(random.randint(110000, 190000)/100000)
        if i == 4:
            return "Generated Account: Failed Finding Phone Button 2"
        
    time.sleep(random.randint(110000, 190000)/100000)

    for i in range(5):
        try:
            driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/section/div/div[2]/div/div[3]/div/form/div[2]/div[4]/div/div/div/div[2]/button').click()
            break
        except:
            try:
                driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/section/div/div[2]/div/div[3]/div/form/div[2]/div[4]/div/div/div/div[2]/button').click()
                break
            except:
                time.sleep(random.randint(110000, 190000)/100000)
        if i == 4:
            return "Generated Account: Failed Finding Phone Button 3"
    
    time.sleep(random.randint(110000, 190000)/100000)

    #PHONE NUMBER
    if phone == "SMSACTIVATE":
        sa = SMSActivateAPI(smsActivateApiKey)

        number = sa.getNumberV2(service='ew', country='16') 
        try: 
            # print(number['phoneNumber']) # 79999999999 
            idnum = (number['activationId'])
            phone = number['phoneNumber']
            sms_mode = 'SMSACTIVATE'
        except: 
            print("failed: " + number['message'])
            return "Failed Getting Phone"
        phone = phone[2:]
    else:
        sms_mode = "Manual"

    for i in range(5):
        try:
            driver.find_element(By.ID, 'phoneNumber').click()
            break
        except:
            try:
                driver.find_element(By.XPATH, '//*[@id="phoneNumber"]').click()
                break
            except:
                time.sleep(random.randint(110000, 190000)/100000)
        if i == 4:
            return "Generated Account: Failed Finding Phone Box"
        
    for letter in phone:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    time.sleep(random.randint(110000, 190000)/100000)

    #CLICK AGREE TERMS
    try:
        driver.find_element(By.ID, 'agreeToTerms').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="agreeToTerms"]').click()
        except:
            return "Generated Account: RETRY PHONE"

    time.sleep(random.randint(110000, 190000)/100000)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Requesting SMS Code'}{reset_color}")

    #CLICK SUBMIT PHONE
    try:
        driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/div/section/div/div[3]/form/div[4]/button').click()
    except:
        act_chain.send_keys(Keys.ENTER).perform()

    if sms_mode == "Manual":
        smscode = input(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'SMS Code: '}{reset_color}")
    elif sms_mode == "SMSACTIVATE":
        smscode = getSMS(idnum, smsActivateApiKey, main_count, email)

    #SMS CODE
    try:
        driver.find_element(By.ID, 'code').click()
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="code"]').click()
        except:
            return "Generated Account: RETRY PHONE"
        
    for letter in smscode:
        act_chain.send_keys(letter).perform()
        time.sleep(random.randint(20000, 110000)/100000)

    time.sleep(random.randint(110000, 190000)/100000)

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][{email}][{main_count}] {'Submitting SMS Code'}{reset_color}")

    #CLICK SUBMIT SMS CODE
    try:
        driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/div/section/div/div[3]/form/div[2]/button').click()
    except:
        act_chain.send_keys(Keys.ENTER).perform()

    return "Generated Account"



def verifyDetails(region,email,password,firstName,lastName,birthDate,phone,proxy,proxy_count):

    if region == '':
        region = 'gb'
    if email == '':
        return "Email Empty"
    if password == '':
        letters = string.ascii_letters
        digits = string.digits
        symbols = string.punctuation
        password = (''.join(random.choices(digits, k=5)) + ''.join(random.choices(letters, k=5)) + random.choice(symbols))
        password = ''.join(random.sample(password, len(password)))
    if firstName == '':
        firstName = names.get_first_name()
    if lastName == '':
        lastName = names.get_last_name()
    if birthDate == '':
        month = random.randint(1, 12)
        day = random.randint(1, 28) if month == 2 else random.randint(1, 30) if month in [4, 6, 9, 11] else random.randint(1, 31)
        year = random.randint(1900, 2022)
        birthDate = f"{month:02}/{day:02}/{year}"
    if phone == '':
        phone = 'SMSACTIVATE'
    if proxy == '':
        with open(PATH_PROXIES) as file:
            myproxies = file.readlines()
            x = myproxies[proxy_count].rstrip('\n')
            proxy = x.split(":")
    elif proxy != '':
        proxy = proxy.split(":")

    return region,email,password,firstName,lastName,birthDate,phone,proxy


def nikeDetails():

    global phoneVerificationResponse, retryLimit, smsActivateApiKey, webhook

    main_count = 0
    proxy_count = 0

    phoneVerification = input("Would you like the bot to sms verify the accounts? (y/n): ")
    if phoneVerification.lower() == "y":
        phoneVerificationResponse = True
    else:
        phoneVerificationResponse = False

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][][{main_count}] {'Loading CSV Details..'}{reset_color}")

    with open(PATH_NIKE_PROFILES, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        csvDetails = []
        for row in reader:
            csvDetails.append(row)

    smsActivateApiKey = jsonerrorlogs.jsonsmsactivatekey()
    webhook = jsonerrorlogs.jsonwebhook()
    retryLimit = jsonerrorlogs.jsonretrylimit()

    print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}][][{main_count}] {'Loaded Details.'}{reset_color}")

    for row in csvDetails:

        region = row[0]
        email = row[1]
        password = row[2]
        firstName = row[3]
        lastName = row[4]
        birthDate = row[5]
        phone = row[6]
        proxy = row[7]

        region,email,password,firstName,lastName,birthDate,phone,proxy = verifyDetails(region,email,password,firstName,lastName,birthDate,phone,proxy,proxy_count)

        for i in range(int(retryLimit)):
            status = nikeGenerateAccount(region,email,password,firstName,lastName,birthDate,phone,proxy,smsActivateApiKey,main_count)
            if "Generated Account" in status:
                creationWebhook(email,password,firstName,lastName,phone,proxy,webhook)
                break
            else:
               None

        writeDetails(region,email,password,firstName,lastName,birthDate,phone,proxy,status)

        proxy_count+=1
        main_count+=1







