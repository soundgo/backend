% Prepare SoundGo for deployment.
release: sh -c 'cd soundgo_api && python3 manage.py makemigrations && python3 manage.py migrate && echo "from accounts.models import Actor; from django.contrib.auth import get_user_model; from configuration.models import Configuration; from languages.models import Language; from records.models import Category; UserAccount = get_user_model();\nConfiguration.objects.all().delete();\nconfig = Configuration.objects.create(maximum_radius=2000, minimum_radius=20, time_listen_advertisement=3, minimum_reports_ban=10); config.save();\nCategory.objects.all().delete();\ncategory1 = Category.objects.create(name='"'"'Leisure'"'"', maxTimeRecord=60, minDurationMap=259200); category1.save(); category2 = Category.objects.create(name='"'"'Experience'"'"', maxTimeRecord=60, minDurationMap=259200); category2.save(); category3 = Category.objects.create(name='"'"'Tourism'"'"', maxTimeRecord=60, minDurationMap=259200); category3.save();\nLanguage.objects.all().delete();\nlanguage1 = Language.objects.create(name='"'"'Spanish'"'"'); language1.save(); language2 = Language.objects.create(name='"'"'French'"'"'); language2.save(); language3 = Language.objects.create(name='"'"'Català'"'"'); language3.save(); language4 = Language.objects.create(name='"'"'Portuguese'"'"'); language4.save(); language5 = Language.objects.create(name='"'"'Italian'"'"'); language5.save(); language6 = Language.objects.create(name='"'"'German'"'"'); language6.save(); language7 = Language.objects.create(name='"'"'Japanese'"'"'); language7.save(); language8 = Language.objects.create(name='"'"'Chinese'"'"'); language8.save(); language9 = Language.objects.create(name='"'"'English'"'"'); language9.save(); language10 = Language.objects.create(name='"'"'Euskera'"'"'); language10.save(); language11 = Language.objects.create(name='"'"'Galician'"'"'); language11.save(); language12 = Language.objects.create(name='"'"'Arab'"'"'); language12.save(); language13 = Language.objects.create(name='"'"'Other'"'"'); language13.save();\nUserAccount.objects.all().delete();\nuser_account_u = UserAccount.objects.create_user_account('"'"'soundgouser'"'"', '"'"'soundgouser'"'"'); language_u = Language.objects.get(name='"'"'Other'"'"'); actor_u = Actor.objects.create(user_account=user_account_u, email='"'"'soundgouser@email.com'"'"', language=language_u); actor_u.save();\nuser_account_a = UserAccount.objects.create_super_user_account('"'"'soundgoadmin'"'"', '"'"'soundgoadmin'"'"'); language_a = Language.objects.get(name='"'"'Other'"'"'); actor_a = Actor.objects.create(user_account=user_account_a, email='"'"'soundgoadmin@email.com'"'"', language=language_a); actor_a.save();" | python3 ./manage.py shell'

% Deploy SoundGo.
web: sh -c 'cd soundgo_api && gunicorn soundgo_api.wsgi --log-file -'
