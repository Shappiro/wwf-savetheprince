#!/bin/bash
#############################################################################
#
# perform_backup.sh
#
# SCRIPT:   	perform_database_backup
# AUTHOR(S):	Aaron Iemma - 02/08/2016
# PURPOSE:  	Backups all databases from some server
# LICENSE:		BEER-WARE
#
# ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  <wolfs.bleat@gmail.com> wrote this file. As long as you retain this notice, you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return. Aaron Iemma
#  ----------------------------------------------------------------------------
#
#############################################################################

MAIN_DIR="/var/www/wwf-tn-prince/backups"

# reload: cat filename.gz | gunzip | psql dbname
DATABASES=("prince")
TODAY="$(date +'%d_%m_%Y')"
BASEDIR="$MAIN_DIR"
HOST='localhost'
PORT='5432'

for i in "${DATABASES[@]}"
do
	FILE="$BASEDIR"/"$i"_"$TODAY"_backup.gz
	echo "''''''''''''''''''''''"
	echo "Perfoming backup of database $i..."
	echo "''''''''''''''''''''''"
	echo $FILE
	pg_dump -p $PORT $i | gzip > $FILE
	echo "''''''''''''''''''''''"
	echo "Backup of $i database ended."
	echo "''''''''''''''''''''''"
done
