from colorama import Fore, Style, init
init()

def success(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

def error(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def info(text):
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"


def greet(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"