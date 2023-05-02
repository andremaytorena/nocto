from colorama import Fore
import os, requests, json, sys, urllib, shutil, time
import RaffleModules.footpatrolentry as footpatrolentry
import RaffleModules.footpatrolaccgen as footpatrolaccgen
import RaffleModules.sizeentry as sizeentry
import RaffleModules.sizeaccgen as sizeaccgen
import RaffleModules.sizewinchecker as sizewinchecker
import RaffleModules.footpatrolwinchecker as footpatrolwinchecker
import RaffleModules.settingsfile as settingsfilepy
import RaffleModules.shopify as shopify
import Paths.paths as paths
import RaffleModules.flatspot as flatspot
import RaffleModules.afew as afew
import noctotools as noctotools
from os import path
from Paths.paths import PATH_SETTINGS
from pypresence import Presence
from Loader.osSelector import clearScreen


def restartprogram(username, license_key):
    print(f'{Fore.WHITE} ')
    print('Choose: ')
    print('1. Go Back to Main Menu')
    print('2. Close Program')
    restart = (input("Option: "))
    if restart == '1':
        clearScreen()
        NoctoRaffles(username, license_key)
    else:
        print(' ')


def NoctoRaffles(username, license_key):

    # discord_rpc()
    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color
    username = f"{Fore.MAGENTA}{username}"

    clearScreen()    
    print("              _   __           __        ____        __________         ")
    print("             / | / /___  _____/ /_____  / __ \____ _/ __/ __/ /__  _____")
    print("            /  |/ / __ \/ ___/ __/ __ \/ /_/ / __ `/ /_/ /_/ / _ \/ ___/")
    print("           / /|  / /_/ / /__/ /_/ /_/ / _, _/ /_/ / __/ __/ /  __(__  ) ")
    print("          /_/ |_/\____/\___/\__/\____/_/ |_|\__,_/_/ /_/ /_/\___/____/  ")
                                                                                                 
    print("")
    print("")
    print(f"                              Welcome Back",  username)
    print("")
    print("")
    print(f"{reset_color}                               0. Settings File              ")
    print("")
    print(f"{OKBLUE}         --- Raffle Sites ---                      --- Mixed Sites ---         {reset_color}")
    print("")
    print("         1. Size? Launches                           5. Shopify")
    print("         2. Footpatrol Launches                      6. Flatspot")
    print("         3. Hipstore Launches                        7. Route One")
    print("         4. Footasylum Launches                      8. JDX ")
    print("                                                     9. Afew")
    print("")
    print(f"{OKBLUE}                           To open NoctoTools type:{Fore.MAGENTA} A1{reset_color}")
    print("")

    option = (input('        Option: '))

    if option == "0":
        settingsfilepy.main()
        NoctoRaffles(username, license_key)

    elif option == "1":
        clearScreen()
        print(" 1. Raffle Entry")
        print(" 2. Account Gen")
        print(" 3. Winchecker")
        print("")
        print(" 4. Back")
        print("")
        size_option = (input(" Option: "))
        if size_option == "1":
            sizeentry.CheckEntryStatus()
        elif size_option == "2":
            sizeaccgen.start()
        elif size_option == "3":
            sizewinchecker.start()
        elif size_option == "4":
            NoctoRaffles(username, license_key)
        else:
            NoctoRaffles(username, license_key)
        restartprogram(username, license_key)

    elif option == "2":
        clearScreen()   
        print(" 1. Raffle Entry")
        print(" 2. Account Gen")
        print(" 3. Winchecker")
        print("")
        print(" 4. Back")
        print("")
        footpatrol_option = (input(" Option: "))
        if footpatrol_option == "1":
            footpatrolentry.CheckEntryStatus()
        elif footpatrol_option == "2":
            footpatrolaccgen.start()
        elif footpatrol_option == "3":
            footpatrolwinchecker.start()
        elif footpatrol_option == "4":
            NoctoRaffles(username, license_key)
        else:
            NoctoRaffles(username, license_key)
        restartprogram(username, license_key)

    elif option == "3":
        print("hipstore") 

    elif option == "5":
        shopify.CheckEntryStatus()
        NoctoRaffles(username, license_key)

    elif option == "6":
        flatspot.CheckEntryStatus()
        NoctoRaffles(username, license_key)

    elif option == "9":
        afew.CheckEntryStatus()
        NoctoRaffles(username, license_key)

    elif option == "A1" or option == "a1":
        noctotools.NoctoTools(username, license_key)

    else:
        NoctoRaffles(username, license_key)

