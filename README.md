# web-application-with-docker
deploy web application with docker and other open source components


该项目基于django+restframework+postgresql，目前支持客户端简单的get和post请求。业务部署在两个容器中，一个是以python为基础镜像，
又在该容器中通过pip install的方式安装了django和restframework；pg数据库部署在一个单独的容器中。客户端使用了jquery和bootstrap。

部署步骤：

1  安装docker和docker-compose，docker pull python/postgresql拉取python和postgresql两个镜像。

2  安装django，django-admin startproject mysite启动一个项目，完成代码的编写。

3  编写Dockerfile和yaml文件，其中Dockerfile是为了在python基础镜像上再构建新的镜像，yaml文件是将两个镜像组合成一个完整的web应用。

4  docker-compose up启动应用，访问客户端。


docker简介:

相比于传统的在虚机上部署业务，docker的优势就是轻量级，比如上面提到的python基础镜像只有几十m，部署完整个业务可能只有不到1G的大小。
传统的虚机中，即使只部署一个很小的业务，也需要一个完整的操作系统。即使基础镜像为centos这种，也会比真正的centos操作系统小很多。
轻量级就会使启动速度变快。

在开发环境构建好docker镜像之后，生产环境直接pull下来就可以直接使用，不需要其它配置。比如你创建好镜像之后，别人想用这个镜像，那么他直接
pull下来然后执行一行docker run命令就可以了，因为你的代码(通过add或者copy的方式)和依赖的包(通过pip install的方式)都在镜像中了。

restframework简介:

首先介绍下rest，rest是一种规范，一种面向资源的url设计规范。比如本例中的接口为/musics（rest中一般为复数形式），get/post/update/delete方法
都是调同一接口，区别是方法。在musics/views.py中通过类视图MusicView，分别复写get方法和post方法来完成客户端的get和post请求。

已经使用nginx和uwsgi拉起服务。

本周目标：

完成一个免费天气API的业务，由于现在免费的气象API都有调用次数的限制（每天），所以计划将查询到的天气放在数据库中，如果对天气预报时间要求不是
很高的话，可以从本API中获取到。
