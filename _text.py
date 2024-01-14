pgflig = None

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
WHITE = "\033[0m"

def setPrintingColor(color:str):
    print(color, end="")

def printBanner(text:str):
    print(pgflig(text))