import time


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
colors = Colors()

def log(message: str):
    color = colors.HEADER
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {message}")

def log_error(message: str):
    color = colors.FAIL
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {message}")

def log_success(message: str):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {message}") 

def name_log_success(first_name, last_name, full_name):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{first_name}{' | '}{last_name}{' | '}{full_name}")

def password_log_success(password):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{password}")

def phonenumber_log_success(phone):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{phone}")

def catchallnumber_log_success(catchall_email):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{catchall_email}")

def bday_log_success(bday):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{bday}")

def postcode_log_success(postcode):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{postcode}")

def sizes_log_success(final):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'Generated pair: '}{final}")

def sizewinchecker(email, number):
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'|'} {number} {'|'} {email} {'|'}")

def CSVsplitter():
    color = colors.OKGREEN
    end = colors.ENDC
    print(f"{color}[{time.strftime('%H:%M:%S', time.localtime())}]{end} {'CSV Split: '}{'Successfully'}")