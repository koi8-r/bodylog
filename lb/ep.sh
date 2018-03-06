#!/bin/bash


domain="`[[ -z "${WEB_DOMAIN}" ]] && echo "local" || echo "${WEB_DOMAIN}"`"
mkdir -p /etc/nginx/vhost.d/

for name in www api ; do
if [[ "$name" == "www" ]]; then
    default_server="default_server" ;
    service_port="80" ;
else
    default_server="" ;
    service_port="8080" ;
fi
cat <<EOF > "/etc/nginx/vhost.d/${name}.conf"
server {
    listen 80 ${default_server} ;
    server_name ${name}.${domain} ;
    access_log /var/log/nginx/${name}-access.log main ;
    error_log /var/log/nginx/${name}-error.log crit ;

    location / {
        proxy_pass http://${name}:${service_port}/ ;
    }

    location /api/ {
        proxy_pass http://api:8080/ ;
        proxy_redirect off ;
        # proxy_set_header Host \$host ;
        # proxy_set_header X-Real-IP \$remote_addr ;
        # proxy_set_header X-Forwarded-Host \$server_name ;
        # proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for ;
        # proxy_set_header X-Forwarded-Proto \$scheme ;
        # proxy_http_version 1.1 ;
        # proxy_set_header Connection "" ;
        # proxy_buffering off ;
        # proxy_redirect http:// https:// ;
        # proxy_pass_header Set-Cookie ;
    }
}
EOF
done


exec "$@" ;
