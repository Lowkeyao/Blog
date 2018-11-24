import markdown
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from haystack.views import SearchView

from blog.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
from .models import Blog, Category, Tag
from pure_pagination import PageNotAnInteger, Paginator
# Create your views here.


# 关于我
class MyView(View):
    def get(self, request):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()
        return render(request, 'about.html', {'blog_nums': blog_nums,
                                              'cate_nums': category_nums,
                                              'tag_nums': tag_nums
                                              })


# 首页

class IndexView(View):
    def get(self, request):

        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()

        all_blog = Blog.objects.all().order_by('-id')

        for blog in all_blog:
            blog.content = markdown.markdown(blog.content.replace("\r\n", '  \n'),
                                             extensions=['markdown.extensions.extra',
                                                         'markdown.extensions.codehilite',
                                                         'markdown.extensions.toc'
                                                         ])

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blog, 3, request=request)
        all_blog = p.page(page)

        return render(request, 'index.html', {'all_blog': all_blog,
                                              'blog_nums': blog_nums,
                                              'cate_nums': category_nums,
                                              'tag_nums': tag_nums
                                              })


# 归档
class ArchiveView(View):
    def get(self, request):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()
        all_blog = Blog.objects.all().order_by('-create_time')

        return render(request, 'archive.html', {'all_blog': all_blog,
                                                'blog_nums': blog_nums,
                                                'cate_nums': category_nums,
                                                'tag_nums': tag_nums,
                                                })


# 云标签
class TagView(View):
    def get(self, request):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()
        all_tag = Tag.objects.all()

        return render(request, 'tags.html', {'all_tag': all_tag,
                                             'blog_nums': blog_nums,
                                             'cate_nums': category_nums,
                                             'tag_nums': tag_nums,
                                             })


# 标签下的所有博客
class TagDetailView(View):
    def get(self, request, tag_name):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()

        tag = Tag.objects.filter(name=tag_name).first()
        tag_blogs = tag.blog_set.all()

        return render(request, 'tag-detail.html', {'tag_blogs': tag_blogs,
                                                   'tag_name': tag_name,
                                                   'blog_nums': blog_nums,
                                                   'cate_nums': category_nums,
                                                   'tag_nums': tag_nums,
                                                   })


# 博客详情页
class BlogDetailView(View):
    def get(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()

        # 博客点击数+1, 评论数统计
        blog.click_nums += 1
        blog.save()
        # blog = Blog.objects.get(id=blog_id)

        blog.content = markdown.markdown(blog.content.replace("\r\n", '  \n'),
                                         extensions=['markdown.extensions.extra',
                                                     'markdown.extensions.codehilite',
                                                     'markdown.extensions.toc'
                                                     ])
        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True
        return render(request, 'blog-detail.html', {'blog': blog,
                                                    'blog_prev': blog_prev,
                                                    'blog_next': blog_next,
                                                    'has_prev': has_prev,
                                                    'has_next': has_next,
                                                    'blog_nums': blog_nums,
                                                    'cate_nums': category_nums,
                                                    'tag_nums': tag_nums,
                                                    })


class CategoryView(View):
    def get(self, request):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()

        all_cate = Category.objects.all()

        return render(request, 'cates.html', {'all_cate': all_cate,
                                              'blog_nums': blog_nums,
                                              'cate_nums': category_nums,
                                              'tag_nums': tag_nums
                                              })


class CategoryDetailView(View):
    def get(self, request, category_name):
        blog_nums = Blog.objects.count()
        category_nums = Category.objects.count()
        tag_nums = Tag.objects.count()

        category = Category.objects.filter(name=category_name).first()
        cate_blogs = category.blog_set.all()

        return render(request, 'category-detail.html', {'cate_blogs': cate_blogs,
                                                        'cate_name': category_name,
                                                        'blog_nums': blog_nums,
                                                        'cate_nums': category_nums,
                                                        'tag_nums': tag_nums,
                                                        })


class MySearchView(SearchView):

    def build_page(self):
        # 分页重写
        super(MySearchView.self).extra_context()

        try:
            page_no = int(self.request.GET.get('page', 1))

        except PageNotAnInteger:
            raise HttpResponse("Not a vaild number for page")

        if page_no < 1:
            raise HttpResponse("Pages should be 1 or greater")

        paginator = Paginator(self.results, HAYSTACK_SEARCH_RESULTS_PER_PAGE, request=self.request)

        page = paginator.page(page_no)

        return paginator, page
