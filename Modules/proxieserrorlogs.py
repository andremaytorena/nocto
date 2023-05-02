import os, time, sys
from Paths.paths import PATH_PROXIES

file_path = PATH_PROXIES
green_color = '\033[92m' #light green
reset_color = '\033[0m' #reset color
red_color = '\033[91m' #red

def checkproxies():

    if os.path.getsize(file_path) == 0:
        print(f"{red_color}[{time.strftime('%H:%M:%S', time.localtime())}] [] {'You need proxies to run this module, please add them in the proxies.txt file inside NoctoTools folder'} {reset_color}")
        input('Press enter to exit...')
        sys.exit()
    else:
        return