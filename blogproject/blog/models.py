from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import markdown
from django.utils.html  import strip_tags
# 专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
from django.contrib.auth.models import User
# Create your models here.
#更改表结构后要更新表

# 分类数据库表
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 标签数据库
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章数据库
class Post(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,blank=True,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    def increase_views(self):
        self.views +=1
        # update_fields 只更新数据库中的views
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering=['-created_time']

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)