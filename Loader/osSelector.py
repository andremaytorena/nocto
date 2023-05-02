import platform, os

def clearScreen():

    operatingSystem = platform.system()

    if operatingSystem == "Windows":
        os.system("cls")
    elif operatingSystem == "Darwin":
        os.system("clear")




