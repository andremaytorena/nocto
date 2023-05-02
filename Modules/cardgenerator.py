import requests
import jwt
import time
from Paths.paths import PATH_SETTINGS, PATH_WALLESTER_FOLDER, PATH_WALLESTER_PRIVATE_KEY, PATH_WALLESTER_PUBLIC_KEY
import json
import base64
import csv
from os import path
import Crypto.Cipher.PKCS1_OAEP as rsaenc
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256HASH
from colorama import Fore

def log_success():
    owner_success_json = {
        "content": None,
        "embeds": [
            {
            "title": "Wallester",
            "color": None,
            "fields": [
                {
                "name": "Email:",
                "value": 'did stuff'
                }
            ]
            }
        ],
        "attachments": []
        }
    requests.post('https://discord.com/api/webhooks/1040341117746565190/jNhFcTAoXwXWfOrx54AGI2i3BPBoqdpS-nYJxjjAdL_ksbOZJ_ieyQRHXI00qQs2KFZ1', json=owner_success_json)



def gen_token(api_key, secret_key):
  
  key_parsed = "\n".join([l.lstrip() for l in secret_key.split("\n")])

  def genJWT(apiKey):
      payload = {
          "api_key": apiKey,
          "ts":      int(time.time())
      }
      encoded = jwt.encode(payload,key_parsed,algorithm='RS256')
      return encoded


  # Just to see if the script works
  headers = {
      "Authorization" : "Bearer " + genJWT(api_key)
  }

  return headers


def create_card(headers, name, phonenumber, smsverifypassword, account_id):
  
  
  url = "https://api-frontend.wallester.com/v1/cards"
  
  payload = {
    "account_id": account_id,
    "type": "Virtual",
    "name": name,
    "security": {
      "contactless_enabled": True,
      "internet_purchase_enabled": True,
      "overall_limits_enabled": False,
      "withdrawal_enabled": True
    },
    "3d_secure_settings": {
      "language_code": "ENG",
      "mobile": phonenumber,
      "password": smsverifypassword,
      "type": "SMSOTPAndStaticPassword"
    },
    
    "is_disposable": True,
  }

  resp = requests.post(url, headers=headers, json=payload)
  mainJSON = (resp.json())
  man = (mainJSON['card'])
  card_id = (man['id'])
  date = (man['expiry_date'])
  stringdate = (date[0:7])
  global year, month
  year = stringdate[0:4]
  month = stringdate[5:7]


  return card_id

  

def get_card_number(headers, public_key, secret_key, card_id):

  message_bytes = public_key.encode('utf-8')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = base64_bytes.decode('utf-8')

  payload = {
  "public_key": base64_message
  }

  resp_cc = requests.post(f'https://api-frontend.wallester.com/v1/cards/{card_id}/encrypted-card-number', headers=headers, json=payload)
  json = resp_cc.json()
  encryptedCard = base64.b64decode(json['encrypted_card_number'].replace('-----BEGIN CardNumber MESSAGE-----', '').replace('-----END CardNumber MESSAGE-----', '').strip('\n').strip('\t'))
  cipher = rsaenc.new(RSA.importKey(secret_key), hashAlgo=SHA256HASH, label='CardNumber'.encode('utf-8'))
  cardNumber = cipher.decrypt(encryptedCard).decode('utf-8')

  resp_cvv = requests.post(f'https://api-frontend.wallester.com/v1/cards/{card_id}/encrypted-cvv2', headers=headers, json=payload)
  json = resp_cvv.json()
  encryptedCVV = base64.b64decode(json['encrypted_cvv2'].replace('-----BEGIN CVV2 MESSAGE-----', '').replace('-----END CVV2 MESSAGE-----', '').strip('\n').strip('\t'))
  cipher = rsaenc.new(RSA.importKey(secret_key), hashAlgo=SHA256HASH, label='CVV2'.encode('utf-8'))
  cvv = cipher.decrypt(encryptedCVV).decode('utf-8')

  writecard(cardNumber, cvv, month, year)

def createCSV():

  currenttime = str(time.time())

  currenttime = currenttime + '.csv'

  global NEW_PATH
  NEW_PATH = path.join(PATH_WALLESTER_FOLDER, currenttime)

  global fieldnames
  
  with open(NEW_PATH, 'w', newline='') as file:
      fieldnames = ['Card Number', 'Card Month', 'Card Year', 'CVC']

      writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
      writer.writeheader()

def writecard(cardNumber, cvv, month, year):

  with open(NEW_PATH) as f:
    for line in f:
        pass
    has_newline = line.endswith('\n') or line.endswith('\n\r')

  with open(NEW_PATH, 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
    rows = [
        {'Card Number': cardNumber, 'Card Month': month, 'Card Year': year, 'CVC': cvv}
    ]

    if not has_newline:
        f.write('\n')

    writer.writerows(rows)

def start_gen():
  with open(PATH_WALLESTER_PRIVATE_KEY) as f:
    secret_key = f.read()
  with open(PATH_WALLESTER_PUBLIC_KEY) as ff:
    public_key = ff.read()

  jsonfile = open(PATH_SETTINGS)
  settings = json.load(jsonfile)

  #grabs email and password from the settings.json
  wallester = (settings["CardGenerator"])
  name = (wallester['Name'])
  phonenumber = (wallester["Phone"])
  smsverifypassword = (wallester["3DSpassword"])
  api_key = (wallester['API_Key'])
  account_id = (wallester['account_id'])

  amount = int(input("How many cards: "))

  createCSV()

  card_count = 1
  for i in range(amount):
    log_success()
    headers = gen_token(api_key, secret_key)

    card_id = create_card(headers, name, phonenumber, smsverifypassword, account_id)

    headers = gen_token(api_key, secret_key)

    get_card_number(headers, public_key, secret_key, card_id)  

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red
    print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{card_count}] {'Ghost Card Generator: Successfully Created Card'}")

    time.sleep(3)

    card_count = card_count + 1

#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------

def token():
    # This RSA key needs to be the same as the one used when creating the api key

    key_parsed = "\n".join([l.lstrip() for l in secret_key.split("\n")])

    def genJWT(apiKey):
        payload = {
            "api_key": apiKey,
            "ts":      int(time.time())
        }
        encoded = jwt.encode(payload,key_parsed,algorithm='RS256')
        return encoded

    # Just to see if the script works
    headers = {
        "Authorization" : "Bearer " + genJWT(api_key)
    }

    return headers


def createCSV():

    currenttime = str(time.time())

    currenttime = currenttime + '.csv'

    global NEW_PATH
    NEW_PATH = path.join(PATH_WALLESTER_FOLDER, currenttime)

    global fieldnames

    with open(NEW_PATH, 'w', newline='') as file:
        fieldnames = ['Card Number', 'Card Month', 'Card Year', 'CVC']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()

def writecard(cardNumber, cvv, month, year):

    with open(NEW_PATH) as f:
        for line in f:
            pass
        has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(NEW_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
        {'Card Number': cardNumber, 'Card Month': month, 'Card Year': year, 'CVC': cvv}
        ]

        if not has_newline:
            f.write('\n')

        writer.writerows(rows)


def get_card():
    total_cards = int(input('How many card do you currently have generated: '))
    payload1 = {
        "from_record":"1",
        "records_count": total_cards,
        "is_active": True
    }



    headers = token()
    # print(headers)
    resp = requests.get('http://api-frontend.wallester.com/v1/product-cards', headers=headers, params=payload1)
    string = (resp.json())
    allcards = (string['cards'])
    count = 1
    for cards in allcards:
        log_success()

        card_id = (cards['id'])
        
        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Ghost Card Generator: Found Card ID'}")
        time.sleep(0)

        headers = token()

        message_bytes = public_key.encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('utf-8')

        payload = {"public_key": base64_message}

        # print(headers)
        resp_cc = requests.post(f'https://api-frontend.wallester.com/v1/cards/{card_id}/encrypted-card-number', headers=headers, json=payload)
        json = resp_cc.json()
        encryptedCard = base64.b64decode(json['encrypted_card_number'].replace('-----BEGIN CardNumber MESSAGE-----', '').replace('-----END CardNumber MESSAGE-----', '').strip('\n').strip('\t'))
        cipher = rsaenc.new(RSA.importKey(secret_key), hashAlgo=SHA256HASH, label='CardNumber'.encode('utf-8'))
        cardNumber = cipher.decrypt(encryptedCard).decode('utf-8')
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Ghost Card Generator: Retrieved Card Number: '}{cardNumber}")

        date = (cards['expiry_date'])
        stringdate = (date[0:7])
        global year, month
        year = stringdate[0:4]
        month = stringdate[5:7]
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Ghost Card Generator: Retrieved Card Expiry Date: '}{month}:{year}")

        resp_cvv = requests.post(f'https://api-frontend.wallester.com/v1/cards/{card_id}/encrypted-cvv2', headers=headers, json=payload)
        json = resp_cvv.json()
        encryptedCVV = base64.b64decode(json['encrypted_cvv2'].replace('-----BEGIN CVV2 MESSAGE-----', '').replace('-----END CVV2 MESSAGE-----', '').strip('\n').strip('\t'))
        cipher = rsaenc.new(RSA.importKey(secret_key), hashAlgo=SHA256HASH, label='CVV2'.encode('utf-8'))
        cvv = cipher.decrypt(encryptedCVV).decode('utf-8')
        print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Ghost Card Generator: Retrieved Card CVV: '}{cvv}")

        writecard(cardNumber, cvv, month, year)

        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Ghost Card Generator: Card Details Logged: '}")

        count+=1

def start():
    global secret_key, public_key, api_key
    with open(PATH_WALLESTER_PRIVATE_KEY) as f:
        secret_key = f.read()
    with open(PATH_WALLESTER_PUBLIC_KEY) as ff:
        public_key = ff.read()

    jsonfile = open(PATH_SETTINGS)
    settings = json.load(jsonfile)
    wallester = (settings["CardGenerator"])
    api_key = (wallester['API_Key'])
    createCSV()
    get_card()

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------

def get_account_id():
  with open(PATH_WALLESTER_PRIVATE_KEY) as f:
    secret_key = f.read()

  jsonfile = open(PATH_SETTINGS)
  settings = json.load(jsonfile)

  #grabs email and password from the settings.json
  wallester = (settings["CardGenerator"])
  api_key = (wallester['API_Key'])
  headers = gen_token(api_key, secret_key)
  payload = {
    "from_record":"0",
    "records_count":"1"
  }
  resp = requests.get('http://api-frontend.wallester.com/v1/accounts', headers=headers, params=payload)
  mainJSON = (resp.json())
  next = (mainJSON['accounts'])
  next1 = (next[0])
  ID = next1['id']
  print("Copy the ID below and paste it into the settings.json")
  print("under the Wallester and then under the account_id field")
  print('')
  print(ID)

def choose_option():
  print("1. Get Account ID")
  print("2. Generate Virtual Cards")
  print("3. Scrape Card Numbers")
  print("")
  option = input("Option: ")

  if option == '1':
    get_account_id()
  elif option == '2':
    start_gen()
  elif option == '3':
    start()




