# syntax=docker/dockerfile:1
FROM nginx


COPY default.conf /etc/nginx/conf.d/
COPY index.html /usr/share/nginx/html/


CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
