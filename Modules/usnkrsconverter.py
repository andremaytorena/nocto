import csv, os
import pandas as pd
from Paths.paths import PATH_SNKRSEMAIL_PASSWORD_FOLDER, PATH_SNKRS_1, PATH_SNKRS_2, PATH_SNKRS_3, PATH_SNKRS_TO_TSB
from os import path
from colorama import Fore
import time
def join_details(option):

    if option == 1:
        count = 1 

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red

        with open(PATH_SNKRS_1) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                email = row[0]
                password = row[1]

                detail = email + '|' + password

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv')) as f:
                    for line in f:
                        pass
                    has_newline = line.endswith('\n') or line.endswith('\n\r')

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv'), 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
                    rows = [
                        {'Account':detail}
                    ]

                    if not has_newline:
                        f.write('\n')
                
                    writer.writerows(rows)

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'uSNKRS Converter: Successfully Converted Profile'} {reset_color}")
                count = count + 1

    elif option == 2:
        count = 1

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red

        with open(PATH_SNKRS_2) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                email = row[0]
                profile = row[1]
                size = row[2]
                proxy = row[3]

                detail = email + '|' + profile  + '|' + size  + '|' + proxy

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv')) as f:
                    for line in f:
                        pass
                    has_newline = line.endswith('\n') or line.endswith('\n\r')

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv'), 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
                    rows = [
                        {'Account':detail}
                    ]

                    if not has_newline:
                        f.write('\n')
                
                    writer.writerows(rows)

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'uSNKRS Converter: Successfully Converted Profile'} {reset_color}")
                count = count + 1

    elif option == 3:
        count = 1

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        
        with open(PATH_SNKRS_3) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                firstname = row[0]
                middlename = row[1]
                lastname = row[2]
                addy1 = row[3]
                addy2 = row[4]
                city = row[5]
                country = row[6]
                zip = row[7]
                state = row[8]
                phone = row[9]
                cc = row[10]
                month = row[11]
                year = row[12]
                cvv = row[13]
                profile_name = row[14]


                detail = firstname + '|' + middlename  + '|' + lastname  + '|' + addy1 + '|' + addy2 + '|' + city + '|' + country + '|' + zip + '|' + state + '|' + phone + '|' + cc + '|' + month + '|' + year + '|' + cvv + '|' + profile_name 
                
                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv')) as f:
                    for line in f:
                        pass
                    has_newline = line.endswith('\n') or line.endswith('\n\r')

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv'), 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
                    rows = [
                        {'Account':detail}
                    ]

                    if not has_newline:
                        f.write('\n')
                
                    writer.writerows(rows)

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'uSNKRS Converter: Successfully Converted Profile'} {reset_color}")
                count = count + 1

    elif option == 4:
        
        createCSV_TSB()

        count = 1

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        
        with open(PATH_SNKRS_TO_TSB) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                
                profile = str(row[0]).split("|")

                firstname = profile[0]
                middlename = profile[1]
                lastname = profile[2]
                addy1 = profile[3]
                addy2 = profile[4]
                city = profile[5]
                country = profile[6]
                zip = profile[7]
                state = profile[8]
                phone = profile[9]
                cc = profile[10]
                month = profile[11]
                year = profile[12]
                cvv = profile[13]
                profile_name = profile[14]

                expiry = month + '/' + year
                
                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'tsb_profile.csv')) as f:
                    for line in f:
                        pass
                    has_newline = line.endswith('\n') or line.endswith('\n\r')

                with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'tsb_profile.csv'), 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
                    rows = [
                        {'id':'detail', 'date':'', 'cc.profileName': profile_name, 'cc.email': profile_name, 'cc.phone': phone, 'cc.simpleId':'', 'cc.ccNumber':cc, 'cc.ccExpiry': expiry, 'cc.ccCvc':cvv, 'shipping.firstName':firstname, 'shipping.lastName':lastname,'shipping.middleName':middlename,'shipping.altFirstName':firstname,'shipping.altLastName':lastname,'shipping.address':addy1,'shipping.address2':addy2,'shipping.address3':'','shipping.zone':'','shipping.country':country,'shipping.city':city,'shipping.zip':zip,'shipping.state':state,'billing.billingSameAsShipping':'','isRussianAddress':'','isMexicanAddress':'','isJapaneseAddress':'','isPhilippinesAddress':'','isTemplate':''}
                    ]

                    if not has_newline:
                        f.write('\n')
                
                    writer.writerows(rows)

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Profile Converter: Successfully Converted Profile'} {reset_color}")
                count = count + 1


def createCSV():

    global fieldnames
    
    with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv'), 'w', newline='') as file:
        fieldnames = ['Account']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()

def createCSV_TSB():

    global fieldnames
    
    with open(path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'tsb_profile.csv'), 'w', newline='') as file:
        fieldnames = ['id','date','cc.profileName','cc.email','cc.phone','cc.simpleId','cc.ccNumber','cc.ccExpiry','cc.ccCvc','shipping.firstName','shipping.lastName','shipping.middleName','shipping.altFirstName','shipping.altLastName','shipping.address','shipping.address2','shipping.address3','shipping.zone','shipping.barangay','shipping.country','shipping.city','shipping.zip','shipping.state','billing.billingSameAsShipping','isRussianAddress','isMexicanAddress','isJapaneseAddress','isPhilippinesAddress','isTemplate']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()


def start():

    PATH_COMBINED = path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'combinedaccounts.csv')

    print('1. EMAIL|PASSWORD')
    print('2. EMAIL|PROFILE|SIZE|PROXY')
    print('3. FIRST NAME|MIDDLE NAME|LAST NAME|ADDRESS LINE 1|ADDRESS LINE 2|CITY|COUNTRY|ZIP|STATE|PHONE NUMBER|CC NUMBER|EXPIRY MONTH|EXPIRY YEAR|CVV|PROFILE NAME')
    print('4. Usnkrs to TSB')
    print('')
    print("5. Back")
    print('')

    option = int(input('Option: '))

    if option == 4:
        PATH_COMBINED = path.join(PATH_SNKRSEMAIL_PASSWORD_FOLDER, 'tsb_profile.csv')

    if option == 5:
        return "BACK"

    createCSV()
    
    join_details(option)

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(PATH_COMBINED)
    else:
        None