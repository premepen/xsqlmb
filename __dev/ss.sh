#!/bin/bash

yum -y install vim python-pip
pip install shadowsocks

systemctl stop firewalld
systemctl disable firewalld

cat > /etc/shadowsocks.json << EOF

{
    "server":"0.0.0.0",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "port_password":{
        "1111":"password1",
        "1112":"password2",
        "1113":"password3"
    },
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
}

EOF

ssserver -c /etc/shadowsocks.json
