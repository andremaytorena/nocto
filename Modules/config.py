
def details():
    global EMAIL, DEVICE_ID, PASSWORD, REV_TOKEN, COPY_ONLY, GEN_NUMBER, EMPLOYEE_EMAIL, CARD_PREFIX, START_WITH_INDEX, SMS_VERIFICATION, CURRENT_USER, BASE_URL
    EMAIL = input("Email: " ) #Login Email Address
    PASSWORD = input("Password: " ) # Login Password

    REV_TOKEN =  ""  #COOKIES (Token)
    DEVICE_ID = "" #x-device-id, all requests - No need to supply if email/password are filled
    print("")
    print("1. Gen Cards")
    print("2. Copy Cards")
    print("")
    typee = int(input("option"))
    if typee == 1:
        COPY_ONLY = False #Copy only, gen
    elif typee == 2:
        COPY_ONLY = True

    GEN_NUMBER = int(input("How many cards: ")) #HOW MANY CARDS TO GEN
    EMPLOYEE_EMAIL = EMAIL #WHICH TEAM MEMBER TO USE
    CARD_PREFIX = "CARD_" #USED TO LABEL GENERATED CARDS
    START_WITH_INDEX = 0 #INDEX WITH YOU WANT TO START CREATING YOUR CARD EX. (44) {CARD_PREFIX}_44, {CARD_PREFIX}_45...
    SMS_VERIFICATION = True #USE True if you want to confirm sms code and store card information in "cards.csv"



    ##########################


    BASE_URL = "https://business.revolut.com/api/"
    CURRENT_USER = BASE_URL + "user/current"