import re
import csv
import pandas as pd
import time
import re, os
from colorama import Fore
from Paths.paths import PATH_PROFILECHECKER_PREFETCHED, PATH_PROFILECHECKER_PROFILES, PATH_PROFILECHECKER_NEW

def CheckEntryStatus(mode): # Opens accounts csv and gets account

    profiles_accounts = pd.read_csv(PATH_PROFILECHECKER_PROFILES)
    profilesaccounts = int((len(profiles_accounts)))

    prefetch_entered = pd.read_csv(PATH_PROFILECHECKER_PREFETCHED)
    prefetchsentered = int((len(prefetch_entered)))


    with open(PATH_PROFILECHECKER_PROFILES, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    with open(PATH_PROFILECHECKER_PREFETCHED, newline='') as p:
        reader = csv.reader(p)
        data_prefetch = list(reader)
        
    tn = 1
    string = ''
    
    print('Loading csv...')
    for i in range(prefetchsentered):
        string = string + data_prefetch[tn][0]
        tn = tn + 1
    
    print('Csv loaded...')
    print('Checking for similarities...')

    count = 1
    
    main = []
    for i in range(profilesaccounts):

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        

        l1 = []
        email = (data[count][0])
        password = (data[count][1])

        x = re.findall(email, str(string))

        if mode == 1:
            if not x:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Profile Checker: Email not duplicate: '}{email} {reset_color}")
            else:
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Profile Checker: Successfully Found Duplicate: '}{email} {reset_color}")
                l1.append(email)
                l1.append(password)
                main.append(l1)

        elif mode == 2:
            if not x:
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Profile Checker: Successfully Found None Duplicate: '}{email} {reset_color}")
                l1.append(email)
                l1.append(password)
                main.append(l1)
            else:
                print(f"{reset_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Profile Checker: Email duplicated: '}{email} {reset_color}")

    
        count = count + 1

    header = ['Email', 'Password']
    with open(PATH_PROFILECHECKER_NEW, 'w', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerows(main)


def start():
    print('1. Export the Duplicates')
    print('2. Export Accounts only in profiles.csv')
    print('')
    mode = int(input('Option: '))

    CheckEntryStatus(mode)

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(PATH_PROFILECHECKER_NEW)
    else:
        None
 




    




