import requests, lxml
from re import compile, findall

# make the login page request

def loginpagerequest(URL):

    r = requests.get(URL)
    return r

def initial_login(URL,csrftoken, sessionCookie):
    username="carlos"
    password="montoya"
    cookies={'session':sessionCookie}
    data="csrf=%s&username=%s&password=%s"%(csrftoken, username, password)
    r=requests.post(URL, data, cookies=cookies)
    mfasession = r.request.headers['Cookie'].split('=')[2] # we performed a redirect, and obtained a new session key. 
    pattern = compile(r'(?<=csrf\" value=\")[^\"]+')
    mfacsrf= pattern.findall(r.text)[0]
    return [mfasession, mfacsrf]

def MFApagerequest(mfasession, mfacsrf, mfacode, mfaurl):
    cookies={'session':mfasession}
    data="csrf=%s&mfa-code=%s"%(mfacsrf, mfacode)
    r=requests.post(mfaurl, data, cookies=cookies)
    return(r.status_code)

def macrofunction(URL, sessionCookie, MFAcode):
    cookies={'session':sessionCookie}
    URL2=URL+'login2'
    URL+='login'
    r=requests.get(URL, cookies=cookies)
    # get the csrf value
    pattern = compile(r'(?<=csrf\" value=\")[^\"]+')
    loginCSRF=pattern.findall(r.text)[0]
    # get to the MFA page
    mfasession, mfacsrf=initial_login(URL, loginCSRF, sessionCookie)
    # make request to MFA page
    statusCode=MFApagerequest(mfasession, mfacsrf, MFAcode,URL2)
    return statusCode
    # if code not found then reset connection.
        



    

