from django.shortcuts import render
from .models import Tag, Post, Category, Comment
from config.models import SideBar
from django.views.generic import DetailView, ListView,TemplateView, RedirectView
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, reverse
from blog.forms import CommentForm
# Create your views here.

'''The common view that contains work like getting the sidebars or tags
   You have to know that this is a Mixin view, it extends nothing, 
   so the view who extends it must extend other generic view at the same time'''
class Common_View_Mixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars':SideBar.get_all()})
        context.update(Category.get_navs())
        paginator_range = context["paginator"].page_range
        context.update({'hot_blogs': Post.hot_blogs()})
        context.update({
            "paginator_range": paginator_range
        })
        # addrString = ''
        # # 查询ip的接口
        # try:
        #     r = requests.get(url='http://whois.pconline.com.cn/ipJson.jsp?ip='+str(self.request.META.get('REMOTE_ADDR'))+'&json=true')
        #     print('http://whois.pconline.com.cn/ipJson.jsp?ip='+self.request.META.get('REMOTE_ADDR')+'&json=true')
        #     # print(type(json.loads(r.content)))
        #     jsonStr = json.loads(str(r.content, encoding="gbk"))
        #     # jsonStr = json.loads(str(r.content, encoding="utf-8"))
        #     # print(jsonStr["country"]+jsonStr["regionName"]+jsonStr["city"])
        #     # addrString = jsonStr["country"]+jsonStr["regionName"]+jsonStr["city"]
        #     addrString = jsonStr["addr"]
        # except Exception as e:
        #     print(e)
        # try:
        #     with open(os.path.dirname(os.path.abspath(__file__))+'visitRecord.txt', 'a') as f:
        #         f.write("IP："+self.request.META.get('REMOTE_ADDR')+"日期："+addrString+str(datetime.now())+"\n")
        #         f.close()
        # except Exception as e:
        #     print(e)
        # print("IP：",self.request.META.get('REMOTE_ADDR'),"日期：",datetime.now())
        return context



'''The firse page you will see with visiting'''
class Home_Home_View(TemplateView):
    template_name = 'homepages/Home_Home.html'

'''The academic page'''
class Home_Academic_View(TemplateView):
    template_name = 'homepages/Home_Academic.html'

'''The blog page'''
class Home_Blog_View(TemplateView):
    template_name = 'homepages/Home_Blog.html'

'''The gallery page'''
class Home_Gallery_View(TemplateView):
    template_name = 'homepages/Home_Gallery.html'

'''The about-me page which used in the Home_Home page'''
class Aboutme_View(TemplateView):
    template_name = 'about_me/About_Me.html'

'''The blog_index page, also show the list of blogs'''
class Blog_Index_View(Common_View_Mixin, ListView):
    queryset = Post.all_posts()
    paginate_by = 8
    context_object_name = 'blog_list'
    template_name = 'blog/Blog_Index.html'

'''The category view extends the Blog_Index_view'''
class Category_View(Blog_Index_View):
    template_name = 'blog/Cate_Blog_Index.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category,
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

'''The '''
class CommonViewMixinDetails:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars':SideBar.get_all()})
        context.update(Category.get_navs())
        # 略显笨拙的修改查看的方法……
        blog_id = self.kwargs.get('blog_id')
        Post.objects.filter(pk = int(blog_id)).update(times = F('times')+1)
        # 添加最热文章
        context.update({'hot_blogs':Post.hot_blogs()})
        context.update({'comments': Comment.get_comments(blog_id)})
        context.update({'comment_form':CommentForm})
        return context

'''The detail of one blog'''
class Blog_Detail_View(CommonViewMixinDetails, DetailView):
    pk_url_kwarg = 'blog_id'
    queryset = Post.all_posts()
    context_object_name = 'blog'
    template_name = 'blog/Blog_Details.html'

class Gallery_View(TemplateView):
    template_name = 'gallery/Gallery_Page.html'

class Comment_View(TemplateView):
    # http_method_names = ['GET']
    template_name = 'blog/Comment_Result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = Post.objects.get(id=target)
            instance.save()
            succeed = True
            # return self.render_to_response()
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            # 'target': target,
        }
        # return redirect(Post.objects.get(id=target))
        return self.render_to_response(context)