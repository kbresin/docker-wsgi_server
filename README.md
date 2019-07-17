# docker-wsgi_server
A Dockerfile for a minimal apache wsgi_server running on port 8000 with no root perms.

Meant to be called like:

sudo docker run -d -p 127.0.0.1:8000:8000 -v /var/log/docker_containers/wsgi_server:/var/log/httpd apache_wsgi
