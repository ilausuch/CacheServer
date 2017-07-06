FROM nginx:latest

RUN \
    apt-get update && \
    apt-get -y install nano python3 python3-pip git procps

RUN pip3 install eventlet gunicorn falcon falcon_cors requests
RUN git clone https://github.com/ilausuch/CacheServer.git /opt/CacheServer
RUN git clone https://github.com/ilausuch/CacheServer-Admin.git /opt/CacheServerWeb

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY start.sh /opt/start.sh

RUN chmod a+x /opt/start.sh
CMD /opt/start.sh && bash

EXPOSE 80
