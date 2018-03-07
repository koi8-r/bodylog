- ```apt-key adv --keyserver ipv4.pool.sks-keyservers.net --recv-keys $KEY
     export KEY=<KEY> GNUPGHOME="$(mktemp -d)" && \
     ( gpg --keyserver ipv4.pool.sks-keyservers.net --recv-keys "$KEY" && \
       gpg --export "$KEY" > /etc/apt/trusted.gpg.d/apt.package.org.gpg ) ; \
     rm -rf "$GNUPGHOME"
  ```
