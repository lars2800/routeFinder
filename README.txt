# Star Citizen Route Finder

A simple python project to find optimal trading routes for star citizen
Based on https://sc-trade.tool/home data.

# How to build
option 1 ) Download and run the .exe in the build folder (Might be flagged by anti-virus or not work)

option 2 ) Download repo, run __init__.py

option 3 ) Download repo, install auto-py-to-exe and pyfiglet, run following command (replace the '<REPO PATH>' with the path of the repo and 'USER' with Ur windows username), this should build the exe:

pyinstaller --noconfirm --onefile --console --icon "<REPO PATH>/3553539.ico" --name "ScRouter" --hidden-import "pyfiglet" --hidden-import "pyfiglet.fonts" --add-data "<REPO PATH>/_text.py;." -F --add-data "C:\Users\<USER>\AppData\Roaming\Python\Python311\site-packages\pyfiglet\fonts;./pyfiglet/fonts" "<REPO PATH>/__init__.py"


# Legal and questions

IF U RUN THIS SCRIPT IT IS UR RESPONSIBILITY FOR ANYTHING THAT HAPPENS.
THIS PROJECT IS OPEN SOURCE BUT U CAN NOT USE IT FOR COMMERCIAL USE WITHOUT EXPLICIT WRITTEN PERMISSION FROM ME.
I AM NOT AN NATIVE SPEAKER OF THE ENGLISH LANGUAGE SO APPLY COMMON SENSE TO THESE RULES.

If u have any Questions be free to send me an DM on discord (legolars2800) (can take 3 days before I respond, also make sure it's clear that its about this project and not some spam.)
