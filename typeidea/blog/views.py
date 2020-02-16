# from django.shortcuts import render
# from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


#
# def post_list(request, category_id=None, tag_id=None):
#     # content = 'post_list category_id={category_id},tag_id={tag_id}'.format(category_id=category_id, tag_id=tag_id, )
#     # return HttpResponse(content)
#     # return render(request, 'blog/list.html', context={'name': 'post_list'})
#     tag = None
#     category = None
#
#     # if tag_id:
#     #     try:
#     #         tag = Tag.objects.get(id=tag_id)
#     #     except Tag.DoesNotExist:
#     #         post_lasts = []
#     #     else:
#     #         post_lasts = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     # else:
#     #     post_lasts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     #     if category_id:
#     #         try:
#     #             category = Category.objects.get(id=category_id)
#     #         except Category.DoesNotExist:
#     #             category = None
#     #     else:
#     #         post_lasts = post_lasts.filter(category_id=category_id)
#     #
#     # context={
#     #     'category':category,
#     #     'tag':tag,
#     #     'post_list':post_lasts
#     # }
#     # return render(request, 'blog/list.html', context=context)
#     if tag_id:
#         post_last, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_last, category = Post.get_by_category(category_id)
#     else:
#         post_last = Post.latest_posts()
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_last,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id):
#     # return HttpResponse('detail')
#     # return render(request, 'blog/detail.html', context={'name': 'post_detail'})
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context={
#         'post':post,
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)


'''
render方法笔记
render(request,template_name,content=None,content_type=None,status=None,using=None)

request 封装HTTP请求的request对象
template_name 模板名称 传入时可带上路径
context 字典数据 会传递到模板中
content_type 页面编码类型 默认text/html
status 状态码 默认200
using 使用哪种模板引擎解析 也可在settings中配置 默认使用Django自带模板

'''
