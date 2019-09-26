Usage:
* nginx_web_new.py <hostname> <ip address> <action>
* status
```
$ ./nginx_web_new.py  someserver.domain.com 192.168.1.224 status
name: someserver.domain.com state: up

name: someserver.domain.com state: draining
```

* drain
```
./nginx_web_new.py  someserver.domain.com 192.168.1.224 drain
someserver.domain.com is draining in the pool beta_web
```

* up
```
./nginx_web_new.py  someserver.domain.com 192.168.1.224 up
someserver.domain.com is back in the pool beta_web
```
