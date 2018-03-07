- initdb send to (`postgres --boot -x1 -F -d 5`) stdin data like `postgres.bki` or `echo ALTER USER ...`
- apt-get install -o APT::Immediate-Configure=false --no-install-recommends -qy postgresql
- apt-get download <package>

  dpkg --unpack <package>*.deb
  
  rm /var/lib/dpkg/info/<package>.postinst -f
  
  dpkg --configure <package>
  
  apt-get install -f -y
- `pg_createcluster 10 main -o listen_addresses '*' -- -W -U postgres`
