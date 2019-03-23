% Prepare SoundGo for deployment.
release: sh -c 'cd soundgo_api && python3 manage.py makemigrations && python3 manage.py migrate'
% Deploy SoundGo.
web: sh -c 'cd soundgo_api && gunicorn soundgo_api.wsgi --log-file -'
