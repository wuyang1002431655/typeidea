from django.shortcuts import render
# from django.http import HttpResponse
from .models import Post, Tag


def post_list(request, category_id=None, tag_id=None):
    # content = 'post_list category_id={category_id},tag_id={tag_id}'.format(category_id=category_id, tag_id=tag_id, )
    # return HttpResponse(content)
    # return render(request, 'blog/list.html', context={'name': 'post_list'})
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_lasts = []
        else:
            post_lasts = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_lasts = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            post_lasts = post_lasts.filter(category_id=category_id)
    return render(request, 'blog/list.html', context={'post_list': post_lasts})


def post_detail(request, post_id):
    # return HttpResponse('detail')
    # return render(request, 'blog/detail.html', context={'name': 'post_detail'})
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})


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
