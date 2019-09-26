Usage:
* nginx_web_new.py hostname ip_address action upstream
* status
```
$ ./main.py  someserver.domain.com 192.168.1.224 status web_pool
name: someserver.domain.com state: up

name: someserver.domain.com state: draining
```

* drain
```
./main.py  someserver.domain.com 192.168.1.224 drain web_pool
someserver.domain.com is draining in the pool web_pool
```

* up
```
./main.py  someserver.domain.com 192.168.1.224 up web_pool
someserver.domain.com is back in the pool web_pool
```
