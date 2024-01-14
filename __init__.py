import json
from operator import itemgetter
import os
import time
import requests
from pyfiglet import figlet_format

import cutie
import _text
_text.pgflig = figlet_format


def welcomeSign() -> None:
    _text.setPrintingColor(_text.BLUE)
    _text.printBanner("Welcome to")
    _text.printBanner("SC Trade Router")
    print("Use arrow keys to select, and enter to confirm!")
    _text.setPrintingColor(_text.WHITE)

def askOptions() -> dict:
    return {
        "hiddenShopsAllowed":cutie.prompt_yes_or_no("Do u want me to include hidden locations?: "),
        "cargoCapacity":cutie.get_number("How much cargo capacity do u want to use?: ",min_value=0,allow_float=False),
        "onlyGreen":cutie.prompt_yes_or_no("Do u want me to only show green routes(same planet system routes, in most cases fastest)?: ")
    }

def downloadCom(com:str,file):
    url = f"https://sc-trade.tools/api/items/{com}/transactions?system=Stanton"

    payload = {}
    headers = {
        'token': '03AFcWeA5ySa6SZChDpAHoBrr-VNY2-Yk38il7TnaItlTeSImPnnelGyFPamD1mPh8rMlWzLzvm0F8F6Wqg_zGBgUn_MAttBnBb6dylsau9rqiXKuN0CuXGPXglr2WB1cPnrRz1EM2e1AVlLQibp_sJd14hIhcWmmh6L4g7jQtVbe7ypPSMGw7ecLEQpp-aiZYL_VWiUIlXgT8NuDBuVFnHbfd-waLskUOkgOKHayL9LC80OwcRBanvOK4q9Q_5IWzRfCbijbxJHjaAYg2-UlAUxqEID5qEa0zV2OT1Sw6Ebex_v2Eapw89CQ4CqbmPird7RhwiX2SjfNEr1nDV2kj7ErfQ01y3Y1LKDtkyo61wzGJDq65Ze-uj5mW26QHuCPhSQWLA2_lDlHDshKiEEFCFaiQeJfBw01AJgbh-oAmXVsG8voo7Wi5sgVnKoRmNZ-ADB2wm8oMUDKcu9b___kKbUmHPG0YnTXdO_MP_bSCTP85DKu-euEtBpuw59r0t7ugf2L000_aWgeBxMhNba9BVonocmqj79e8Q-QvHvz4CDe0tGkYryXAkDxctPpVo84z6Fk6UVpQr5eJeeRGEniduR6fGCS__6nFtT5bdLLkzGb1DJrVQZXXjTOjWxXlrF1D0ejntszLNn5l'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    open(file,"w+").write(json.dumps(response))

def downloadData() -> None:
    _text.setPrintingColor(_text.PURPLE)
    if not os.path.exists("data/download"):
        os.makedirs("data")
        os.makedirs("data/download")

    print("Downloading data may take a while...")
    url = "https://sc-trade.tools/api/items"

    payload = {}
    headers = {}

    coms = requests.request("GET", url, headers=headers, data=payload).json()

    for com in coms:
        downloadCom(com,f"data/download/{com.lower().replace(' ','_')}.json")
    
    print("Done downloading...")
    print()
    _text.setPrintingColor(_text.WHITE)

def showData(folder:str = "data"):

    if not os.path.exists("data/download"):
        _text.setPrintingColor(_text.RED)
        print("U HAVE NOT DOWNLOADED THE REQUIRED DATA!")
        _text.setPrintingColor(_text.WHITE)

        if cutie.prompt_yes_or_no(f"{_text.RED} DO U WANT TO DOWNLOAD REQUIRED DATA? {_text.WHITE}"):
            downloadData()
        else:
            _text.setPrintingColor(_text.RED)
            print("EXITING PROGRAM")
            return

    opt = askOptions()
    routes = []
    for _f in os.listdir(folder+"/download"):
        with open("data/download/"+_f) as f:
            comInfo = json.load(f)

            sellingShops = [s for s in comInfo if s["action"] == "SELLS" and ( (not s["isHidden"]) or (opt["hiddenShopsAllowed"]) )]
            buyingShops  = [s for s in comInfo if s["action"] == "BUYS"  and ( (not s["isHidden"]) or (opt["hiddenShopsAllowed"]) )]

            

            for sellingShop in sellingShops:
                for buyingShop in buyingShops:
                    d = buyingShop["price"]-sellingShop["price"]
                    if d > 0:
                        routes.append([d,buyingShop,sellingShop])

    routes.sort(key=itemgetter(0))
    topComs = list(dict.fromkeys([x[1]["itemName"] for x in routes if x]))
    print("Top comodeties pick one ore multible to know more info about (use up en down arrow keys to navigate and space to select/deselect and enter to confirm choises): ")
    selectedComs = cutie.select_multiple(topComs)
    for _c in selectedComs:
        c = topComs[_c]
        _text.setPrintingColor(_text.CYAN)
        print("")
        _text.printBanner(c)
        print("")
        _text.setPrintingColor(_text.WHITE)
        for r in routes:
            if r[1]["itemName"] == c:

                
                if r[2]['location'].split(" > ")[1] == r[1]['location'].split(" > ")[1]:
                    _text.setPrintingColor(_text.GREEN)
                
                if opt["onlyGreen"] and not (r[2]['location'].split(" > ")[1] == r[1]['location'].split(" > ")[1]):
                    pass

                else:

                    print(f"")
                    print(f"Option for ")
                    print(f"Buy  @ {r[2]['location'] + ' > ' + r[2]['shop']} for {r[2]['price']}")
                    print(f"Sell @ {r[1]['location'] + ' > ' + r[1]['shop']} for {r[1]['price']}")
                    print(f"Profit: {r[0]*opt['cargoCapacity']}, {r[0]}/scu ")
                    print(f"")

                _text.setPrintingColor(_text.WHITE)

def main() -> int:

    

    
    welcomeSign()

    print()
    optionsMenuText = [
        "Welcome!, what do u want to do? ",
        "Download/Update comodetie data.",
        "Show the best routes based on given data.",
        "Both!",
        "Or... QUIT?!"
    ]
    optionsMenuCaptions = [
        optionsMenuText.index("Welcome!, what do u want to do? ")
    ]
    selectedOption = cutie.select(optionsMenuText,optionsMenuCaptions,confirm_on_select=True,selected_index=1)
    print()

    if selectedOption == 1:
        downloadData()
        return 1
    
    elif selectedOption == 2:
        showData()

    elif selectedOption == 3:
        downloadData()
        showData()

    else:
        return 1



    return 1

if __name__ == "__main__":
    exitCode = "CRASH"

    """
    try:
        exitCode = main()
    except Exception as e:
        open("crash.log","w+").write(str(e))
        _text.setPrintingColor(_text.RED)
        print("unexcpected crash, details dumped to crash.log")
        _text.setPrintingColor(_text.WHITE)
    """
    exitCode = main()


    print(f"Code finished with exit code: {exitCode}")
    input("Press enter to exit. > ")