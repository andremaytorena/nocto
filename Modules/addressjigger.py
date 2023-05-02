import csv
import string, random
import Modules.logger as logger
from Paths.paths import PATH_ADDRESSJIGGER_ADDRESSES, PATH_ADDRESSJIGGER_RESULT 
from os import path
import time, os

def first():
    
    while True:
        print('Type of J1g: ')
        print('')
        print('1. XXX Address')
        print("2. XXX Address XXX")
        print("3. Address XXX")
        print("")
        print("4. Back")
        print('')

        try:
            option = int(input("Option: "))
            break
        except ValueError:
            print('Please only respond with a number from 1 to 3')

    if option == 4:
        return "BACK"

    print('')
    address_line_1 = input("Enter address line 1: ")
    address_line_2 = input("Enter address line 2: ")


    def xxx_infront():

        base = {
            "address1": address_line_1,
            "address2": address_line_2
        }


        addy1 = []
        addy2 = []

        addresses = [] # List of dicts

        def jig(amount: int):
            genned = 0
            while genned != amount:
                jig_length = 3
                jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))

                jigged1 = f"{jig} {base['address1']}"
                jigged2 = f"{jig} {base['address2']}"        

                while jigged1 in addy1:
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged1 = f"{jig} {base['address1']}"
                
                while jigged2 in addy2: 
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged2 = f"{jig} {base['address2']}"

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{genned+1}] {f'Generated pair: {jigged1} | {jigged2}'}")

                addresses.append({
                    "address1": jigged1, 
                    "address2": jigged2
                })
                addy1.append(jigged1)
                addy2.append(jigged2)
                genned += 1


        def main():
            logger.log("Loading csv...")
            load_csv()
            logger.log(f"Loaded {len(addy1)} address line 1 and {len(addy2)} address line 2!")
            amount = int(input("Amount: "))
            
            jig(amount)
            append_results()

        def load_csv():
            with open(PATH_ADDRESSJIGGER_ADDRESSES, newline='') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        for row in spamreader:
                            loaded = {
                                "address1": row[0],
                                "address2": row[1],
                            }

                            addy1.append(row[0])
                            if row[1] not in (None, ""):
                                addy2.append(row[1])

                            addresses.append(loaded)


        def append_results():
            with open(PATH_ADDRESSJIGGER_RESULT, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in addresses:
                    writer.writerow(
                        [item["address1"], item["address2"]])
                    
        main()


    def xxx_both():

        base = {
            "address1": address_line_1,
            "address2": address_line_2
        }


        addy1 = []
        addy2 = []

        addresses = [] # List of dicts

        def jig(amount: int):
            genned = 0
            while genned != amount:
                jig_length = 3
                jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))

                jigged1 = f"{jig} {base['address1']} {jig}"
                jigged2 = f"{jig} {base['address2']} {jig}"        

                while jigged1 in addy1:
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged1 = f"{jig} {base['address1']} {jig}"
                
                while jigged2 in addy2: 
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged2 = f"{jig} {base['address2']} {jig}"

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{genned+1}] {f'Generated pair: {jigged1} | {jigged2}'}")

                addresses.append({
                    "address1": jigged1, 
                    "address2": jigged2
                })
                addy1.append(jigged1)
                addy2.append(jigged2)
                genned += 1


        def main():
            logger.log("Loading csv...")
            load_csv()
            logger.log(f"Loaded {len(addy1)} address line 1 and {len(addy2)} address line 2!")
            amount = int(input("Amount: "))
            
            jig(amount)
            append_results()

        def load_csv():
            with open(PATH_ADDRESSJIGGER_ADDRESSES, newline='') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        for row in spamreader:
                            loaded = {
                                "address1": row[0],
                                "address2": row[1],
                            }

                            addy1.append(row[0])
                            if row[1] not in (None, ""):
                                addy2.append(row[1])

                            addresses.append(loaded)


        def append_results():
            with open(PATH_ADDRESSJIGGER_RESULT, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in addresses:
                    writer.writerow(
                        [item["address1"], item["address2"]])
                    
        main()

    def xxx_behind():

        base = {
            "address1": address_line_1,
            "address2": address_line_2
        }


        addy1 = []
        addy2 = []

        addresses = [] # List of dicts

        def jig(amount: int):
            genned = 0
            while genned != amount:
                jig_length = 3
                jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))

                jigged1 = f"{base['address1']} {jig}"
                jigged2 = f"{base['address2']} {jig}"        

                while jigged1 in addy1:
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged1 = f"{base['address1']} {jig}"
                
                while jigged2 in addy2: 
                    jig = ''.join(random.choice(string.ascii_uppercase) for _ in range(jig_length))
                    jigged2 = f"{base['address2']} {jig}"

                green_color = '\033[92m' #light green
                reset_color = '\033[0m' #reset color
                red_color = '\033[91m' #red
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{genned+1}] {f'Generated pair: {jigged1} | {jigged2}'}")

                addresses.append({
                    "address1": jigged1, 
                    "address2": jigged2
                })
                addy1.append(jigged1)
                addy2.append(jigged2)
                genned += 1


        def main():
            logger.log("Loading csv...")
            load_csv()
            logger.log(f"Loaded {len(addy1)} address line 1 and {len(addy2)} address line 2!")
            amount = int(input("Amount: "))
            
            jig(amount)
            append_results()

        def load_csv():
            with open(PATH_ADDRESSJIGGER_ADDRESSES, newline='') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        for row in spamreader:
                            loaded = {
                                "address1": row[0],
                                "address2": row[1],
                            }

                            addy1.append(row[0])
                            if row[1] not in (None, ""):
                                addy2.append(row[1])

                            addresses.append(loaded)


        def append_results():
            with open(PATH_ADDRESSJIGGER_RESULT, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in addresses:
                    writer.writerow(
                        [item["address1"], item["address2"]])
                    
        main()

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    
    if option == 1:
        xxx_infront()
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(PATH_ADDRESSJIGGER_RESULT)
        else:
            None

    elif option == 2:   
        xxx_both()
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(PATH_ADDRESSJIGGER_RESULT)
        else:
            None
    
    elif option == 3:
        xxx_behind()
        print("")
        open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
        if open_file_option == 'y':
            os.startfile(PATH_ADDRESSJIGGER_RESULT)
        else:
            None



