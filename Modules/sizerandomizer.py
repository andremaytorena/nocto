import csv
import os
import random
import Modules.logger as logger
from Paths.paths import PATH_SIZE_RANDOMIZER_FOLDER
import time
from os import path
from Loader.osSelector import clearScreen

def sizes_main():

    print('Type of Size: ')
    print('')
    print('1. UK 10')
    print("2. 10")
    print('')
    option = (input("Option: "))
    print('')
    clearScreen()

    green_color = '\033[92m' #light green
    reset_color = '\033[0m' #reset color
    red_color = '\033[91m' #red

    if option == '1':

        fromsize = int(input("From size (do not put half sizes): "))
        tosize = int(input("To size (do not put half sizes): "))
        amount = int(input("How many sizes: "))

        sizes = [6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5]
        numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

        size = ([s for s in sizes if fromsize <= s <= tosize])
        test = len(size)
        test = test -1
        number = ([a for a in numbers if 1 <= a <= test])
            
        with open(path.join(PATH_SIZE_RANDOMIZER_FOLDER, "sizes.csv"), "w", newline='') as csvfile:
            fieldnames = ['Sizes']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count=1
            for i in range(amount):
                
                random_size = (random.choice(number))

                final = (size[random_size])

                finalist = 'UK ' + str(final)

                thewriter.writerow({'Sizes':finalist})

                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{finalist} {reset_color}")
                count+=1


    if option == '2':

        fromsize = int(input("From size: "))
        tosize = int(input("To size: "))
        amount = int(input("How many sizes: "))

        sizes = [6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5]
        numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

        size = ([s for s in sizes if fromsize <= s <= tosize])
        test = len(size)
        test = test -1
        number = ([a for a in numbers if 1 <= a <= test])
            
        with open(path.join(PATH_SIZE_RANDOMIZER_FOLDER, "sizes.csv"), "w", newline='') as csvfile:
            fieldnames = ['Sizes']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            count=1
            for i in range(amount):
                
                random_size = (random.choice(number))

                final = (size[random_size])

                thewriter.writerow({'Sizes':final}) 
                print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: '}{final} {reset_color}")

                count+=1

    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    print("")
    open_file_option = input(f"{OKBLUE}[{time.strftime('%H:%M:%S', time.localtime())}] [ ] {'Would you like to open the csv (y/n):'} {reset_color}")
    if open_file_option == 'y':
        os.startfile(path.join(PATH_SIZE_RANDOMIZER_FOLDER, "sizes.csv"))
    else:
        None
