FROM centos
MAINTAINER kyle+git@101010.org
RUN /usr/bin/yum -y install mod_wsgi.x86_64
#RUN /bin/sed -i 's/^Listen 80$/Listen 8000/' /etc/httpd/conf/httpd.conf
RUN /bin/rm -f /etc/httpd/conf.modules.d/00-dav.conf /etc/httpd/conf.modules.d/00-lua.conf /etc/httpd/conf.modules.d/00-proxy.conf /etc/httpd/conf.modules.d/01-cgi.conf /etc/httpd/conf.modules.d/00-base.conf
RUN /bin/rm -f /etc/httpd/conf.d/*
RUN chmod 770 /run/httpd
ADD ./httpd.conf /etc/httpd/conf/httpd.conf
ADD ./00-minimal.conf /etc/httpd/conf.modules.d/00-base.conf
ADD ./hw-wsgi.conf /etc/httpd/conf.d/hw-wsgi.conf
ADD ./hw.wsgi /app/hw.wsgi
USER apache
ENTRYPOINT ["/usr/sbin/httpd", "-DFOREGROUND"]
