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

wechat nginx config:

```
server {
    server_name _;
    listen 80;

    location /wechat {
        #proxy_pass_header Server;
        proxy_redirect off;
    #Proxy Settings
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_max_temp_file_size 0;
        proxy_connect_timeout      90;
        proxy_send_timeout         90;
        proxy_read_timeout         90;
        proxy_buffer_size          4k;
        proxy_buffers              4 32k;
        proxy_busy_buffers_size    64k;
        proxy_temp_file_write_size 64k;
        proxy_pass http://127.0.0.1:8888;
        access_log /var/log/wechat.kkee.tk_access.log;
    }
}
```


```
nginx -s reload

```
[参考][2]

##supervsor

```
echo_supervisord_conf > /etc/supervisord.conf

echo_supervisord_conf > .local/etc/supervisord.conf

[include]
files = /etc/supervisor/*.ini
```


[1]:https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
[2]:http://xvfeng.me/posts/Nginx-for-developers/