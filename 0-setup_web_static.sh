#!/usr/bin/env bash
apt-get update
apt-get install -y --no-upgrade nginx
mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo 'testing nginx config...' > /data/web_static/releases/test/index.html
ln -s -f /data/web_static/releases/test/ /data/web_static/current
chown -fhR ubuntu:ubuntu /data/
sudo sed -i -r 's|^(\s*)(location / \{)|\1location /hbnb_static {\n\1\1alias /data/web_static/current;\n\1\}\n\n\1\2|' /etc/nginx/sites-available/default
service nginx restart
