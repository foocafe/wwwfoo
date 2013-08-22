#!/bin/bash

printf "==> Setting up the Foo Vagrant box \n"

sudo mkdir -p /var/vagrant_provision
## The poor mans idempotent provisioning guard
MARKER=/var/vagrant_provision/foobox-installed
if [ -f "${MARKER}" ]; then
    printf "\talready setup, ignoring."
    exit 0
fi

## NFS Client support
sudo apt-get install -yq nfs-common portmap

## nginx
sudo apt-get install -yq nginx

## MySQL client software
sudo apt-get install -yq  mysql-client-5.5

## Python software
### Python dev
sudo apt-get install python-dev

### PIP
sudo apt-get install -yq python-pip

### uWSGI support
sudo apt-get install -yq uwsgi uwsgi-plugin-python

### PIL
sudo apt-get install -yq python-imaging

### MySQL
sudo apt-get install -yq python-mysqldb

### Django
DJANGO_VERSION=1.5.2
#DJANGO=django-${DJANGO_VERSION}
#wget -q https://www.djangoproject.com/download/${DJANGO_VERSION}/tarball/ -O ${DJANGO}.tar.gz
#tar -xzf ${DJANGO}.tar.gz
#rm ${DJANGO}.tar.gz

#cd ${DJANGO}
#sudo python setup.py install
#cd ..
#rm -rf ${DJANGO}

sudo pip install Django==${DJANGO_VERSION}

### Django Google Maps
sudo pip install django-google-maps==0.2.2

## Add the db host to /etc/hosts
sudo bash -c "echo '192.168.1.100 umini.local'  >> /etc/hosts"

## Mark as provisioned
CURRENT_DATE=`date +%Y-%m-%dT%H:%M:%S`
sudo bash -c "echo ${CURRENT_DATE} >> ${MARKER}"
