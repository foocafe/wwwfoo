#!/bin/bash

#: Install and configure a predefined version of  Nginx
#:

nginx_version=1.4.1

printf "==> Building and installing Nginx ${nginx_version} \n"

## The poor mans idempotent provisioning guard
MARKER=/var/vagrant_provision/nginx-installed
if [ -f "${MARKER}" ]; then
    printf "\talready setup, ignoring."
    exit 0
fi

LOG=~/nginx-install.log
rm -f ${LOG}
touch ${LOG}

## Build your own Nginx
sudo apt-get -yq install build-essential >> ${LOG} 2>&1
sudo apt-get -yq install libgeoip-dev libpcre3-dev libssl-dev >> ${LOG} 2>&1

instance_store=/var/instance-store

cd && wget -q http://nginx.org/download/nginx-${nginx_version}.tar.gz
tar xzf nginx-${nginx_version}.tar.gz && cd nginx-${nginx_version}
CFLAGS="-g -O0" ./configure \
  --prefix=/etc/nginx \
  --sbin-path=/usr/sbin/nginx \
  --conf-path=/etc/nginx/nginx.conf \
  --error-log-path=/var/log/nginx/error.log \
  --http-client-body-temp-path=${instance_store}/nginx/body \
  --http-fastcgi-temp-path=${instance_store}/nginx/fastcgi \
  --http-scgi-temp-path=${instance_store}/nginx/scgi \
  --http-uwsgi-temp-path=${instance_store}/nginx/uwsgi \
  --http-log-path=/var/log/nginx/access.log \
  --http-proxy-temp-path=/var/lib/nginx/proxy \
  --lock-path=/var/lock/nginx.lock \
  --pid-path=/var/run/nginx.pid \
  --with-http_realip_module \
  --with-http_geoip_module \
  --with-http_ssl_module >> ${LOG} 2>&1

make >> ${LOG} 2>&1
sudo make install >> ${LOG} 2>&1
cd && rm -rf nginx-${nginx_version} nginx-${nginx_version}.tar.gz

sudo mkdir -p /var/log/nginx
sudo mkdir -p /var/lib/nginx

sudo mkdir -p ${instance_store}/nginx/body
sudo mkdir -p ${instance_store}/nginx/fastcgi
sudo mkdir -p ${instance_store}/nginx/scgi
sudo mkdir -p ${instance_store}/nginx/uwsgi

sudo chown -R www-data:www-data /var/log/nginx
sudo chown -R www-data:www-data /var/lib/nginx

sudo chown -R www-data:www-data ${instance_store}

## Nginx service script

sudo touch /etc/init.d/nginx
sudo bash -c "cat > /etc/init.d/nginx" <<EOF
#!/bin/sh

### BEGIN INIT INFO
# Provides:          nginx
# Required-Start:    $local_fs $remote_fs $network $syslog
# Required-Stop:     $local_fs $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the nginx web server
# Description:       starts nginx using start-stop-daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/sbin/nginx
NAME=nginx
DESC="nginx http server"
PIDFILE=/var/run/\${NAME}.pid

# Include nginx defaults if available
if [ -f /etc/default/nginx ]; then
	. /etc/default/nginx
fi

test -x \${DAEMON} || exit 0

set -e

. /lib/lsb/init-functions

test_nginx_config() {
	if \${DAEMON} -t \${DAEMON_OPTS} >/dev/null 2>&1; then
		return 0
	else
		\${DAEMON} -t \${DAEMON_OPTS}
		return $?
	fi
}

case "\${1}" in
	start)
		echo -n "Starting \${DESC}: "
		test_nginx_config
		# Check if the ULIMIT is set in /etc/default/nginx
		if [ -n "\${ULIMIT}" ]; then
			# Set the ulimits
			ulimit \${ULIMIT}
		fi
		start-stop-daemon --start --quiet --pidfile \${PIDFILE} --exec \${DAEMON} -- \${DAEMON_OPTS} || true
		echo "\${NAME}."
		;;

	stop)
		echo -n "Stopping \${DESC}: "
		start-stop-daemon --stop --quiet --pidfile \${PIDFILE} --exec \${DAEMON} || true
		echo "\${NAME}."
		;;

	restart|force-reload)
		echo -n "Restarting \${DESC}: "
		start-stop-daemon --stop --quiet --pidfile \${PIDFILE} --exec \${DAEMON} || true
		sleep 1
		test_nginx_config
		start-stop-daemon --start --quiet --pidfile \${PIDFILE} --exec \${DAEMON} -- \${DAEMON_OPTS} || true
		echo "${NAME}."
		;;

	reload)
		echo -n "Reloading \${DESC} configuration: "
		test_nginx_config
		start-stop-daemon --stop --signal HUP --quiet --pidfile \${PIDFILE} --exec \${DAEMON} || true
		echo "\${NAME}."
		;;

	configtest|testconfig)
		echo -n "Testing \${DESC} configuration: "
		if test_nginx_config; then
			echo "\${NAME}."
		else
			exit \${?}
		fi
		;;

	status)
		status_of_proc -p \${PIDFILE} "\${DAEMON}" nginx && exit 0 || exit $?
		;;
	*)
		echo "Usage: \${NAME} {start|stop|restart|reload|force-reload|status|configtest}" >&2
		exit 1
		;;
esac
exit 0
EOF

sudo chmod 0755 /etc/init.d/nginx
cd /etc/init.d
sudo update-rc.d nginx defaults >> ${LOG} 2>&1

## Nginx log rotation

sudo bash -c "cat > /etc/logrotate.d/nginx" <<EOF
/var/log/nginx/*.log {
        daily
        missingok
        rotate 5
        compress
        delaycompress
        notifempty
        create 0640 www-data adm
        sharedscripts
        prerotate
                if [ -d /etc/logrotate.d/httpd-prerotate ]; then
                    run-parts /etc/logrotate.d/httpd-prerotate;
                fi;
        endscript
        postrotate
                [ ! -f /var/run/nginx.pid ] || kill -USR1 `cat /var/run/nginx.pid`
        endscript
}
EOF

## Configure nginx for wordpress
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.org

sudo bash -c "cat > /etc/nginx/nginx.conf" <<EOF
user                www-data;
worker_processes    2;
pid                 /var/run/nginx.pid;

events {
  worker_connections 1024;
  multi_accept off;
}

http {

    # The server setting might have to be change depending
    # on what the php5-fpm is configured to expose
    upstream php {
        server 127.0.0.1:9000;
        server unix:/var/run/php5-fpm.sock;
    }

    include mime.types;

    include conf.d/*.conf;
    include sites-enabled/*;
}
EOF

sudo mkdir -p /etc/nginx/sites-enabled
sudo bash -c "cat > /etc/nginx/sites-enabled/default.conf" <<EOF

server {

        ##
        listen 80;
        server_name www.dev-foocafe.org;

        ## Your only path reference.
        root /var/www/wordpress;

        index index.php index.html;
#        try_files \$uri \$uri/ /index.php?q=\$uri;

        location ~* \.(js|css|png|jpg|jpeg|gif|ico)\$ {
                expires max;
                log_not_found off;
        }

        location / {
                try_files \$uri \$uri/ /index.php?\$args;
        }

        location ~ \.php\$ {
                include fastcgi.conf;
                fastcgi_intercept_errors on;
                fastcgi_pass php;
        }
}
EOF

## Mark as provisioned
CURRENT_DATE=`date +%Y-%m-%dT%H:%M:%S`
sudo bash -c "echo ${CURRENT_DATE} >> ${MARKER}"
