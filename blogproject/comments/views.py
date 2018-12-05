from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm
# Create your views here.

def post_comment(request,post_pk):
    # 这里获取文章内容，没有的话返回404页面
    post = get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        # 构造commentform表单
        form = CommentForm(request.POST)
    #表单可用
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        #将评论和被评论的文章关联起来
        comment.post = post
        # 最终保存到数据库
        comment.save()
        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，
        # 它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        return redirect(post)
    else:
        # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
        # 因此我们传了三个模板变量给 detail.html，
        # 一个是文章（Post），一个是评论列表，一个是表单 form
        # 注意这里我们用到了 post.comment_set.all() 方法，
        # 这个用法有点类似于 Post.objects.all()
        # 其作用是获取这篇 post 下的的全部评论，
        # 因为 Post 和 Comment 是 ForeignKey 关联的，
        # 因此使用 post.comment_set.all() 反向查询全部评论。
        # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
        comment_list = post.comment_set.all()
        context = {
            'post':post,
            'form':form,
            'comment_list':comment_list
        }
        return render(request,'blog/detail.html',context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return render(post)