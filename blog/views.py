from django.contrib.auth.models import User
from django.db.models import Q 
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

# Create your views here.

def post_list(request):
    post = Post.objects.all()
    if(request):
        query = request.GET.get("q")
        results = Post.objects.filter(Q(title=query) | Q(name=query))
        print (results)
    return render(request, 'blog/post_list.html', {'post': post , 'results': results})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
def Search(request):
        query = request.GET.get('q')
        print (query)
        results = Post.objects.filter(Q(title=query) | Q(published_date__year=query) | Q(name=query))
        print (results)
        return render(request, 'blog/search.html', {'results': results})
