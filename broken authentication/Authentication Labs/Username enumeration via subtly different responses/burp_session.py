#!/bin/python3

import requests, re

def get_key(url):
    r = requests.get(url)
    get_session = re.compile(r'\w*(?=;)')
    it = get_session.finditer(r.headers['Set-Cookie'])
    session_cookie=it.__next__().group()
    return session_cookie