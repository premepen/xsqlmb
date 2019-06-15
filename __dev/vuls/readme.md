# docker-vuls教程

[docker-vuls](https://vuls.io/docs/en/tutorial-docker.html)


## Fetch NVD
```bash
for i in `seq 2002 2020`; do \
    docker run --rm -it \
    -v $PWD:/vuls \
    -v $PWD/go-cve-dictionary-log:/var/log/vuls \
    vuls/go-cve-dictionary fetchnvd -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true"  -years $i ; \
  done
```
```bash
for i in `seq 2002 2020`; do go-cve-dictionary fetchnvd -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" -years $i ; done
```

## Fetch oval
```bash
docker run --rm -it \
    -v $PWD:/vuls \
    -v $PWD/goval-dictionary-log:/var/log/vuls \
    vuls/goval-dictionary fetch-redhat -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" \ 
       5 6 7 
```

```bash
goval-dictionary fetch-redhat -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" 5 6 7 
## 下面的无视
goval-dictionary fetch-amazon -dbtype mysql -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" 
goval-dictionary  fetch-alpine -dbtype mysql -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true"  3.3 3.4 3.5 3.6
goval-dictionary fetch-oracle -dbtype mysql -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true"  
goval-dictionary fetch-ubuntu  -dbtype mysql -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" 12 14 16 18
goval-dictionary  fetch-debian -dbtype mysql -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true"   7 8 9 10
   
 
```

## fetch gost
```bash
docker run --rm -i \
    -v $PWD:/vuls \
    -v $PWD/goval-log:/var/log/gost \
    vuls/gost fetch -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" \ 
      redhat
```
```bash
gost fetch  -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" redhat --after 2016-01-01   

gost fetch debian -dbtype mysql \
      -dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true"  

```

## fetch go-exploit
```bash
go-exploitdb fetch -dbtype mysql \ 
-dbpath "root:1q2w3e4R@(192.168.2.223:3306)/vuls?parseTime=true" exploitdb -deep
```
