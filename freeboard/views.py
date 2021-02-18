from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Post, Comment

@login_required(login_url='common:login')
def list(request):
    page = request.GET.get('page', '1')

    post_list = Post.objects.order_by('-create_date')

    paginator = Paginator(post_list, 10)
    page_obj = paginator.get_page(page)

    context = {'post_list': page_obj}
    return render(request, 'freeboard_list.html', context)


@login_required(login_url='common:login')
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'freeboard_detail.html', context)


@login_required(login_url='common:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            return redirect('freeboard:list')
    else:
        form = PostForm()

    context = {'form': form}

    return render(request, 'freeboard_create.html', context)


@login_required(login_url='common:login')
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('freeboard:list', post_id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.modify_date = timezone.now()
            post.save()
            return redirect('', post_id=post_id)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'freeboard_list.html', context)


@login_required(login_url='common:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('freeboard:list', post_id=post.id)

    post.delete()

    return redirect('freeboard:list')

@login_required(login_url='common:login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('freeboard:detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm()

    context = {'form': form}
    return render(request, 'freeboard_list.html', context)


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('freeboard:detail', post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('freeboard:detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)

    context = {'form': form}
    return render(request, '', context)


@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('freeboard:detail', post_id=comment.post_id)
    else:
        comment.delete()

    return redirect('freeboard:detail', post_id=comment.post_id)

