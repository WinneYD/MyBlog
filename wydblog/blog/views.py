import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from comments.form import CommentForm
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q

class IndexView(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name='post_list'
    paginate_by=3
    def get_context_data(self,**kwargs):
        '''
        在视图函数中将模板变量传递给模板是通过render函数的context参数传递字典实现，
        在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的，
        所以复写该方法，以便插入自定义的模板变量
        '''
        #获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)
        #父类模板中已经有 paginator,page_obj,is_paginated 这三个模板变量
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页
        #由于context是一个字典，调用get方法从中获取某个键对应的值
        paginator=context.get('paginator')
        page=context.get('page_obj')
        is_paginated=context.get('is_paginated')
        #调用自己写的pagination_data方法获得分页导航栏需要的数据
        pagination_data=self.pagination_data(paginator,page,is_paginated)
        #将分页导航条的模板变量更新到 context 中，pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        left=[]
        right=[]
        left_has_more=False
        right_has_more=False
        first=False
        last=False

        page_number=page.number
        total_pages=paginator.num_pages
        page_range=paginator.page_range

        left=page_range[(page_number-3) if (page_number-3)>0 else 0:(page_number-1) if (page_number-1)>0 else 0]
        right=page_range[page_number:page_number+2]
        if right:
            if right[-1] < total_pages - 1:
                right_has_more=True
            if right[-1] < total_pages:
                last=True
        if left:
            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True

        data={
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }
        return data






'''
def index(request):
    post_list=Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})
'''


class ArchivesView(IndexView):
    def get_queryset(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,created_time__month=month)

'''
def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,created_time__month=month)
    return render(request,'blog/index.html',context={'post_list':post_list})
'''

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
    #从URL捕获的命名组参数值保存在实例的kwargs属性里（是一个字典），非命名组参数值保存在实例的args属性里（是一个列表）

'''
def category(request,id):
    cate=get_object_or_404(Category,id=id)
    post_list=Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})
'''

class TagView(IndexView):
    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)


class PostDetailView(DetailView):
    model=Post
    template_name='blog/detail.html'
    context_object_name='post'
    #文章阅读量增加
    def get(self,request,*args,**kwargs):
        #get方法返回的是一个HttpResponse实例
        #先调用父类的get方法后，才有self.object属性，其值为Post模型实例，及被访问的文章post
        response=super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        #视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md=markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',  #代码高亮拓展
                TocExtension(slugify=slugify),    #自动生成目录
            ]
        )
        post.body=md.convert(post.body)
        post.toc=md.toc
        return post


    def get_context_data(self,**kwargs):
        #把评论表单和post的评论列表传递给模板
        context=super(PostDetailView, self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})





'''
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    post.increase_views()
    # 记得在顶部引入 markdown 模块
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form=CommentForm()
    comment_list=post.comment_set.all()
    context={
        'post':post,
        'form':form,
        'comment_list':comment_list,
    }
    return render(request, 'blog/detail.html', context=context)
'''

# Create your views here.

