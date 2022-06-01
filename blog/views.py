from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, BlogComment, Category
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras


def LikeView(request, pk, slug):
    # print(11111111111, request.POST.get('post_id'))
    post = get_object_or_404(Post, sno=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        print("POST", post, "SLUG", slug, "PK", pk)
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blogPost', kwargs={'slug': slug, 'pk': pk}))


# Create your views here.
def blogHome(request):
    # allPosts = Post.objects.all();
    allPosts = None

    # categories = Category.get_all_categories()
    categories = Category.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        allPosts = Post.get_all_post_by_categoryid(categoryID)
    else:
        allPosts = Post.get_all_post();

    data = {}
    data['allPosts'] = allPosts
    data['categories'] = categories
    # context = {'allPosts': allPosts}
    # return render(request, "blog/blogHome.html", context)
    return render(request, 'blog/blogHome.html', data)


def blogPost(request, slug, pk, *args, **kwargs):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)

    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print("KEY", pk)
    stuff = get_object_or_404(Post, sno=pk)
    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    total_likes = stuff.total_likes()

    liked = False
    print("Stuff", stuff)
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    context['total_likes'] = total_likes
    context["liked"] = liked
    return render(request, "blog/blogPost.html", context)


def postComment(request):
    global post
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")


class AddPostView(CreateView):
    model = Post
    template_name = 'blog/add_post.html'
    fields = ['title', 'author', 'slug', 'content', 'category']


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    fields = ['title', 'slug', 'content']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home')


