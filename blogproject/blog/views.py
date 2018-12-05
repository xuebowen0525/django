from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  #分页
from django.views.generic import ListView,DetailView

from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.utils.text import slugify
# Create your views here.
def index(request):
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})

class IndexView(ListView):
    def __init__(self):
        pass
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2
    def get_context_data(self,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        #调用 pagination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator,page,is_paginated)
        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        # 当前页右边连续的页码号，初始值为空
        right = []
        # 标示第 1 页页码后是否需要显示省略号
        left_has_more =False
        # 标示最后一页页码后是否需要显示省略号
        right_has_more =False
        first = False
        last = False
        # # 获得用户当前请求的页码号
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number+2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left':left,
            'right':right,
            'right_has_more':right_has_more,
            'left_has_more':left_has_more,
            'first':first,
            'last':last,
        }
        return data
#详情页
def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.body = markdown.markdown(post.body,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    #评论数
    form = CommentForm()
    #获取全部评论文章
    comment_list = post.comment_set.all()
    #每访问一次views+1
    post.increase_views()
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list
    }
    return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )


def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    pagination_data = pagination_data(paginator,page,is_paginated)
    context = context.updata(pagination_data)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag)

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q :
        error_msg='请输入关键字'
        return render(request,'blog/index.html',{'error_msg':error_msg})
    else:
        #icontains不区分大小写；contains区分大小写
        post_list = Post.objects.filter(title__icontains=q)
        paginator = Paginator(post_list,2)
        page = request.GET.get('page')
        try:
            post_list  = paginator.page(page)
        except PageNotAnInteger:
            post_list  = paginator.page(1)
        except EmptyPage:
            post_list  = paginator.page(paginator.num_pages)
        return render(request,'blog/index.html',{'post_list':post_list,'error_msg':error_msg})



# def listing():
#     paginator = Paginator(post_list,2)
#     page = request.GET.get('page')
#     try:
#         post_list  = paginator.page(page)
#     except PageNotAnInteger:
#         post_list  = paginator.page(1)
#     except EmptyPage:
#         post_list  = paginator.page(paginator.num_pages)
#     return post_list

# #主页面
# def index(request):
#     post_list = Post.objects.all()
#     # paginator = Paginator(post_list,2)
#     # page = request.GET.get('page')
#     # try:
#     #     post_list  = paginator.page(page)
#     # except PageNotAnInteger:
#     #     post_list  = paginator.page(1)
#     # except EmptyPage:
#     #     post_list  = paginator.page(paginator.num_pages)
#     listing()
#     return render(request,'blog/index.html',context={"post_list":post_list})

# #详情页
# def detail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     post.body = markdown.markdown(post.body,extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     #评论数
#     form = CommentForm()
#     #获取全部评论文章
#     comment_list = post.comment_set.all()
#     #每访问一次views+1
#     post.increase_views()
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list
#     }
#     return render(request,'blog/detail.html',context=context)

# # 归档视图
# def archives(request,year,month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})


# # 分类视图
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

# #标签视图
# def tag(request,pk):
#     cata = get_object_or_404(Tag,pk=pk)
#     tag_list = Post.objects.filter(tag=cata)
#     return render(request,'blog/index.html',context={'post_list':tag_list})

# def search(request):
#     q = request.GET.get('q')
#     error_msg = ''
#     if not q :
#         error_msg='请输入关键字'
#         return render(request,'blog/index.html',{'error_msg':error_msg})
#     else:
#         #icontains不区分大小写；contains区分大小写
#         post_list = Post.objects.filter(title__icontains=q)
#         paginator = Paginator(post_list,2)
#         page = request.GET.get('page')
#         try:
#             post_list  = paginator.page(page)
#         except PageNotAnInteger:
#             post_list  = paginator.page(1)
#         except EmptyPage:
#             post_list  = paginator.page(paginator.num_pages)
#         return render(request,'blog/index.html',{'post_list':post_list,'error_msg':error_msg})

    
