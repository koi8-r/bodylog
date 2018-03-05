#!/bin/bash

echo "set \$web_domain = $([ -z "${WEB_DOMAIN}" ] && echo "local" || echo "${WEB_DOMAIN}") ;" \
  > /etc/nginx/web_domain.conf

exec "$@" ;
