# 安装说明：
## 自动安装(仅仅centos7)：
```
wget -O install.sh https://raw.githubusercontent.com/anthonydeng2000/94imm/master/install.sh && chmod +x install.sh &&./install.sh
```
安装过程中需要输入
```
> * allow url:www.94imm.com   # 防盗链允许的使用的域名
> * site_name:94imm   # 网站名称，将显示在网站底部网站title和底部
> * site_url:www.94imm.com   # 网站url
> * Create databases:94imm   # 添加数据库
> * Create databases password:   # 数据库账号(root)如未安装mysql，此处将设置为root密码
> * Password for root:   # 如本机以安装mysql，此处需输入root密码
```
参数配置
> 配置文件为根目录下的config.py
```python
# 数据库信息，一键脚本自动添加
mysql_config = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '94imm',
        'USER': '94imm',
        'PASSWORD': '94imm',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
# 数组形式，可以添加多个域名。如使用反代，此处必须添加127地址，否则400
allow_url=["www.94imm.com","94imm.com","127.0.0.1"]
# 缓存超时时间，服务器性能好可缩短此时
cache_time=300
# 使用的模板（暂时开放一个）
templates="zde"
# 网站名
site_name="94iMM"
# 一键脚本自动添加
site_url = "https://www.94imm.com"
# 网站关键词
key_word = "关键词1,关键词2,关键词3"
# 网站说明
description = "这是一个高质量的自动爬虫"
# 底部联系邮箱
email = "admin@94imm.com"
# 网站调试模式
debug = False
# 页面底部友情链接
friendly_link = [{"name":"94imm","link":"https://www.94imm.com"},{"name":"获取源码","link":"https://github.com/Turnright-git/94imm.git"}]
# 远程图片地址,如"https://img.94imm.com","/为使用本地文件".
img_host = "/"
```

使用说明
> 进入项目根目录
```shell
启动网站
./start s
关闭网站
./start stop
重启网站
./start r
清空网站缓存（使所做的修改立即生效）
./start c
```
```
> 使用说明：
> 自动采集或发布前需要先cd到crawler目录下
> 爬虫目录为crawler，统一读取config中的数据库信息。在此目录下执行python3 爬虫文件名可手动采集，加入系统定时任务可实现自动采集
> 项目模板目录templates，base.html中可直接添加统计代码
> 如使用远程文件需要注意附件手动上传static/images目录到远程服务器（可搭配oneindex的程序）
```
```
> 发布图集：
> 在项目post目录下新建目录，目录名为图集名称
> 将图片上传至新建的目录
> 在项目跟目录下执行sh start.sh post
> 输入要发布的图集个数
> 将crawler/AutoPost.py num 添加到定时任务可实现自动发布，如python3 AutoPost.py 5
```
手动安装说明
> 项目依赖python3.6 mysql5.6

```
1.安装python3.6
2.安装mysql5.5+ 建议5.6
3.克隆项目
4.进入项目目录执行 pip3 install -r requirements.txt
5.修改config.py和uwsgi.ini，uwsgi.ini需要取消英文部分的注释
6.导入sql文件
7.复制templates/zde/pagination.html 到/python安装目录/site-packages/dj_pagination/templates/pagination/
8.项目根目录下执行./start s 启动网站
9.如需反代自行安装nginx
```
如需使用反向代理，在nginx.conf中添加如下server段
```
server {
        listen       80;
        server_name  localhost; # 网站域名

        location / {
            proxy_pass http://127.0.0.1:8000;
        }
```
