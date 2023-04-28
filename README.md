# about nginx
config file: 

/etc/nginx/sites-available/mysite

cmd:
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl status nginx
# about gunicorn
config file:
/mysite/config/gunicorn/prod.py
/mysite/config/gunicorn/dev.py
cmd:
gunicorn -c config/gunicorn/prod.py
pkill gunicorn
tail -f /var/log/gunicorn/error.log
