#!/bin/bash
# Local environment setup script for SoundGo

################### INSTALL REQUIREMENTS ###################

echo -e "\n<<<< Installing requirements >>>>\n"

cd ..
pip3 install -r requirements.txt

###################### MAKE MIGRATIONS #####################

echo -e "\n<<<< Making migrations >>>>\n"

cd soundgo_api
python3 manage.py makemigrations

########################## MIGRATE #########################

echo -e "\n<<<< Applying migrations  >>>>\n"

python3 manage.py migrate

##################### POPULATE DATABASE  ###################

echo -e "\n<<<< Populating database >>>>\n"

python3 manage.py shell -c "from records.models import Category; Category.objects.all().delete();"
python3 manage.py shell -c "from records.models import Category; category1 = Category.objects.create(name='Leisure', maxTimeRecord=60, minDurationMap=259200); category1.save(); category2 = Category.objects.create(name='Experience', maxTimeRecord=60, minDurationMap=259200); category2.save(); category3 = Category.objects.create(name='Tourism', maxTimeRecord=60, minDurationMap=259200); category3.save();"


python3 manage.py shell -c "from configuration.models import Configuration; Configuration.objects.all().delete();"
python3 manage.py shell -c "from configuration.models import Configuration; config = Configuration.objects.create(maximum_radius=20000, minimum_radius=20, time_listen_advertisement=3, minimum_reports_ban=10, time_extend_audio=3600); config.save();"

echo -e "Database populated"

###################### CREATE USER  ###################

echo -e "\n<<<< Creating user >>>>\n"

python3 manage.py shell -c "from accounts.models import UserAccount; UserAccount.objects.all().delete();"
python3 manage.py shell -c "from accounts.models import Actor; from django.contrib.auth import get_user_model; UserAccount = get_user_model(); user_account = UserAccount.objects.create_user_account('soundgouser', 'soundgouser', is_active=True); actor = Actor.objects.create(user_account=user_account, email='soundgouser@email.com', photo='https://res.cloudinary.com/soundgov3/image/upload/v1556306590/photos/manuel_hsjzbx.jpg'); actor.save();"

echo -e "User created with the following credentials: ['soundgouser', 'soundgouser']"

###################### CREATE ADVERTISER  ###################

echo -e "\n<<<< Creating advertiser >>>>\n"

python3 manage.py shell -c "from accounts.models import CreditCard; CreditCard.objects.all().delete();"
python3 manage.py shell -c "from accounts.models import Actor, CreditCard; from django.contrib.auth import get_user_model; UserAccount = get_user_model(); user_account = UserAccount.objects.create_user_account('soundgoadvertiser', 'soundgoadvertiser', is_active=True); credit_card = CreditCard.objects.create(holderName = 'Carlos Mallado', brandName= 'MASTERCARD', number= '5364212315362996', expirationMonth = 7, expirationYear = 21, cvvCode= 841, isDelete= False) ;actor = Actor.objects.create(user_account=user_account, email='soundgoadvertiser@email.com', photo='https://res.cloudinary.com/soundgov3/image/upload/v1556306591/photos/carlos_ebw2lm.jpg', credit_card = credit_card); actor.save();"


echo -e "Advertiser created with the following credentials: ['soundgoadvertiser', 'soundgoadvertiser']"

###################### CREATE SUPERUSER  ###################

echo -e "\n<<<< Creating superuser >>>>\n"

python3 manage.py shell -c "from accounts.models import Actor; from django.contrib.auth import get_user_model; UserAccount = get_user_model(); user_account = UserAccount.objects.create_super_user_account('soundgoadmin', 'soundgoadmin'); actor = Actor.objects.create(user_account=user_account, email='soundgoadmin@email.com', photo='https://res.cloudinary.com/soundgov3/image/upload/v1556306590/photos/rafael_wk9h7e.jpg'); actor.save();"

echo -e "Superuser created with the following credentials: ['soundgoadmin', 'soundgoadmin']\n"