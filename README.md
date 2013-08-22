# WWW Foo

## The www.foo(cafe).org Django application

### Admin user

fooadmin/likeaboss

### Dependencies

pip freeze will give you this:

    Django==1.5.2
    MySQL-python==1.2.4
    PIL==1.1.7
    django-google-maps==0.2.2
    mock==1.0.1
    wsgiref==0.1.2

And to get tagging support, I've used this bastard

    https://github.com/alex/django-taggit.git

It has to be cloned and installed manually...


## Vagrant box

*Please Note* The base box the used in the vagrant file isn't  available
on a da net yet...

The vagrant used is a Debian box, see more in the Vagrantfile. Provisioning
of the box is defined by the scripts in the ``vagrant/`` folder.

Note, I'm using NFS to share folders between the host and the box so NFS
client software should be installed on the box. If not do it with:

    sudo apt-get install nfs-common portmap

### Up:ing the box

When you up the box for the first time you need to comment out the host
sharing setting. After the box has been provisioned the after the first
``Vagrant up`` you can restore the sharing setting again.

### Host config

Edit your host configuration on, yes indeed, your host machine, i.e. modify the
``/etc/hosts`` to include:

    192.168.56.80   dev-foocafe.org www.dev-foocafe.org


