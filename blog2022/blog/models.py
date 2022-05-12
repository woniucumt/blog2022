from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # post_count = models.IntegerField(default=1,verbose_name = "文章数量")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
                # 下面这句话会产生一次io操作吧?而且写的也不是很高明啊,能用post_set搭配那个select_related函数么？
                cate.post_count = Post.objects.filter(category=cate).count()
            else:
                normal_categories.append(cate)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    POST_ORIGNATE = "原创"
    POST_TRAMSMIT = "转载"
    POST_REPRINTE = "加工"
    IS_ORIGNAL = (
        (POST_ORIGNATE, '原创'),
        (POST_TRAMSMIT, '转载'),
        (POST_REPRINTE, '加工'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    # 这也是一种处理方式，下面的那种先不管，这种能用就行啊！
    desc = models.TextField(verbose_name="摘要",blank = True, max_length=1000)
    # desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文")
    # content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    # is_md = models.BooleanField(default=False, verbose_name="markdown语法")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_orignal = models.CharField(max_length=255, default="原创", choices=IS_ORIGNAL, verbose_name="文章类型")
    is_topped = models.BooleanField(default=False, verbose_name="是否顶置")
    # # 字数统计
    # word_count = models.PositiveIntegerField(default=0,verbose_name="字数统计")
    # read_time = models.PositiveIntegerField(default=12, verbose_name="建议阅读时间")
    #
    times = models.PositiveIntegerField(default=1)
    dianzan = models.PositiveIntegerField(default=1)
    @classmethod
    def hot_blogs(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-times')[0:5]

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']

    def __str__(self):
        return self.title
    #
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list = []
        else:
            post_list = tag.post_set.filter(status= Post.STATUS_NORMAL).select_related('owner','category')
        return post_list, tag
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list= []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return post_list, category
    @classmethod
    def all_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def get_topped(cls):
        post_topped = cls.objects.filter(is_topped=True)
        return post_topped
    # 注意这个save可不是admin里面的那个保存的方法，那个admin就是那个admin!是用来管理admin界面的！
    # def save(self, *args, **kwargs):
    #     # self.content_html = mistune.markdown(self.content)
    #     self.content_html = self.content
    #     # self.word_count = len(self.content.split())
    #     super().save(*args, **kwargs)

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_CHECKING = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_CHECKING, '审核中'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Post, verbose_name="被评文章", on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=2000, verbose_name="内容")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    status = models.PositiveIntegerField(default=STATUS_CHECKING, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
    @classmethod
    def get_comments(cls,target):
        return cls.objects.filter(target = target, status=cls.STATUS_NORMAL)[:4]