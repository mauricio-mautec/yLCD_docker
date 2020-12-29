FROM nginx
ENV HOME=/app
WORKDIR ${HOME}

RUN apt-get update && apt-get install -y supervisor uwsgi sqlite3 python3 python3-pip procps vim htop lsof cron rsyslog && \
    rm /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY nginx.conf /etc/nginx/nginx.conf
COPY uwsgi.ini /app/uwsgi.ini
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /app/entrypoint.sh
COPY yLCD.cron /var/spool/cron/crontabs/root
COPY app/yLCD /app/yLCD

RUN mkdir -p /spool/nginx /run/pid && \
    chmod -R 777    /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chgrp -R  0     /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX  /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    rm /etc/nginx/conf.d/default.conf

RUN touch /var/log/supervisor/supervisord.log

RUN ln -s /usr/local/bin /app/bin && \
    ln -s /usr/local/lib /app/lib

RUN chmod -R 0600 /var/spool/cron/crontabs/root && \
    sed -i '/cron/s/^#//g' /etc/rsyslog.conf

#	# https://github.com/moby/moby/issues/31243#issuecomment-406879017
#	RUN ln -s      /usr/local/bin/entrypoint.sh / && \ 
#	    chmod 777  /usr/local/bin/entrypoint.sh && \
#	    chgrp -R 0 /usr/local/bin/entrypoint.sh && \
#	    chown -R   nginx:root /usr/local/bin/entrypoint.sh
#
#	# https://docs.openshift.com/container-platform/3.3/creating_images/guidelines.html
#	RUN chgrp -R 0     /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
#	    chmod -R g+rwX /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
#  	    chown -R nginx:root /app && \
# 	    chmod -R 777 /app /etc/passwd
 
 
EXPOSE 8080:8080
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["supervisord"]

