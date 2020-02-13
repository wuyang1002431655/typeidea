from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def __str__(self):
        return self.name


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def __str__(self):
        return self.name


class CategoryOwnerFilter(admin.SimpleListFilter):
    # 通过集成Django admin提供的SimpleListFilter类实现自定义过滤器，然后把自定义过滤器配置到ModelAdmin
    # SimpleListFilter提供两个属性和两个方法供复习
    title = '分类过滤器'  # 展示标题
    parameter_name = 'owner_category'  # 查询时URL参数的名字

    # 例如查询分类id为1的内容，URL的Query部分是?owner_category=1，此时可以通过过滤器拿到这个id，从而进行过滤

    def lookups(self, request, model_admin):  # 返回要展示的内容和查询用的ID
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):  # 根据URL Query的内容返回列表页数据 例如?owner_category=1 得到id=1
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset  # QuerySet是列表页所有展示数据的合集


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'operator']
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category_name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    form = PostAdminForm
    # fields = (
    #     ('catrgory', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )
    # fieldsets用来控制布局，格式是有两个元素的tuple的list例如
    # fieldsets=(
    #     (名称,{内容}),
    #     (名称,{内容}),
    # )
    # 其中第一个元素是当前板块的名称，第二个元素是当前板块的描述,字段，样式配置
    # 也就是说第一个元素是string，第二个元素是dict，而dict的key可以是fields，description，classes
    # fields的效果是控制展示哪些元素，也可以给元素排序并组合元素位置
    # classes是给要配置的板块加上CSS属性，Django admin默认支持collapse和wide
    # filter_horizontal = ('tags',)#设置哪些字段横向展示
    # filter_vertical = ('tags',)#设置哪些字段纵向展示
    exclude = ('owner',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def __str__(self):
        return self.name

    # class Media:
    #     css={
    #         'all':("地址",),
    #     }
    #     js=('地址',)
    # 可以这样引用css和js
