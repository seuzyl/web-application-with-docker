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

什么是uWSGI?讲下CGI/FastCGI/uWSGI/uwsgi/WSGI的历史：

1、什么是CGI
最开始的web服务器只能返回静态页面，1000个人访问同一个API得到的html是一样的。
CGI:commom gateway interface通用网关接口，commom有两层含义：一是CGI脚本可以运行在任何支持CGI的服务器上，而是CGI脚本可以是任何语言编写的，python/java/php等。
CGI脚本需要放在特定的目录下，使用特定的文件扩展名，并设置为可以执行。
例如使用Apache服务器（使用CGI协议），通过修改设置改变CGI脚本的目录为ScriptAlias/webpath/usr/local/cgi，就可以通过http://localhost/webpath/script.cgi，来访问（执行）/usr/local/cgi/script.cgi这个脚本。当然了，Apache也支持uwsgi协议。
CGI可以通过环境变量获取参数，也可以通过get/post请求接收客户端参数（使用cgi.FieldStorage类），返回动态的html页面。
与uWSGI服务器不同的是，CGI脚本返回的是html页面，而不是httpresponse。
CGI的方式是每个请求起一个进程执行一个CGI脚本，实现方式比较简单，但是高并发的时候要创建/销毁大量的进程（假设创建+销毁进程的时间和进程运行时间如果是1:1，会浪费多少时间），性能会降低。

2、怎么样能快点
为了解决这个问题，FastCGI出现了：在服务器内嵌入FastCGI进程管理器，进程管理器会启动多个CGI解释器进程并等待来自服务器的连接，CGI脚本只在服务器进程初始化的时候载入一次，数据库连接也是。并一直保持直到web服务器关闭。CGI解释器进程返回响应之后并不销毁（FastCGI进程也不会销毁），继续等待下一个连接（CGI在这一步就销毁了）。FastCGI已经是上世纪90年代的东东了。

3、当代服务器
uwsgi/uWSGI/WSGI（有关组织起名能认真点吗）
WSGI：发音为wiz-gee，全称Web Server Gateway Interface，解决的是web服务器和python应用之间（比如django）如何交互的。基本思想是python应用返回一个可调用对象（方法或实现了__call__的类），以django为例说明一下。
查看app目录下wsgi.py文件，可以看到application = get_wsgi_application()，这个函数返回的是一个WSGIHandler实例，这个类中实现了__call__方法__call__(self, environ, start_response)，入参为environ和start_response，其中environ是一个字典，包括request data（方法、端口、header、query string等）、操作系统环境变量、WSGI变量（版本号、线程/进程数据）。这两个入参是uWSGI服务器传给django的。start_response下面还会有return response（实际上这个response是一个可迭代对象），start_response中的入参只有状态码和响应头，为什么不在start_response里直接将response传进去？对于简单的响应，返回的响应是一个只包含一个元素的迭代器，但是当响应比较大的时候，这样并不可行（response为一个单元素迭代器），uWSGI需要将大的响应变为小的。stackoverfolw上还有个回答：One of the primary reasons was to allow a server to return a write() callable to support existing Python web applications that were used to being able to call a write() function to produce content. This saved them from being rewritten to return an iterable. 例子如下：
def application(environ, start_response):
    write = start_response(status, headers)
    write('content block 1')
    write('content block 2')
    write('content block 3')
    return None

def application(environ, start_response):
    start_response(status, headers)
    return ['content block 1',
            'content block 2',
            'content block 3']
这两种返回方式是一样的。

uWSGI是实现了WSGI接口的web服务器。

uwsgi是uWSGI服务器连接到其它应用的协议，一般用来uWSGI服务器连接nginx服务器，uwsgi协议是nginx和uWSGI服务器如何交互的。
数据从客户端到Python app的数据流向应该是：client-->nginx-->uWSGI-->Django，响应按照相反的顺序返回。

本周目标：

完成一个免费天气API的业务，由于现在免费的气象API都有调用次数的限制（每天），所以计划将查询到的天气放在数据库中，如果对天气预报时间要求不是
很高的话，可以从本API中获取到。
