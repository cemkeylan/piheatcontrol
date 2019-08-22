#!/bin/sh

BASEDIR="$(pwd)"
sudo apt update
sudo apt install dialog libpq5 -y
SERVERNAME="$(dialog --inputbox 'Enter postgres server address e.g pg.domain.ld' 10 60 3>&1 1>&2 2>&3)"
DBNAME="$(dialog --inputbox 'Enter database name e.g. postgres' 10 60 3>&1 1>&2 2>&3)"
DBPORT="$(dialog --inputbox 'Enter port number for postgres server, leave blank if it is 5432 (default)' 10 60 3>&1 1>&2 2>&3)"
USERNAME="$(dialog --inputbox 'Enter your username' 10 60 3>&1 1>&2 2>&3)"
PASSWORD="$(dialog --passwordbox 'Enter your password' 10 60 3>&1 1>&2 2>&3)"
[ -z "$DBPORT" ] && DBPORT="5432"
if [ -z "$SERVERNAME" ] || [ -z "$DBNAME" ] || [ -z "$USERNAME" ]
then
	dialog --msgbox "The program is going to exit because you did not fill all of the required input areas." 10 60
	clear
fi	
printf \
"class credentials():\n\
    name = \"$SERVERNAME\"\n\
    db = \"$DBNAME\"\n\
    port = \"$DBPORT\"\n\
    username = \"$USERNAME\"\n\
    password = \"$PASSWORD\"\n\n\n" > $BASEDIR/customs.py
clear
MAXTEMP="$(dialog --inputbox 'Enter the maximum temperature for the program to send an alarm (Leave empty if you do not want an alarm)' 10 60 3>&1 1>&2 2>&3)"
[ -z $MAXTEMP ] && MAXTEMP="None"
printf \
"class heat():\n\
    max = $MAXTEMP\n\n\n" >> $BASEDIR/customs.py
clear
! [ -e $HOME/.notifymailrc ] && notifymail.py --setup
clear
