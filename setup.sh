sudo apt update
sudo apt install python3-pip -y
sudo apt install mlocate -y
sudo apt install nginx -y
pip install django
pip install django-ratelimit
pip install openai
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
echo 'alias gl="git pull"' >> ~/.bashrc
echo 'alias dr="python3 manage.py runserver 0.0.0.0:8000"' >> ~/.bashrc
echo 'alias p3="python3"' >> ~/.bashrc
echo 'alias dc="python3 manage.py collectstatic"' >> ~/.bashrc
echo 'alias gk="pkill gunicorn"' >> ~/.bashrc
echo 'alias gs="gunicorn -c config/gunicorn/prod.py"' >> ~/.bashrc
echo "BASH ended =============================="
