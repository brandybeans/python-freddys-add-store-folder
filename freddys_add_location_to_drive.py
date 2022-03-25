import fileinput
import pyperclip
import os
import shutil
import re

'''Script Made by Brandon Hahn 2022'''

'''Log File Location'''
debug = 0
if debug == 0:
    log_file = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\\pdill\\add_location_log.txt"
else:
    log_file = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\\pdill\\add_location_log - Copy.txt"

'''
Blank Staging File folder location
'''
blank_staging_folder = "\\\\192.168.1.100\\map_as_y\\Brink\Customers\\FFC\\pdill\\Blank Staging File - Brink"

'''
NAS folder location
'''
network_drive_loc = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\Staging\\"
'''
Main function that adds a new store folder on the network drive using the contents of the Blank Staging File.
Using pyperclip is adds the Location ID from the clipboard and edits each .cfg file in their 
respective folder.
'''
def add_location_to_drive():
    store_num = input("What is the store number? ")
    term = "R1"
    filename = network_drive_loc+"{}".format(store_num)
    if not os.path.exists(filename):
        #os.makedirs(filename)
        src = blank_staging_folder
        dst = filename
        shutil.copytree(src, dst)
    filename = network_drive_loc+"{}\\{}\\Register.cfg".format(store_num, term)
    file = open(filename, "r")
    line = file.read()
    file.close()
    regex = r"(\w\w\w\w\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\w\w\w\w\w\w\w\w)"
    regexsearch = re.search(regex, line)
    text_to_search = regexsearch[1]
    text_to_search2 = "00000000-0000-0000-0000-000000000000"
    Clipboard_test = input("Once LocationID is copied to clipboard press enter to continue")
    replacement_text = pyperclip.paste()
    '''
    Checks if the location ID matches the 00000000-0000-0000-0000-000000000000 format.
    '''
    if not len(text_to_search2) == len(replacement_text):
        print("Warning the text that you copied doesn't match the 00000000-0000-0000-0000-000000000000 format!")
        print("Please delete the store folder you created on the Y drive and try again!")
        run_again = input("Do you want to add another location to the y Drive? ")
        run_again = run_again.upper()
        if run_again[0] == "Y":
            add_location_to_drive()
        return 0
    '''
    If there's a duplicate it'll warn the user.
    '''
    if duplicate_locid_check(replacement_text, log_file):
        run_again = input("\nAre you sure you want to continue with location ID " + replacement_text + "? ")
        run_again = run_again.upper()
        if not run_again[0] == "Y":
            print("Please delete the store folder you created on the Y drive and try again!")
            exitinput = input("Press enter to continue")
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

    print("Added store {} with LocationID {}.".format(store_num, replacement_text))
    print("Please confirm LocationID before exiting")
    os.system('notepad.exe ' + filename)
    run_again = input("Do you want to add another location to the y Drive? ")
    run_again = run_again.upper()
    if run_again[0] == "Y":
        add_location_to_drive()
    return 0

'''
Edits the .cfg file based on the given parameters.
'''
def replace_loc_id(store_num, term, type, text_to_search, replacement_text):
    filename = network_drive_loc+"{}\\{}\\{}.cfg".format(store_num, term, type)
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

'''
Checks if Location ID has already been used in the log file.
If there is a duplicate in the log file it'll warn the user first.
'''
def duplicate_locid_check(locid, log_file):
    if os.path.exists(log_file):
        duplicates = []
        regex = r"(" + re.escape(locid) + r")"

        with open(log_file) as file:

            for line in file:
                regexsearch = re.search(regex, line)
                if not regexsearch:
                    pass
                else:
                    duplicates.append(line)
        if len(duplicates) > 0:
            print("Warning! That location ID has already been used! See below. \n")
            for i in duplicates:
                print(i.strip())
            return True
        return False
    return False


#duplicate_locid_check("7f341892-5609-446b-b1b3-c4d8730102f3", log_file)
add_location_to_drive()
