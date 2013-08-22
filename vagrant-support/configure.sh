#!/bin/bash

printf "==> Configuring the Foo Vagrant box \n"

sudo mkdir -p /var/vagrant_provision
## The poor mans idempotent provisioning guard
MARKER=/var/vagrant_provision/foobox-configured
if [ -f "${MARKER}" ]; then
    printf "\talready setup, ignoring."
    exit 0
fi

## nginx configuration for wwwfoo
sudo bash -c "cat > /etc/nginx/sites-available/wwwfoo" <<NGINXWWWFOO
server {

    listen      80;
    server_name www.dev-foocafe.org;
    access_log  /var/log/nginx/wwwfoo.log;

    location / {
        uwsgi_pass 127.0.0.1:3031;
        include uwsgi_params;
    }
}
NGINXWWWFOO

if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
fi

sudo ln -s /etc/nginx/sites-available/wwwfoo /etc/nginx/sites-enabled/wwwfoo
sudo /etc/init.d/nginx restart


## uWsgi configuration for wwwfoo
sudo bash -c "cat > /etc/uwsgi/apps-available/wwwfoo.ini" <<UWSGIWWWFOO
[uwsgi]
chdir = /home/vagrant/host-share
pythonpath = .
socket = 127.0.0.1:3031
master = True
vacuum = True
DEBUG = True
module = app.wsgi:application
processes = 2
daemonize=/var/log/uwsgi/wwwfoo.log
UWSGIWWWFOO

sudo ln -s /etc/uwsgi/apps-available/wwwfoo.ini /etc/uwsgi/apps-enabled/wwwfoo.ini
sudo /etc/init.d/uwsgi restart


## Mark as provisioned
CURRENT_DATE=`date +%Y-%m-%dT%H:%M:%S`
sudo bash -c "echo ${CURRENT_DATE} >> ${MARKER}"
