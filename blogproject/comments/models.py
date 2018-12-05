from django.db import models
from blog.models import Post
# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=10)
    text = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)
    def __str__(self):
        return self.text[:20]
