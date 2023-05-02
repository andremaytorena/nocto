import Modules.addressjigger as addressjigger
import Modules.birthdategenerator as birthdategenerator
import Modules.catchallgenerator as catchallgenerator
import Modules.csvsplitter as csvsplitter
import Modules.courierbulktracker as courierbulktracker
import Modules.icloudgenerator as icloudgenerator
import Modules.namegenerator as namegenerator
import Modules.passwordgenerator as passwordgenerator
import Modules.phonegenerator as phonegenerator
import Modules.postcodegenerator as postcodegenerator
import Modules.sizerandomizer as sizerandomizer
import Modules.stripecardgenerator as stripecardgenerator
import Modules.usnkrsconverter as usnkrsconverter
import Modules.freesim as freesim
import Modules.gmailgen as gmailgen
import Modules.ghostsecretjig as ghostsecretjig
import Modules.revbusinesscardgen as revbusiness
import Modules.prodirect as prodirect
import Modules.niketracker as niketracker
import Modules.meshordertracker as meshordertracker
import Modules.footshopstockscraper as footshop
import Modules.revolutbusinesssolver as revbusinesssolver
import Modules.revolutpersonalsolver as revpersonalsolver
import Modules.meshstockscraper as meshstockscraper
import Modules.endstockscraper as endstockscraper
import Modules.testsolver as solver
import noctoraffles as noctoraffles
import Modules.platform_comparator as platform_comparator
import Modules.nikeaccgen as nikeaccgen
from Loader.osSelector import clearScreen
import sys, os
from colorama import Fore


def restartprogram(username, license_key):
    print(f'{Fore.WHITE} ')
    print('Choose: ')
    print('1. Restart the Program')
    print('2. Close Program')
    restart = (input("Option: "))
    if restart == '1':
        clearScreen()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        NoctoTools(username, license_key)

def NoctoTools(username, license_key):
    
    # from Paths import paths 
    username = f"{Fore.MAGENTA}{username}"
    # discord_rpc()
    clearScreen()                                                                                                            
    OKBLUE = '\033[94m'
    reset_color = '\033[0m' #reset color

    print("                                           _   __           __        ______            __     ") 
    print("                                          / | / /___  _____/ /_____  /_  __/___  ____  / /____ ")
    print("                                         /  |/ / __ \/ ___/ __/ __ \  / / / __ \/ __ \/ / ___/ ")
    print("                                        / /|  / /_/ / /__/ /_/ /_/ / / / / /_/ / /_/ / (__  )  ")
    print("                                       /_/ |_/\____/\___/\__/\____/ /_/  \____/\____/_/____/   ")
    print("")
    print("")
    print(f"                                                       Welcome Back",  username)

    print("")
    print(f"{OKBLUE}               --- Credential Generators ---            --- Revolut Solvers ---              --- Random Things ---   {reset_color}")
    print("")
    print("                  00. Name Generator                   11. Rev Personal Solver               19. Platform Comparator")
    print("                  01. Catchall Generator               12. Rev Business Solver               20. END Stock Scraper")
    print("                  02. Password Generator                                                     21. FS Stock Scraper")
    print(f"                  03. Phone Generator                  {OKBLUE}--- Card Generators ---{reset_color} ")
    print(f"                  04. Birthdate Generator                                                   {OKBLUE}   --- Addresses --- {reset_color}")
    print("                  05. Postcode Generator                13. Stripe Card Gen")
    print("                                                        14. Revolut Card Gen                  22. Address J1gger")
    print(f"{OKBLUE}                 --- Random Generators ---   {reset_color}                                                 23. Nike J1gger")
    print(f"                                                       {OKBLUE}--- Email Generators ---{reset_color}")
    print(f"                  06. Free Sim Cards Gen                                                     {OKBLUE}--- Order Trackers ---{reset_color}")
    print("                  07. PDs Account Gen                   15. Gmail Generator")
    print("                  08. uSNKRS Converter                  16. iCloud Generator                  24. Nike Tracker")
    print("                  09. CSV Splitter                      17. Outlook Generator                 25. Mesh Tracker")
    print("                  10. Size Randomizer                   18. Nike Generator                  26. Courier Tracker")
    print("")
    print(f"{OKBLUE}                                                    To open NoctoRaffles type: {Fore.MAGENTA}A1{reset_color}")
    print("")

    def handle_option_0():
        clearScreen()
        print('')
        result = namegenerator.start()
        if result == 'BACK':
            NoctoTools(username, license_key)
        else:
            restartprogram(username, license_key)

    options = {
        '00': handle_option_0,
        '01': catchallgenerator.catchall_main,
        '02': passwordgenerator.passwordgen_main,
        '03': phonegenerator.phonegen_main,
        '04': birthdategenerator.bdaygen_main,
        '05': postcodegenerator.postcode_start,
        '06': freesim.start,
        '07': prodirect.start,
        '08': usnkrsconverter.start,
        '09': csvsplitter.CSVsplit,
        '10': sizerandomizer.sizes_main,
        '11': revpersonalsolver.thread_sessions,
        '12': revbusinesssolver.get_session,
        '13': stripecardgenerator.start,
        '14': revbusiness.start,
        '15': gmailgen.CheckEntryStatus,
        '16': icloudgenerator.task_option,
        '17': lambda: print("COMING SOON..."),
        '18': nikeaccgen.nikeDetails,
        '19': platform_comparator.platform_main,
        '20': endstockscraper.start,
        '21': footshop.scrape_stock,
        '22': lambda: addressjigger.first() or NoctoTools(username, license_key),
        '23': ghostsecretjig.start,
        '24': niketracker.start,
        '25': meshordertracker.start,
        '26': lambda: courierbulktracker.start_main() or NoctoTools(username, license_key),
        '27': solver.thread_sessions,
        '0': handle_option_0,
        '1': catchallgenerator.catchall_main,
        '2': passwordgenerator.passwordgen_main,
        '3': phonegenerator.phonegen_main,
        '4': birthdategenerator.bdaygen_main,
        '5': postcodegenerator.postcode_start,
        '6': freesim.start,
        '7': prodirect.start,
        '8': usnkrsconverter.start,
        '9': csvsplitter.CSVsplit,
        'A1' : noctoraffles.NoctoRaffles,
        'a1' : noctoraffles.NoctoRaffles
    }
    print('')
    option = input("                Option: ")
    clearScreen()

    if option in options:
        if option == 'A1' or option == 'a1':# special handling for NoctoRaffles option
            options[option](username, license_key)  # call the function with arguments
        else:
            clearScreen()
            options[option]()  # call the function without arguments
            NoctoTools(username, license_key)
    else:
        NoctoTools(username, license_key)


