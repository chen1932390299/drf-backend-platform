# drf-backend-platform
python version 3.6.6
depend on requirements.txt


# 组件
mysql8
redis
nginx
python3.6.6
Django 3.2.2
django-rest-framework 3.12.1

# 依赖需要安装docker-compose，docker
docker安装教程：https://www.runoob.com/docker/centos-docker-install.html
docker-compose安装教程：https://www.runoob.com/docker/docker-compose.html

# 关于部署(先进入docker-compose.yml所在目录)
docker-compose build
docker-compose up -d 或者 docker-compose

# 常用docker-compose启停命令
docker-compose restart/stop/up

# 验证服务测试，打开chrome：
输入${your_server_ip}:80/swagger-mysite/ 可以看到swagger 文档表示ok

正常启动compose日志

            へ　　　　　／|
        　　/＼7　　　 ∠＿/
        　 /　│　　 ／　／
        　│　Z ＿,＜　／　　 /`ヽ
        　│　　　　　ヽ　　 /　　〉
        　 Y　　　　　`　 /　　/
        　ｲ●　､　●　　⊂⊃〈　　/
        　()　 へ　　　　|　＼〈
        　　>ｰ ､_　 ィ　 │ ／／
        　 / へ　　 /　ﾉ＜| ＼＼
        　 ヽ_ﾉ　　(_／　 │／／
        　　7　　　　　　　|／
        　　＞―r￣￣`ｰ―＿
ookie    | No changes detected
rookie    | Operations to perform:
rookie    |   Apply all migrations: admin, auth, contenttypes, django_apscheduler, mysite, sessions
rookie    | Running migrations:
rookie    |   No migrations to apply.
rookie    | [uWSGI] getting INI configuration from uwsgi.ini
rookie    | *** Starting uWSGI 2.0.19.1 (64bit) on [Thu Jul  1 08:15:30 2021] ***
rookie    | compiled with version: 6.3.0 20170516 on 01 July 2021 07:21:24
rookie    | os: Linux-3.10.0-1127.8.2.el7.x86_64 #1 SMP Tue May 12 16:57:42 UTC 2020
rookie    | nodename: rookie
rookie    | machine: x86_64
rookie    | clock source: unix
rookie    | pcre jit disabled
rookie    | detected number of CPU cores: 4
rookie    | current working directory: /code/rookie
rookie    | writing pidfile to uwsgi.pid
rookie    | detected binary path: /usr/local/bin/uwsgi
rookie    | *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***
rookie    | chdir() to /code/rookie
rookie    | limiting address space of processes...
rookie    | your process address space limit is 6341787648 bytes (6048 MB)
rookie    | your memory page size is 4096 bytes
rookie    |  *** WARNING: you have enabled harakiri without post buffering. Slow upload could be rejected on post-unbuffered webservers ***
rookie    | detected max file descriptor number: 1048576
rookie    | lock engine: pthread robust mutexes
rookie    | thunder lock: disabled (you can enable it with --thunder-lock)
rookie    | uwsgi socket 0 bound to TCP address :8000 fd 3
rookie    | *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***
rookie    | Python version: 3.6.6 (default, Oct 16 2018, 07:17:20)  [GCC 6.3.0 20170516]
rookie    | Python main interpreter initialized at 0x558a7623fdf0
rookie    | *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***
rookie    | python threads support enabled
rookie    | your server socket listen backlog is limited to 100 connections
rookie    | your mercy for graceful operations on workers is 60 seconds
rookie    | mapped 1031270 bytes (1007 KB) for 8 cores
rookie    | *** Operational MODE: preforking+threaded ***
rookie    | WSGI app 0 (mountpoint='') ready in 2 seconds on interpreter 0x558a7623fdf0 pid: 12 (default app)
rookie    | mountpoint  already configured. skip.
rookie    | *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***
rookie    | *** uWSGI is running in multiple interpreter mode ***
rookie    | spawned uWSGI master process (pid: 12)
rookie    | spawned uWSGI worker 1 (pid: 14, cores: 2)
rookie    | spawned uWSGI worker 2 (pid: 16, cores: 2)
rookie    | spawned uWSGI worker 3 (pid: 18, cores: 2)
rookie    | spawned uWSGI worker 4 (pid: 20, cores: 2)



# 常见问题
1.关于mysql5.7支持中文乱码问题导致django.db.utils.OperationalError: (1067, "Invalid default value for 'project_name'")
需要添加 command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
services:
  mysql:
    image: mysql:5.7
    container_name: mysql   # settings 的HOST 填写的是容器的名称
    hostname: mysql
    restart: always
    volumes:
      - ./mysql:/var/lib/mysql  # 把当前文件夹下的 ./mysql文件夹挂载到docker容器 /var/lib/mysql 路径下,会自动创建
    ports:
      - "3306:3306"
    environment:
      - MYSQL_HOST=db
      - MYSQL_ROOT_PASSWORD=App@123456
      - MYSQL_DATABASE=drf_backend
      - MYSQL_USER=App
      - MYSQL_PASSWORD=App@123456
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

2. mysqlclient 安装如果报错请安装：
yum install mysql-devel -y

3.uwsgi.ini
也支持.sock形式部署：
socket = /code/rookie/script/uwsgi.sock

nginx配置

http {
    include       mime.types;
    default_type  application/octet-stream;



    sendfile        on;

    keepalive_timeout  65;

    upstream django {
        server unix:/code/rookie/script/uwsgi.sock;
    }

    server {
        listen       80;
        server_name  localhost;



        location / {
            uwsgi_pass django;
            include /etc/nginx/uwsgi_params;
        }
        location /static {
           alias /code/rookie/static/;
	}


    }


# 关于docker-compose :
docker-compose up 本质是docker-compose logs -f，它会收集所有容器的日志输出直到退出命令，或者容器都停止运行。
docker-compose up -d 以后台的方式运行容器。不会在终端上打印运行日志

[root@hadoop drf-backend-platform]# docker-compose --help
Define and run multi-container applications with Docker.

Usage:
  docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]
  docker-compose -h|--help

Options:
  -f, --file FILE             Specify an alternate compose file
                              (default: docker-compose.yml)
  -p, --project-name NAME     Specify an alternate project name
                              (default: directory name)
  --verbose                   Show more output
  --log-level LEVEL           Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  --no-ansi                   Do not print ANSI control characters
  -v, --version               Print version and exit
  -H, --host HOST             Daemon socket to connect to

  --tls                       Use TLS; implied by --tlsverify
  --tlscacert CA_PATH         Trust certs signed only by this CA
  --tlscert CLIENT_CERT_PATH  Path to TLS certificate file
  --tlskey TLS_KEY_PATH       Path to TLS key file
  --tlsverify                 Use TLS and verify the remote
  --skip-hostname-check       Don't check the daemon's hostname against the
                              name specified in the client certificate
  --project-directory PATH    Specify an alternate working directory
                              (default: the path of the Compose file)
  --compatibility             If set, Compose will attempt to convert keys
                              in v3 files to their non-Swarm equivalent

Commands:
  build              Build or rebuild services
  bundle             Generate a Docker bundle from the Compose file
  config             Validate and view the Compose file
  create             Create services
  down               Stop and remove containers, networks, images, and volumes
  events             Receive real time events from containers
  exec               Execute a command in a running container
  help               Get help on a command
  images             List images
  kill               Kill containers
  logs               View output from containers
  pause              Pause services
  port               Print the public port for a port binding
  ps                 List containers
  pull               Pull service images
  push               Push service images
  restart            Restart services
  rm                 Remove stopped containers
  run                Run a one-off command
  scale              Set number of containers for a service
  start              Start services
  stop               Stop services
  top                Display the running processes
  unpause            Unpause services
  up                 Create and start containers
  version            Show the Docker-Compose version information




