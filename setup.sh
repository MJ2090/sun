echo "BASE started =============================="
sudo apt update
sudo apt install python3-pip -y
sudo apt install mlocate -y
sudo apt install nginx -y
sudo apt install mysql-server -y
pip install django
pip install django-ratelimit
pip install openai
pip install openai[embeddings]
pip install gunicorn
pip install stripe
pip install numpy
pip install pandas
pip install tiktoken
pip install mysql-connector-python
pip install boto3
echo "BASE ended =============================="

echo "DJANGO started =============================="
echo "export PYTHONPATH=~/moon:$PYTHONPATH" >> ~/.bashrc
echo "export SECRET_KEY='$(openssl rand -hex 40)'" > ~/.DJANGO_SECRET_KEY
source ~/.DJANGO_SECRET_KEY
echo "DJANGO ended =============================="

echo "BASH started =============================="
echo 'export LD_LIBRARY_PATH=:/usr/lib/x86_64-linux-gnu/' >> ~/.bashrc
echo 'source .DJANGO_SECRET_KEY' >> ~/.bashrc
echo 'alias gl="git pull"' >> ~/.bashrc
echo 'alias dr="python3 manage.py runserver 0.0.0.0:8000"' >> ~/.bashrc
echo 'alias p3="python3"' >> ~/.bashrc
echo 'alias dc="python3 manage.py collectstatic"' >> ~/.bashrc
echo 'alias gk="pkill gunicorn"' >> ~/.bashrc
echo 'alias gs="gunicorn -c config/gunicorn/prod.py"' >> ~/.bashrc
echo 'alias gt="tail -f /var/log/gunicorn/error.log"' >> ~/.bashrc
echo 'sudo mkdir -pv /var/{log,run}/gunicorn/' >> ~/.bashrc
echo 'sudo chown -cR ubuntu:ubuntu /var/{log,run}/gunicorn/' >> ~/.bashrc
echo "BASH ended =============================="
echo "======>>>> May need to manually run source .bashrc"
echo "======>>>> May need to config nginx"
echo "======>>>> May need to adjust the chown cmd"
echo "======>>>> May need to run gs + gt to see gunicorn works"
echo "======>>>> May need to open http://IP to see nginx works"
echo "======>>>> May need to add IP to ALLOWED_HOSTS"
echo "======>>>> May need to p3 manage.py createsuperuser"
echo "======>>>> May need to export OPENAI_API_KEY=***"
