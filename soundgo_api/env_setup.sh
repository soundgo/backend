#!/bin/bash
# Local environment setup script for SoundGo

################### INSTALL REQUIREMENTS ###################

echo -e "\n<<<< Installing requirements >>>>\n"

pip3 install -r requirements.txt

###################### MAKE MIGRATIONS #####################

echo -e "\n<<<< Making migrations >>>>\n"

python3 manage.py makemigrations

########################## MIGRATE #########################

echo -e "\n<<<< Applying migrations  >>>>\n"

python3 manage.py migrate