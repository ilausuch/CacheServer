cd /opt/CacheServer/src
python3 server.py 2>/var/log/serverCache.log &
gunicorn -w 4 api:api 2>&1 >/var/log/serverCacheApi.log &
/usr/sbin/service nginx start
