cd /opt/CacheServer
git pull

cd /opt/CacheServerWeb
git pull

cd /opt/CacheServer/src
python3 server.py 2>/var/log/serverCache.log &
gunicorn -w 4 -b 127.0.0.1:8000 api:api 2>/var/log/serverCacheApi.err 1>&2 &
/usr/sbin/service nginx start
