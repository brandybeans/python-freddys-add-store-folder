import fileinput
import pyperclip
import os
import shutil
import re

#Script Made by Brandon Hahn 2022

log_file = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\\pdill\\add_location_log.txt"

def add_location_to_drive():
    store_num = input("What is the store number? ")
    term = "R1"
    filename = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\Staging\\{}".format(store_num)
    if not os.path.exists(filename):
        #os.makedirs(filename)
        src = "\\\\192.168.1.100\\map_as_y\\Brink\Customers\\FFC\\pdill\\Blank Staging File - Brink"
        dst = filename
        shutil.copytree(src, dst)
    filename = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\Staging\\{}\\{}\\Register.cfg".format(store_num, term)
    file = open(filename, "r")
    line = file.read()
    file.close()
    #print(line)
    regex = r"(\w\w\w\w\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\w\w\w\w\w\w\w\w)"
    regexsearch = re.search(regex, line)
    text_to_search = regexsearch[1]
    #print(text_to_search)
    text_to_search2 = "00000000-0000-0000-0000-000000000000"

    Clipboard_test = input("Once LocationID is copied to clipboard press enter to continue")

    replacement_text = pyperclip.paste()
    if not len(text_to_search2) == len(replacement_text):
        print("Warning the text that you copied doesn't match the 00000000-0000-0000-0000-000000000000 format!")
        print("Please delete the store folder you created on the Y drive and try again!")
        run_again = input("Do you want to add another location to the y Drive? ")
        run_again = run_again.upper()
        if run_again[0] == "Y":
            add_location_to_drive()
        return 0

    logfile = open(log_file, "a+")
    logfile.write("Added store {} with LocationID {}.".format(store_num, replacement_text) + "\n")
    logfile.close()

    replace_loc_id(store_num, "R1", "Register", text_to_search, replacement_text)
    replace_loc_id(store_num, "R2", "Register", text_to_search, replacement_text)
    replace_loc_id(store_num, "R3", "Register", text_to_search, replacement_text)
    replace_loc_id(store_num, "R4", "Register", text_to_search, replacement_text)
    replace_loc_id(store_num, "R5", "Register", text_to_search, replacement_text)
    replace_loc_id(store_num, "Grill", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "Make", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "Expo", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "Custard", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "DT Grill", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "DT Make", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "Grill 2", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "DT Expo", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "DT Grill 2", "Kitchen", text_to_search, replacement_text)
    replace_loc_id(store_num, "DT Expo 2", "Kitchen", text_to_search, replacement_text)

    print("Please confirm LocationID before exiting")
    os.system('notepad.exe ' + filename)
    run_again = input("Do you want to add another location to the y Drive? ")
    run_again = run_again.upper()
    if run_again[0] == "Y":
        add_location_to_drive()
    return 0

def replace_loc_id(store_num, term, type, text_to_search, replacement_text):
    filename = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\Staging\\{}\\{}\\{}.cfg".format(store_num, term, type)
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

add_location_to_drive()
