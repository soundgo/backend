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

###################### CREATE LANGUAGE #####################
echo -e "\n<<<< Creating LANGUAGES >>>>\n"

python3 manage.py shell -c "from accounts.models import Language; Language.objects.all().delete();"
python3 manage.py shell -c "from accounts.models import Language; language1 = Language.objects.create(name='Spanish'); language1.save(); language2 = Language.objects.create(name='French');
language2.save(); language3 = Language.objects.create(name='Catalá'); language3.save(); language4 = Language.objects.create(name='Portuguese'); language4.save();
language5 = Language.objects.create(name='Italian'); language5.save(); language6 = Language.objects.create(name='German'); language6.save(); language7 = Language.objects.create(name='Japanese');
language7.save(); language8 = Language.objects.create(name='Chinese'); language8.save(); language9 = Language.objects.create(name='English'); language9.save();
language10 = Language.objects.create(name='Euskera'); language10.save(); language11 = Language.objects.create(name='Galician'); language11.save();
language12 = Language.objects.create(name='Arab'); language12.save(); language13 = Language.objects.create(name='Other'); language13.save();"

echo -e "Languages created\n"

###################### CREATE SUPERUSER  ###################

echo -e "\n<<<< Creating superuser >>>>\n"

python3 manage.py shell -c "from accounts.models import UserAccount; UserAccount.objects.all().delete();"
python3 manage.py shell -c "from accounts.models import Actor; from django.contrib.auth import get_user_model; from accounts.models import Language; UserAccount = get_user_model(); user_account = UserAccount.objects.create_super_user_account('soundgoadmin', 'soundgoadmin'); language = Language.objects.get(name='Other'); actor = Actor.objects.create(user_account=user_account, email='soundgoadmin@email.com', language=language); actor.save();"

echo -e "Superuser created with the following credentials: ['soundgoadmin', 'soundgoadmin']"

##################### POPULATE DATABASE  ###################

echo -e "\n<<<< Populating database >>>>\n"

python3 manage.py shell -c "from records.models import Category; Category.objects.all().delete();"
python3 manage.py shell -c "from records.models import Category; category1 = Category.objects.create(name='Leisure', maxTimeRecord=60, minDurationMap=259200); category1.save(); category2 = Category.objects.create(name='Experience', maxTimeRecord=60, minDurationMap=259200); category2.save(); category3 = Category.objects.create(name='Tourism', maxTimeRecord=60, minDurationMap=259200); category3.save();"

echo -e "Database populated\n"
