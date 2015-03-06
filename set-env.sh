#!/bin/bash

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
	
	echo ''
}

# Python 2.7
chk_pkg 'python2.7'

# Django
chk_pkg 'python-django'
chk_pkg 'python-django-extensions'

# MySQL
chk_pkg 'nysql-server'
chk_pkg 'python-mysqldb'
