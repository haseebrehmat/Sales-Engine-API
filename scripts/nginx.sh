
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-available/octagon

sudo cp /home/ubuntu/Octagon-BE/nginx/nginx.conf /etc/nginx/sites-available/octagon
sudo ln -s /etc/nginx/sites-available/octagon /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/octagon /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

