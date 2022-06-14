#!/usr/bin/env bash
# sets up a data directory for serving releases and tests
apt-get update
apt-get install -y --no-upgrade nginx
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo 'testing nginx config...' > /data/web_static/releases/test/index.html
ln -s -f /data/web_static/releases/test/ /data/web_static/current
chown -fhR ubuntu:ubuntu /data/

LINE=$(grep -Eno "^\s*location / {" /etc/nginx/sites-available/default | cut -d : -f 1)

EXIST=$(grep -Eco "^\s*location /hbnb_static {" /etc/nginx/sites-available/default)

LOCATION_CONFIG="\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n"

if [ "$EXIST" -le 0 ]
then
    sudo sed -i "$LINE i\ $LOCATION_CONFIG"  /etc/nginx/sites-available/default
fi
service nginx restart
