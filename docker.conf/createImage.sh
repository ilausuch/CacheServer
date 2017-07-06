docker build -t server_cache:beta1 . && docker rm -f serverCache && docker run --name serverCache -di -p 8080:80 server_cache:beta1
