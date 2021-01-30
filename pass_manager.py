from cryptography.fernet import Fernet 
import json
from selenium import webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"


def add_data():
    var = bytes("\n", encoding='utf-8')
    # getting key from file
    key_file = open("key.key", "rb")
    key = key_file.read()
    f = Fernet(key)
    key_file.close()

    user ={}
    try:
        user_file = open("user_info.json", "rb")
        user_read = user_file.read()
        user_list = json.loads(user_read)
        user_file.close()
    except:
        user_list = []


# Getting data from password file
    try:
        pass_list=[]
        pass_file = open("pass_list.txt", "rb")
        for password in pass_file:
            pass_decrypt = f.decrypt(password)
            pass_string = str(pass_decrypt)
            pass_list.append(pass_string)     
        pass_file.close()
    except:
        pass_list=[]

    # getting input from user
    user["name"] = input("enter name of website")
    user["url"] = input("enter the url of the website")
    user["username"] = input("enter username of the account")
    pass_input = input("Enter password")

    # adding info to list
    pass_list.append(pass_input)
    user_list.append(user)

    while True:
        # check for continuation
        check = input("Enter more passwords (y/n) ?")
        if check == "n": 
            break
        elif check == "y": 
            user = {}
            user["name"] = input("enter name of website")
            user["url"] = input("enter the url of the website")
            user["username"] = input("enter username of the account")
            password = input("Etner password")            
            # adding info to files
            pass_list.append(password)
            # adding dictionary to list
            user_list.append(user)

    # adding list to file

    user_file = open("user_info.json", "w")
    user_file.write(json.dumps(user_list))
    user_file.close()

    # adding password into password file from password list
    pass_file = open("pass_list.txt", "wb")
    for password in range(len(pass_list)):
        pass_encrypt = f.encrypt(pass_list[password].encode())
        pass_file.write(pass_encrypt + var)
    pass_file.close()





def launch_web():
    pass_list = []
    match_counter = 0

    # getting key
    key_file = open("key.key", "rb")
    key = key_file.read()
    f = Fernet(key)
    key_file.close()

    # Getting data from user file
    try:
        user_file = open("user_info.json","rb")
        user_read = user_file.read()
        user_list = json.loads(user_read)
        user_file.close()
    except:
        print("ERROR: No data in user file")
    # Getting data from password file
    try:
        pass_file = open("pass_list.txt", "rb")
        for password in pass_file:
            pass_decrypt = f.decrypt(password)
            pass_list.append(pass_decrypt)     
        pass_file.close()
    except:
        print("ERROR: No file in password file ")
        return
    unique_list = set()
    for name in range(len(user_list)): 
        unique_list.add(user_list[name]["name"])
    print("list of websites found in files:")
    for item in unique_list:
        print(item)

    # user input 
    user_input = input("Enter the website you want to search the password for")
    
    # search for website name similar to user input
    for name in range(len(user_list)):
        web_name = user_list[name]["name"]
        if web_name == user_input:
            match_counter +=1

            print("""
Result {}
Name: {}
URL: {}
Username: {}
Password: {}
            """. format(match_counter,user_list[name]["name"], user_list[name]["url"], user_list[name]["username"]
            ,pass_list[name].decode(encoding="utf-8")))


    
    if match_counter == 0: 
        print("no result found")
    else:
        confirmation = input("Would you like to launch it? (y/n)")
        if confirmation == "y":
            # opening the link stored in the file
            driver = webdriver.Chrome(PATH)
            for i in range(len(user_list)):
                if user_input == user_list[i]["name"]:
                    driver.get(user_list[i]["url"])
            while True:
                pass

def delete_pass(): 
    # var for creating new line in password file
    var = bytes("\n", encoding='utf-8')
    pass_list = []
    match_counter = 0
    # getting key
    key_file = open("key.key", "rb")
    key = key_file.read()
    f = Fernet(key)
    key_file.close()

    # Getting data from user file
    try:
        user_file = open("user_info.json","rb")
        user_read = user_file.read()
        user_list = json.loads(user_read)
        user_file.close()
    except:
        print("ERROR: No data in user file")
        return
    # Getting data from password file
    try:
        pass_file = open("pass_list.txt", "rb")
        for password in pass_file:
            pass_decrypt = f.decrypt(password)
            pass_string = pass_decrypt.decode(encoding='utf-8')
            pass_list.append(pass_string)     
        pass_file.close()
    except:
        print("ERROR: No file in password file ")
        return
    
    # change the unique list to set to remove any duplicates
    unique_list = set()

    for name in range(len(user_list)): 
        unique_list.add(user_list[name]["name"])
    print("list of websites found in files:")
    for item in unique_list:
        print(item.title())

    # user input 
    user_input = input("Enter the website you want to search the password for")
    
    # search for website name similar to user input
    for name in range(len(user_list)):
        web_name = user_list[name]["name"]
        if web_name == user_input:
            match_counter +=1
            print("""
Result {}
Position: {}
Name: {}
URL: {}
Username: {}
Password: {}
            """. format(match_counter,name +1,user_list[name]["name"],  user_list[name]["url"], user_list[name]["username"]
            ,pass_list[name]))

    del_input = int(input("enter the position number of the one you want to delete"))

    print ("""
Data Deleted: 
Position: {}
Name: {}
URL: {}
Username: {}
Password: {}
    """. format(del_input, user_list[del_input-1]["name"], user_list[del_input-1]["url"], user_list[del_input-1]["username"], pass_list[del_input-1]))
    
    user_list.pop(del_input-1)
    pass_list.pop(del_input-1)

    update_user = open("user_info.json", "w")
    update_user.write(json.dumps(user_list))
    update_user.close()

    update_pass = open("pass_list.txt", "wb")
    for item in range(len(pass_list)):
        pass_encrypt = f.encrypt(pass_list[item].encode())
        update_pass.write(pass_encrypt + var)
    update_pass.close()
    menu()






def decrypted_data():
    # getting key from file to decrypt data
    decrypt_pass =[]
    key_file = open("key.key", "rb")
    key = key_file.read()
    f = Fernet(key)
    key_file.close()

    # opening file 
    pass_list = open("pass_list.txt", "rb")
    user_list = open("user_info.json", "rb")

    # read user_list
    user_read = user_list.read()
    user_info = json.loads(user_read)
    for i in user_info:
        print(i)

    # read password 
    for password in pass_list:
        print(password)
        # decrypt encrypted message
        pass_decrypt = f.decrypt(password)
        # changing type from byte to string
        item = pass_decrypt.decode(encoding='utf-8')
        decrypt_pass.append(item)
        print(item)

    for stuv in decrypt_pass: 
        pass_encrypt = f.encrypt(stuv.encode())
        print(pass_encrypt)
    # decr

def menu():
    while True:
        print("""
        Welcome to password manager: 
        1. Add password
        2. Delete password
        3. Launch Website
        """)
        user_input=int(input("Enter the number of the action you want to perform"))

        if user_input == 1: 
            add_data()
            break
        elif user_input == 2:
            delete_pass()
            break
        elif user_input == 3: 
            launch_web()
            break
        else: 
            print("input not recognized")


menu()