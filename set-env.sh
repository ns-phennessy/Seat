#!/bin/bash

if [ `id -u` != "0" ]; then
    echo 'You must be root to execute this script'
    exit
fi

success="\e[0;32m"
error="\e[0;31m"
white="\e[0;37m"

function chk_pkg(){
	dpkg -l $1 > /dev/null 2>&1
	INSTALLED=$?

	echo "Checking install of $1..." 

	if [ $INSTALLED == '0' ]; then
		echo "$1 is up to date."
	else
		echo "Installing $1"
		apt-get --assume-yes install $1 > /dev/null 2>&1
		
		if [ $? -eq 0 ]; then
			echo "$success Successful installation"
		else
			echo -e "! $error Failed to install $white [ $1 ]"
		fi	
	fi
	
	echo -e '\e[0m'
}

REQUIRED_PACKAGES="
    python2.7 
    python-django 
    python-django-extensions 
    mysql-server-5.6 
    python-mysqldb
    libmysqlclient-dev
    python-dev
"

for PACKAGE in $REQUIRED_PACKAGES; do
    chk_pkg $PACKAGE
done

