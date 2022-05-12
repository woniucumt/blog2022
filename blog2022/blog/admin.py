from django.contrib import admin
from .models import Post, Category, Tag, Comment
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .adminforms import PostAdminForm
# Register your models here.

# inline是内联控制编辑的。
# TabularInline是样式
class PostInline(admin.TabularInline):
    fields = ('title', 'desc', 'content', 'status', 'category', 'tag','owner')
    extra = 1 #控制额外多几个。
    model = Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('name','status','owner','is_nav','created_time','post_count')
    fileds=('name','status','is_nav')

    # 但是这个自定义方法什么时候用呢？
    # 这里的这个post_set确定真的有用？还是已经没用了在2.0中？
    # 这个post_set是外键，自动生成的。
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"

    # 调用父类的save方法
    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','owner','created_time')
    fields=('name','owner','status')

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)

class CategoryOwnerFilter(admin.SimpleListFilter):
    #"自定义过滤器"
    title = '分类过滤器'
    parameter_name='owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.values())
        return queryset

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []
    # 配置右边的过滤器的
    # 就是界面右边的那个方框过滤器，一般也没人看的那个,下面就是按照状态分类了。
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category__name']
    # 下面这三个是真的没用。
    # 话说配置是真的全在admin中啊，只要知道说明书，用插件就行了
    actions_on_top = True
    # actions_on_bottom = True
    # save_on_top = True

    # fields = (('category','title'),
    #           'desc','status','is_topped','is_orignal',('word_count','read_time'),'content','tag',)
    fields = (
        ('title','category'),
         'desc',
         'status',
         'content',
         'tag',)
    # fieldsets = (
    #     ('基础配置',{
    #         'description':'基础配置描述',
    #         'field':(
    #             ('title','category'),
    #             'status',
    #         ),
    #     }),
    # )

    # 这个是自定义操作的。其实也没啥用
    # 但我奇怪的是，自定义字段只要定义函数就行了
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'
    # This would cause a problem.
    #  If you add post through inline way, this save method could not be called!
    # You can add owner into the fields of PostInline
    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)

    # 这个倒确实是在admin当中，因为你在定制admin能看到的东西。
    # 那这里的request又是从哪里传进来的呢？
    def get_queryset(self,request):
        qs=super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'target','content','nickname',
        'status',
    ]
    fields = ['target','content','nickname',
        'status',]
    list_display_links = []
    # 配置右边的过滤器的
    # 就是界面右边的那个方框过滤器，一般也没人看的那个,下面就是按照状态分类了。
    list_filter = [CategoryOwnerFilter]