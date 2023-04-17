#!/usr/bin/bash

sudo rm -rf /home/ubuntu/logs/*
sudo mkdir /home/ubuntu/logs

sudo cp /home/ubuntu/Octagon-BE/gunicorn/gunicorn.socket  /etc/systemd/system/gunicorn.socket
sudo cp /home/ubuntu/Octagon-BE/gunicorn/gunicorn.service  /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service

