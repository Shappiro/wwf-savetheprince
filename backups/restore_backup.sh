#!/bin/bash
#############################################################################
#
# perform_backup.sh
#
# SCRIPT:   	perform_database_backup
# AUTHOR(S):	Aaron Iemma - 02/08/2016
# PURPOSE:  	Restores databases from some .gz file
# LICENCE:		BEER-WARE
#
# ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  <wolfs.bleat@gmail.com> wrote this file. As long as you retain this notice, you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return. $USER Iemma
#  ----------------------------------------------------------------------------
#
#############################################################################

# $1 dbname
# $2 db backup file

PORT=$(cat ../.env | grep DATABASE_PORT | sed 's/DATABASE\_PORT\=//g')
HOST=$(cat ../.env | grep DATABASE_HOST | sed 's/DATABASE\_HOST\=//g')
USER=$(cat ../.env | grep DATABASE_USER | sed 's/DATABASE\_USER\=//g')

PGPASSWORD=$(cat ../.env | grep DATABASE_PW | sed 's/DATABASE\_PW\=//g') dropdb -U $USER -p $PORT -h $HOST $1
PGPASSWORD=$(cat ../.env | grep DATABASE_PW | sed 's/DATABASE\_PW\=//g') createdb -U $USER -p $PORT -h $HOST $1
cat $2 | gunzip | PGPASSWORD=$(cat ../.env | grep DATABASE_PW | sed 's/DATABASE\_PW\=//g') psql -U $USER -p $PORT -h $HOST $1