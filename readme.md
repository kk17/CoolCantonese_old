#粤讲粤酷微信公众号工程
![粤讲粤酷](data/qrcode.jpg)


##配置
参考configs目录下的`env.cfg.example`和`redis.cfg.example`文件生成`env.cfg`和`redis.cfg`

##部署：
##使用docker部署
需要安装docker和fig，然后在工程目录下运行`sudo fig up`

##本机部署：
###安装Redis
[参考][1]
配置：
redis.conf
requirepass h~||..-9Y3|r5|BqZJD=;B+G+Yj58j_S

```
[9005] 08 Feb 15:48:20.704 # Server started, Redis version 2.8.9
[9005] 08 Feb 15:48:20.704 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.[9005] 08 Feb 15:48:20.705 * The server is now ready to accept connections on port 6379
```

###nginx:

```
server {
    server_name _;
    listen 9090;
    root /home/kk17/Cantonese_audio/words_audio;
    
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

deb http://ppa.launchpad.net/hgneng/ekho/ubuntu precise main 

[Ekho(余音) - 中文语音合成软件(支持粤语、普通话)](http://www.eguidedog.net/cn/ekho_cn.php)
[Howto add PPA in debian](https://blog.anantshri.info/howto-add-ppa-in-debian/)

[1]:https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
[2]:http://xvfeng.me/posts/Nginx-for-developers/

##测试
推荐使用[ushuz/weixin-simulator](https://github.com/ushuz/weixin-simulator)进行测试
