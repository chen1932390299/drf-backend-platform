#### 1.depends on

* django

* python  3.6.6

* django rest framework


#### 2.components
* mysql8.x
* redis
* nginx
#### 3.before deploy  need prepare
###### install docker:
[https://www.runoob.com/docker/centos-docker-install.html](https://www.runoob.com/docker/centos-docker-install.html)


* * *
###### install docker-compose:
[https://www.runoob.com/docker/docker-compose.html](https://www.runoob.com/docker/docker-compose.html)


#### 4. deploy (execute  at docker-compose.yml dir )
docker-compose build

docker-compose up -d 或者 docker-compose

#### 5.validate deploy
* open chrome and input following format and enter :
 ${your_server_ip}:80/swagger-mysite/

* you will see like this represent you success :

* * *

* ![3f0f02b4f9c4413943335189b64dd52a.png](en-resource://database/605:1)


* * *
#### 6.docker-compose start log

* rookie    | spawned uWSGI master process (pid: 12)
* rookie    | spawned uWSGI worker 1 (pid: 14, cores: 2)
* rookie    | spawned uWSGI worker 2 (pid: 16, cores: 2)
* rookie    | spawned uWSGI worker 3 (pid: 18, cores: 2)
* rookie    | spawned uWSGI worker 4 (pid: 20, cores: 2)
#### 7.frequently asked question (FAQ):
###### 1.django.db.utils.OperationalError: (1067, "Invalid default value for 'project_name'")



*  solution:

     config command with --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci


* * *



    services: 
        mysql:   
            image: mysql:5.7   
            container_name: mysql  
            hostname: mysql   
            restart: always   
            volumes:     
                - ./mysql:/var/lib/mysql 
            ports:     
                - "3306:3306"   
           environment:     
                - MYSQL_HOST=db     
                - MYSQL_ROOT_PASSWORD=App@123456     
                - MYSQL_DATABASE=drf_backend     
                - MYSQL_USER=App     
                - MYSQL_PASSWORD=App@123456   
                command:
                    --character-set-server=utf8mb4
                    --collation-server=utf8mb4_unicode_ci


* * *





2. ###### mysqlclient  install failed ：
    solution： yum install mysql-devel -y

3. ###### about docker-compose :

* docker-compose up 本质是docker-compose logs -f，它会收集所有容器的日志输出直到退出命令，或者容器都停止运行

* docker-compose up -d 以后台的方式运行容器。不会在终端上打印运行日志



4. ###### more about docker-compose usage you can see by :



*    docker-compose --help






5. ###### python web server restart or shutdown :
* docker-compose restart/stop/up

* * *
#####  more issue support please contact with  us :
QQ Group: 796245415

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























