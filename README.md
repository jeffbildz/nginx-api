Usage:
* nginx_web_new.py hostname ip_address action upstream
* status
```
$ ./nginx_web_new.py  someserver.domain.com 192.168.1.224 status web_pool
name: someserver.domain.com state: up

name: someserver.domain.com state: draining
```

* drain
```
./nginx_web_new.py  someserver.domain.com 192.168.1.224 drain web_pool
someserver.domain.com is draining in the pool web_pool
```

* up
```
./nginx_web_new.py  someserver.domain.com 192.168.1.224 up web_pool
someserver.domain.com is back in the pool web_pool
```
