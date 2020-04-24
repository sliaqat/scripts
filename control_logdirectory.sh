#!/bin/bash
echo 'Checking host = ' $(hostname)
OLDTHANDAYS=30

#deletion Procedure

DeleteFromDirectory() {
	directory=$1
	description=$2
	foldersizethreshold=$3
	days=$4

	foldersize=$(du -s $directory|awk -F " " '{print $1}')

	echo '---' $description ' has size of ' $foldersize
	if [ $foldersize -gt $foldersizethreshold ]
	then
        	echo '----Removing files from ' $directory
        	find $directory -type f -mtime +$days -exec rm -rf {} \;
	else
        	echo '----no deletion done'
	fi

}

#
#DeleteFromDir	    directory_path    description  size_threshold(bytes)  days_to_remove(if size is greater than bytes specified)
DeleteFromDirectory "/opt/apache-tomcat/logs/" "Apache Logs" '3000000' '5'
DeleteFromDirectory "/var/log/app01/" "Application Archive Logs" '10000000' '30'

echo ' finished script on ' $(hostname)
