from django.conf.urls import url
from .views import IndexView
from .views import ArchiveView
from .views import TagView
from .views import TagDetailView
from .views import BlogDetailView
from .views import CategoryDetailView
from .views import MyView
from .views import CategoryView
from .views import MySearchView

urlpatterns = [
    url(r'^about/$', MyView.as_view(), name='about'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive'),
    url(r'^tags/$', TagView.as_view(), name='tags'),
    url(r'^tags/(?P<tag_name>\w+)$', TagDetailView.as_view(), name='tag_name'),
    url(r'^blog/(?P<blog_id>\d+)$', BlogDetailView.as_view(), name='blog_id'),
    url(r'^category/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_name>\w+)/$', CategoryDetailView.as_view(), name='category_name'),
    url(r'^search/', MySearchView(), name='haystack_search'),
]