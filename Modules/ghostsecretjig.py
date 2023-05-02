import random
import csv
import time, os, sys
from os import path
from Paths.paths import PATH_ADDRESSJIGGER_ADDRESSES, PATH_ADDRESSJIGGER_FOLDER

green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def createCSV():

    currenttime = str(time.time())

    currenttime = currenttime + '.csv'

    global NEW_PATH
    NEW_PATH = path.join(PATH_ADDRESSJIGGER_FOLDER, currenttime)

    global fieldnames
    
    with open(NEW_PATH, 'w', newline='') as file:
        fieldnames = ['Address Line 1', 'Address Line 2']

        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='')
        writer.writeheader()

    

def writetocsv(modified_addy_num):

    with open(NEW_PATH) as f:
            for line in f:
                pass
            has_newline = line.endswith('\n') or line.endswith('\n\r')

    with open(NEW_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='')
        rows = [
            {'Address Line 1': modified_addy_num, 'Address Line 2': ''}
        ]

        if not has_newline:
            f.write('\n')
    
        writer.writerows(rows)



def jig(addressline):
    
    count = 0
    count_1 = 0
    count_letter = 0
    

    print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {reset_color}{'Ghost Secret J1g: '}{addressline}")
    for i in range(2):



        verbs = ['NUM', 'Numbr', 'House Num']
        verbs_2 = ['', 'no']
        random_letter = ['a', 'a']

        

        address = str(addressline)



        house_number = ""
        for i in address:
            if i.isdigit():
                house_number = house_number + i

        # print(house_number)

        house_address_no_num = address.strip(house_number)



        word_list = house_address_no_num.split()
        number_of_words = len(word_list)

        if number_of_words == 1:
            print('1 word')


        elif number_of_words == 2:
            print("NOW")
        
        elif number_of_words == 3:
            print("Address Format Invalid, only use addresses that look like this: 64 Maida Vale")
            input("Press Enter to Exit..")
            sys.exit()

        full_word_string = ""

        for i in range(number_of_words):

            second_word = house_address_no_num.split(" ")[2]
            length_second_word = (len(second_word))
            length_second_word = length_second_word / 2
            length_second_word = (round(length_second_word))

            full_second_word_length = (len(second_word))
            
            if count_letter == 0:

                length_second_word = (len(second_word))
                length_second_word = length_second_word


                random_length_num = random.randint(2,length_second_word-1)
                random_letter_first = second_word[random_length_num]
                first_half = second_word[:random_length_num]
                second_half = second_word[random_length_num:]
                
                new_last_word = first_half  + random_letter_first + second_half
                new_last_word = random_letter[count_letter] + '.' + new_last_word                

                first_word = house_address_no_num.split(" ")[1]
                first_word_length = (len(first_word))

                random_length_num = random.randint(2,first_word_length-1)
                random_letter_first = first_word[random_length_num]
                first_half = first_word[:random_length_num]
                second_half = first_word[random_length_num:]
                

                new_first_word = first_half + '.' + random_letter_first + second_half

                final_first_word = new_first_word[:1] + '.' + new_first_word

                

                modified_addy_num = verbs[count] + '' + verbs_2[count_1] + '.' + house_number + ' ' +  final_first_word + ' '+ new_last_word
                

            elif count_letter == 1:
                new_last_word = second_word[:length_second_word] + str(random.randint(1,5)) + second_word[length_second_word:]
                final_last_word = new_last_word[:full_second_word_length] + '.' + new_last_word[full_second_word_length:]
        

                first_word = house_address_no_num.split(" ")[1]
                first_word_length = (len(first_word))

                random_length_num = random.randint(2,first_word_length-1)
                random_letter_first = first_word[random_length_num]
                first_half = first_word[:random_length_num]
                second_half = first_word[random_length_num:]
                

                new_first_word = first_half + random_letter_first + second_half

                random_length_num1 = random.randint(2,first_word_length-1)
                first_half = new_first_word[:random_length_num]
                second_half = new_first_word[random_length_num:]

                new = first_half + str(random_length_num1) + second_half

                modified_addy_num = verbs[count] + ' 0' + house_number + ' ' +  new + ' '+ final_last_word

            
                

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red
        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count+1}] {reset_color}{'Nike J1g: '}{modified_addy_num}")


        writetocsv(modified_addy_num)


        count_letter = count_letter + 1
        count = count + 1
        count_1 = count_1 + 1


def start_address(strength, addy1, amount):

    
    for i in range(int(amount)):

        addresslist = []
        if strength == 'light':
                addyLine1 =  addy1
                beginningChars = ""
                for i in range(random.randint(2,3)):
                    beginningChars += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                addyLine1 = beginningChars + " " + addyLine1

        elif strength == 'medium':
            addyLine1 =  addy1

            # Add 1-3 random characters to the beginning of the addyLine1
            beginningChars = ""
            for i in range(random.randint(2,3)):
                beginningChars += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            addyLine1 = beginningChars + " " + addyLine1

            # Add 1-2 random characters to the end of the addyLine1
            endChars = ""
            for i in range(random.randint(1, 2)):
                endChars += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            addyLine1 = addyLine1 + " " + endChars

        elif strength == 'tough':
            addyLine1 =  addy1
            # Add a dot to the addyLine1 at a random position
            if random.random() < 0.83:
                dotPos = random.randint(1, len(addyLine1)-1)
                addyLine1 = addyLine1[:dotPos] + "." + addyLine1[dotPos:]

            
            # Add 1-3 random characters to the beginning of the addyLine1
            beginningChars = ""
            for i in range(random.randint(1,3)):
                beginningChars += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            addyLine1 = beginningChars + " " + addyLine1


            # Add 1-2 random characters to the end of the addyLine1
            endChars = ""
            for i in range(random.randint(1, 2)):
                endChars += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            addyLine1 = addyLine1 + " " + endChars

            # Duplicate the last letter of the addyLine1
            if random.random() < 0.5:
                lastLetter = addyLine1[addyLine1.rindex(" ")+1:]
                addyLine1 += lastLetter

        green_color = '\033[92m' #light green
        reset_color = '\033[0m' #reset color
        red_color = '\033[91m' #red

        writetocsv(addyLine1)

        print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{0}] {reset_color}{'Ghost Secret J1g: '}{addyLine1}")


def magic(amount, initial_address, address_line_2):

        list_random_fronts = ['NUM', 'Numbr', 'House Num', 'Residence', 'Home', 'NO', 'Numb', 'Home Number', 'Numero']
        list_random_numberfronts = ['', 'no', '00', '0', '.', ',']


        #step 1: split the number from 
        house_number = ""
        for i in initial_address:
            if i.isdigit():
                house_number = house_number + i

        #step 2: split the address from house number
        address_no_number = initial_address.strip(house_number)

        #step 3: check how many words in this address
        splitted_address_no_number = address_no_number.split()
        amount_words_address_no_number = len(splitted_address_no_number)


        #step 4: run a loop to j1g each word
        for i in range(amount):
            count = 0
            main_word = ''
            random_int = random.randint(0,8)
            random_numberfront = random.randint(0,5)
            random_numberback = random.randint(0,21)
            for i in range(int(amount_words_address_no_number)):
                address_word = splitted_address_no_number[count]
                
                #step 5: check amount of letters in word

                amount_letter_address_word = len(address_word)

                #step 6: get random numbers to replace letters
                random_one = random.randint(0, int(amount_letter_address_word))
                random_two = random.randint(0, int(amount_letter_address_word)+1)
                random_three = random.randint(0, int(amount_letter_address_word)+2)
                random_four = random.randint(0, int(amount_letter_address_word)+3)

                random_number = random.randint(0,4)
                random_letter = random.randint(0,14)

                #step 7: set random numbers and letters
                list_numbers = ['1', '2', '3', '4', '5']
                list_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'x', 'z', 'y']

                #step 8: first change
                change_one_word = address_word[:random_one] + list_numbers[random_number] + address_word[random_one:]
                
                #step 9: second change
                change_two_word = change_one_word[:random_two] + list_letters[random_letter] + change_one_word[random_two:]

                #step 10: third change
                change_three_word = change_two_word[:random_three] + '.' + change_two_word[random_three:]

                #step 11: fourth change

                #step 11: get an address line 2

                main_word = main_word + change_three_word + ' '

                count+=1
            

            address_line_one = list_random_fronts[random_int] + ' ' + list_random_numberfronts[random_numberfront] + house_number + ' ' + main_word 
            
            writetocsv(address_line_one)
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {reset_color}{'Nike J1g: '}{address_line_one}")

def start():

    print('Select type: ')
    print("")
    print("1. Nike Address J1g")
    print("2. Strength J1g")
    print("3. Nike Address J1g v2")
    print("")
    option = input("Option: ")

    createCSV()

    if option == '1':
        print("Info: Make sure to have the addresses saved in the addresses.csv inside the AddressJigger folder!")

        with open(PATH_ADDRESSJIGGER_ADDRESSES) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                addressline = row[0]
                writetocsv(addressline)
                jig(addressline)

    elif option == '2':
        print("Info: Make sure to have the addresses saved in the addresses.csv inside the AddressJigger folder!")
        print("")
        print("Select strength: ")
        print("")
        print("1. Light")
        print("2. Medium")
        print("3. Tough")
        print("")
        option = input("Option: ")

        amount = int(input("Amount: "))

        if option == '1':
            strength = 'light'
        elif option == '2':
            strength = 'medium'
        elif option == '3':
            strength = 'tough'

        with open(PATH_ADDRESSJIGGER_ADDRESSES) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                addressline = row[0]
                writetocsv(addressline)
                start_address(strength, addressline, amount)

    elif option == '3':
        print("Info: Make sure to have the addresses saved in the addresses.csv inside the AddressJigger folder!")
        print("")
        sentence = input("Address line 1: ")
        sentence_two = input("Address Line 2: ")
        amount = int(input("Amount: "))

        with open(PATH_ADDRESSJIGGER_ADDRESSES) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                addressline = row[0]
                magic(amount, sentence, sentence_two)

        print("Successfully J1gged Address")
        print("Check your AddressJigger folder for the csv..")
        
    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(NEW_PATH)
    else:
        None

