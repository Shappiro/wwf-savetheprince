from django.shortcuts import render, get_object_or_404, redirect


from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
app_name = __package__

def post_list(request):
    news = Post.objects.all().order_by('-date')
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    return render(request, app_name + '/post_list.html', {'news': news,'page_obj': page_obj})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, app_name + '/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, app_name + '/post_detail.html', {'new': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, app_name + '/post_edit.html', {'form': form})