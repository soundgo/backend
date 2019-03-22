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

###################### CREATE SUPERUSER  ###################

echo -e "\n<<<< Creating superuser >>>>\n"

python3 manage.py shell -c "from accounts.models import UserAccount; UserAccount.objects.all().delete();"
python3 manage.py shell -c "from accounts.models import Actor; from django.contrib.auth import get_user_model; UserAccount = get_user_model(); user_account = UserAccount.objects.create_super_user_account('soundgoadmin', 'soundgoadmin'); actor = Actor.objects.create(user_account=user_account, email='soundgoadmin@email.com'); actor.save();"

echo -e "Superuser created with the following credentials: ['soundgoadmin', 'soundgoadmin']"

##################### POPULATE DATABASE  ###################

echo -e "\n<<<< Populating database >>>>\n"

python3 manage.py shell -c "from records.models import Category; Category.objects.all().delete();"
python3 manage.py shell -c "from records.models import Category; category1 = Category.objects.create(name='Leisure', maxTimeRecord=60, minDurationMap=259200); category1.save(); category2 = Category.objects.create(name='Experience', maxTimeRecord=60, minDurationMap=259200); category2.save(); category3 = Category.objects.create(name='Tourism', maxTimeRecord=60, minDurationMap=259200); category3.save();"

echo -e "Database populated\n"
