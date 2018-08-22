FROM public-docker-virtual.artnj.zte.com.cn/nginx
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/sites-available/
COPY musics_nginx.conf /etc/nginx/sites-available/
RUN mkdir -p /etc/nginx/sites-enable/\
    && ln -s /etc/nginx/sites-available/musics_nginx.conf /etc/nginx/sites-enabled/
CMD ["nginx", "-g", "deamon off;"]