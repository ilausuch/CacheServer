cd /opt/CacheServer/src
python3 server.py 2>/var/log/serverCache.err &
gunicorn -w 4 -b 127.0.0.1:8000 api:api api:api 2>/var/log/serverCacheApi.err >/var/log/serverCacheApi.log &
/usr/sbin/service nginx start
