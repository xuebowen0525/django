# django--
django博客（发布、详情、首页、搜索、评论、筛选）

django modles中创建表中字段后创建数据库表：
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations --empty 你的应用名(无法创建表时，先执行这句再创建)


django 运行：
python manage.py runserver

创建app:
python manage.py startapp 项目资源共享名
创建django项目：
django-admin startproject 项目名称 
python manage.py startproject 项目名称
创建超级管理员：
python manage.py createsuperuser
1、urls.py 
添加创建app的文件路由：path('index/', views.index),
2、创建app中创建index函数
def index（request）：
	return render（request，‘xxx.html’）
3、models.py中创建数据库表
class 表名（modles.Modle）：
	pass
4、创建templates目录新建一个xxx.html文件
5.settings中templas里添加
        'DIRS': [os.path.join(BASE_DIR,'templates')],
最后添加：
   STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

参考：https://blog.csdn.net/xudailong_blog/article/list/11?t=1
