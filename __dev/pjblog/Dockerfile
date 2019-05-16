FROM centos:7

ENV PHP_VERSION 7.2.3
ENV NODE_VERSION 8.11.3
ENV WORKDIR /root/

RUN yum install gcc libxml2 libxml2-devel make gcc-c++ \
libjpeg libpng-devel freetype freetype-devel pcre pcre-devel libxslt libxslt-devel \
  openssl openssl-devel bzip2-devel.x86_64 bison libcurl libcurl-devel -y

RUN cd /usr/src && wget http://cn2.php.net/distributions/php-${PHP_VERSION}.tar.gz && \
 tar -xzxvf php-${PHP_VERSION}.tar.gz && cd php-${PHP_VERSION} && \
 ./configure \
 --prefix=/usr/local/php \
 --with-curl \
 --with-freetype-dir \
 --with-gd \
 --with-gettext \
 --with-iconv-dir \
 --with-kerberos \
 --with-libdir=lib64 \
 --with-libxml-dir \
 --with-mysqli \
 --with-openssl \
 --with-pcre-regex \
 --with-pdo-mysql \
 --with-pdo-sqlite \
 --with-pear \
 --with-png-dir \
 --with-jpeg-dir \
 --with-xmlrpc \
 --with-xsl \
 --with-zlib \
 --with-bz2 \
 --with-mhash \
 --enable-fpm \
 --enable-bcmath \
 --enable-libxml \
 --enable-inline-optimization \
 --enable-mbregex \
 --enable-mbstring \
 --enable-opcache \
 --enable-pcntl \
 --enable-shmop \
 --enable-soap \
 --enable-sockets \
 --enable-sysvsem \
 --enable-sysvshm \
 --enable-xml \
 --enable-zip && make && make install

# 安装 composer
RUN cd /usr/local/src/ && php -r "copy('https://install.phpcomposer.com/installer', 'composer-setup.php');" && \
php composer-setup.php && php -r "unlink('composer-setup.php');" && ln -sn /usr/local/src/composer.phar /usr/bin/composer

## 修复常见的composer版本不兼容错误
#RUN composer install --ignore-platform-reqs

# 编译安装Node
RUN cd /usr/local/src/ && wget https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}.tar.gz \
&& tar zxvf node-v${NODE_VERSION}.tar.gz && cd node-v${NODE_VERSION} && ./configure --prefix=/usr/local/node && make && make install

RUN ln -sn /usr/local/node/bin/node /usr/bin/node
RUN ln -sn /usr/local/node/bin/npm /usr/bin/npm



RUN cd ${WORKDIR} && git clone https://github.com/premepen/blog && cd ${WORKDIR}/blog \
&& composer install -vvv && npm install && npm run dev && php artisan blog:install

## 错误处理 syslink错误 https://stackoverflow.com/questions/47409417/storage-in-laravel-says-symlink-no-such-file
# RUN cd ${WORKDIR}/blog && rm public/storage && artisan storage:link

USER root
