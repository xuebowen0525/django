from django.conf.urls import url
from .import views
app_name = 'blog' #要加上app_name = 'blog',会报错（'blog' is not a registered namespace）
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    # 分类
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
    #标签
    url(r'^tag/(?P<pk>[0-9]+)/$',views.tag,name='tag'),
    #搜索
    url(r'^search$', views.search, name='search')
]
# urlpatterns = [
#     url(r'^$',views.IndexView.as_view(),name='index'),
#     url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
#     url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
#     url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
#     url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
#     url(r'^search$', views.search, name='search')
# ]