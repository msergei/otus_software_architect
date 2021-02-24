FROM nginx:alpine

COPY ./nginx/headers.conf /etc/nginx/
COPY ./nginx/nginx.conf /etc/nginx/
COPY ./nginx/proxy.conf /etc/nginx/

COPY ./nginx/services.conf /etc/nginx/conf.d/default.conf
