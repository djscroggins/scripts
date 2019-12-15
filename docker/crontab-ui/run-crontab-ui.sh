cd ..
./docker-login.sh
docker run -d -p 8000:8000 --name crontab-ui alseambusher/crontab-ui
sleep 5
open http://localhost:8000/
