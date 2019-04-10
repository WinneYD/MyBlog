from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .form import CommentForm

def post_comment(request,post_id):
    #获取被评论的文章，因为后面要与被评论的文章联系起来
    #get_object_or_404函数的作用，获取的文章（Post）存在时获取，否则返回404页面给用户
    post=get_object_or_404(Post,id=post_id)
    #当用户请求为POST时需要开始处理表单
    if request.method=='POST':
        #用户提交的数据存储在request_POST中，这是一个类字典对象
        form=CommentForm(request.POST)

        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect(post)
        else:
            comment_list=Comment.objects.filter(post=post)
            context={'post':post,'form':form,'comment_list':comment_list}
            return render(request,'blog/detail.html',context)
        #不是POST请求，说明用户没有提交数据，重定向到文章详情页
        return redirect(post )



# Create your views here.
