#!/bin/bash

#generated new IP 

function newIP(){

    local IP=$(($RANDOM%256)).$(($RANDOM%256)).$(($RANDOM%256)).$(($RANDOM%256))
    echo $IP

}
