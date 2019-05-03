% Prepare SoundGo for deployment.
release: sh -c 'cd soundgo_api && python3 manage.py makemigrations && python3 manage.py migrate && echo "from accounts.models import Actor, CreditCard; from django.contrib.auth import get_user_model; from configuration.models import Configuration; from records.models import Category; from tags.models import Tag; UserAccount = get_user_model();\nCreditCard.objects.all().delete();\nConfiguration.objects.all().delete();\nconfig = Configuration.objects.create(maximum_radius=20000, minimum_radius=20, time_listen_advertisement=3, minimum_reports_ban=10); config.save();\nTag.objects.all().delete();\nCategory.objects.all().delete();\ncategory1 = Category.objects.create(name='"'"'Leisure'"'"', maxTimeRecord=60, minDurationMap=259200); category1.save(); category2 = Category.objects.create(name='"'"'Experience'"'"', maxTimeRecord=60, minDurationMap=259200); category2.save(); category3 = Category.objects.create(name='"'"'Tourism'"'"', maxTimeRecord=60, minDurationMap=259200); category3.save();\nUserAccount.objects.all().delete();\nuser_account_u_soundgo = UserAccount.objects.create_user_account('"'"'manuel'"'"', '"'"'Manuel123.'"'"', is_active=True); actor_u_soundgo = Actor.objects.create(user_account=user_account_u_soundgo, email='"'"'manuel@email.com'"'"', photo='"'"'https://res.cloudinary.com/soundgov3/image/upload/v1556306590/photos/manuel_hsjzbx.jpg'"'"'); actor_u_soundgo.save();\nuser_account_ad_soundgo = UserAccount.objects.create_user_account('"'"'carlos'"'"', '"'"'Carlos123.'"'"', is_active=True); credit_card_ad_soundgo = CreditCard.objects.create(holderName ='"'"'Carlos Clebal'"'"', brandName='"'"'MasterCard'"'"', number='"'"'5455 5595 5077 4446'"'"', expirationMonth = 10, expirationYear = 22, cvvCode= 100, isDelete= False); actor_ad_soundgo = Actor.objects.create(user_account=user_account_ad_soundgo, email='"'"'carlos@email.com'"'"', credit_card = credit_card_ad_soundgo, photo='"'"'https://res.cloudinary.com/soundgov3/image/upload/v1556306591/photos/carlos_ebw2lm.jpg'"'"'); actor_ad_soundgo.save();\nuser_account_admin_soundgo = UserAccount.objects.create_super_user_account('"'"'rafael'"'"', '"'"'Rafael123.'"'"'); actor_admin_soundgo = Actor.objects.create(user_account=user_account_admin_soundgo, email='"'"'rafael@email.com'"'"', photo='"'"'https://res.cloudinary.com/soundgov3/image/upload/v1556306590/photos/rafael_wk9h7e.jpg'"'"'); actor_admin_soundgo.save();\nuser_account_u_1 = UserAccount.objects.create_user_account('"'"'aitanaalberro'"'"', '"'"'aitanaalberro123'"'"', is_active=True); actor_u_1 = Actor.objects.create(user_account=user_account_u_1, email='"'"'aitanaalberro@gmail.com'"'"'); actor_u_1.save();\nuser_account_u_2 = UserAccount.objects.create_user_account('"'"'jmanuelsanchez'"'"', '"'"'jmanuelsanchez'"'"', is_active=True); actor_u_2 = Actor.objects.create(user_account=user_account_u_2, email='"'"'jmanuelsanchez@gmail.com'"'"'); actor_u_2.save();\nuser_account_u_3 = UserAccount.objects.create_user_account('"'"'maribelolmo'"'"', '"'"'maribelolmo'"'"', is_active=True); actor_u_3 = Actor.objects.create(user_account=user_account_u_3, email='"'"'maribelolmo@gmail.com'"'"'); actor_u_3.save();\nuser_account_u_4 = UserAccount.objects.create_user_account('"'"'javierfernan'"'"', '"'"'javierfernan'"'"', is_active=True); actor_u_4 = Actor.objects.create(user_account=user_account_u_4, email='"'"'javierfernan@gmail.com'"'"'); actor_u_4.save();\nuser_account_ad_1 = UserAccount.objects.create_user_account('"'"'estudiante'"'"', '"'"'estudiante'"'"', is_active=True); credit_card_ad_1 = CreditCard.objects.create(holderName ='"'"'Estudiante'"'"', brandName='"'"'Visa'"'"', number='"'"'4716 8165 6908 5463'"'"', expirationMonth = 6, expirationYear = 22, cvvCode= 972, isDelete= False); actor_ad_1 = Actor.objects.create(user_account=user_account_ad_1, email='"'"'estudiante@gmail.com'"'"', credit_card = credit_card_ad_1); actor_ad_1.save();\nuser_account_ad_2 = UserAccount.objects.create_user_account('"'"'ñamñam'"'"', '"'"'ñamñam'"'"', is_active=True); credit_card_ad_2 = CreditCard.objects.create(holderName ='"'"'Ñam Ñam'"'"', brandName='"'"'Visa'"'"', number='"'"'4539 5745 2961 7355'"'"', expirationMonth = 12, expirationYear = 23, cvvCode= 867, isDelete= False); actor_ad_2 = Actor.objects.create(user_account=user_account_ad_2, email='"'"'niamniam@gmail.com'"'"', credit_card = credit_card_ad_2); actor_ad_2.save();\nuser_account_ad_3 = UserAccount.objects.create_user_account('"'"'saludortiz'"'"', '"'"'saludortiz'"'"', is_active=True); credit_card_ad_3 = CreditCard.objects.create(holderName ='"'"'Salud Ortiz'"'"', brandName='"'"'MasterCard'"'"', number='"'"'5198 3110 0543 3968'"'"', expirationMonth = 9, expirationYear = 21, cvvCode= 625, isDelete= False); actor_ad_3 = Actor.objects.create(user_account=user_account_ad_3, email='"'"'saludortiz@gmail.com'"'"', credit_card = credit_card_ad_3); actor_ad_3.save();\nuser_account_ad_4 = UserAccount.objects.create_user_account('"'"'barretti'"'"', '"'"'barretti'"'"', is_active=True); credit_card_ad_4 = CreditCard.objects.create(holderName ='"'"'Barretti'"'"', brandName='"'"'Visa'"'"', number='"'"'4485 0538 8450 5251'"'"', expirationMonth = 2, expirationYear = 23, cvvCode= 539, isDelete= False); actor_ad_4 = Actor.objects.create(user_account=user_account_ad_4, email='"'"'barretti@gmail.com'"'"', credit_card = credit_card_ad_4); actor_ad_4.save();\nuser_account_ad_5 = UserAccount.objects.create_user_account('"'"'santamarta'"'"', '"'"'santamarta'"'"', is_active=True); credit_card_ad_5 = CreditCard.objects.create(holderName ='"'"'Santa Marta'"'"', brandName='"'"'Visa'"'"', number='"'"'4539 0313 0420 0006'"'"', expirationMonth = 5, expirationYear = 21, cvvCode= 883, isDelete= False); actor_ad_5 = Actor.objects.create(user_account=user_account_ad_5, email='"'"'santamarta@gmail.com'"'"', credit_card = credit_card_ad_5); actor_ad_5.save();\nuser_account_ad_6 = UserAccount.objects.create_user_account('"'"'lcsfiestas'"'"', '"'"'lcsfiestas'"'"', is_active=True); credit_card_ad_6 = CreditCard.objects.create(holderName ='"'"'LCS Fiestas'"'"', brandName='"'"'Visa'"'"', number='"'"'4539 5512 5526 8397'"'"', expirationMonth = 9, expirationYear = 23, cvvCode= 996, isDelete= False); actor_ad_6 = Actor.objects.create(user_account=user_account_ad_6, email='"'"'lcsfiestas@gmail.com'"'"', credit_card = credit_card_ad_6); actor_ad_6.save();\nuser_account_ad_7 = UserAccount.objects.create_user_account('"'"'barpino'"'"', '"'"'barpino'"'"', is_active=True); credit_card_ad_7 = CreditCard.objects.create(holderName ='"'"'Bar Pino'"'"', brandName='"'"'Visa'"'"', number='"'"'4716 9103 0532 2817'"'"', expirationMonth = 9, expirationYear = 22, cvvCode= 796, isDelete= False); actor_ad_7 = Actor.objects.create(user_account=user_account_ad_7, email='"'"'barpino@gmail.com'"'"', credit_card = credit_card_ad_7); actor_ad_7.save();\nuser_account_ad_8 = UserAccount.objects.create_user_account('"'"'josemaortiz'"'"', '"'"'josemaortiz'"'"', is_active=True); credit_card_ad_8 = CreditCard.objects.create(holderName ='"'"'Josema Ortiz'"'"', brandName='"'"'Visa'"'"', number='"'"'4916 1660 5114 2945'"'"', expirationMonth = 2, expirationYear = 22, cvvCode= 196, isDelete= False); actor_ad_8 = Actor.objects.create(user_account=user_account_ad_8, email='"'"'josemaortiz@gmail.com'"'"', credit_card = credit_card_ad_8); actor_ad_8.save();" | python3 ./manage.py shell'

% Deploy SoundGo.
web: sh -c 'cd soundgo_api && gunicorn soundgo_api.wsgi --log-file -'

% Scheduler.
clock: python3 soundgo_api/clock.py
