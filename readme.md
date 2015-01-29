##部署：

###安装Redis
[参考][1]
配置：
redis.conf
requirepass h~||..-9Y3|r5|BqZJD=;B+G+Yj58j_S

###nginx:
```
server {
    server_name _;
    listen 9090;
    root /home/kk17/Cantonese/words_audio;
    
    location ~* \.(gif|jpg|png|mp3)$ {
    expires 30d;
    }   
}
```

```
nginx -s reload
```
[参考][2]

##supervsor



[1]:https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
[2]:http://xvfeng.me/posts/Nginx-for-developers/