from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comment, PostLike, PostDeslike, Ingredients
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, IngredientForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    likes_count = PostLike.objects.filter(post_id= pk).count()
    deslikes_count = PostDeslike.objects.filter(post_id = pk).count()

    percent_likes = 0
    percent_deslikes = 0
    total_reactions = likes_count + deslikes_count

    if total_reactions == 0:
        percent_likes = 0
        percent_deslikes = 0
    else:
        percent_likes = likes_count / total_reactions * 100
        percent_deslikes = deslikes_count / total_reactions * 100

    if likes_count > 0:
        liked = True 
    else:
        liked = False

    if deslikes_count > 0:
        desliked = True
    else:
        desliked = False 

    if liked or desliked:
        reacted = True
    else:
        reacted = False     
   
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'liked': liked,
        'reacted': reacted,
        'percent_likes': percent_likes,
        'percent_deslikes': percent_deslikes}
        )
    
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
    
@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_like(request, pk):
    post_like, created = PostLike.objects.get_or_create(post_id=pk, user=request.user)
    return redirect('post_detail', pk=pk)

def post_deslike(request, pk):
    post_deslike, created = PostDeslike.objects.get_or_create(post_id=pk, user=request.user)
    return redirect('post_detail', pk=pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
    
@login_required
def ingredient_new(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)         
        if form.is_valid():
           form.save()
        return redirect('ingredients_list')
    else:
        form = IngredientForm()
    return render(request,'blog/ingredient_edit.html',{'form': form})

def ingredients_list(request):
    ingredients = Ingredients.objects.filter().order_by('name')
    return render(request, 'blog/ingredient_list.html', {'ingredients': ingredients})

def searchposts(request):
    if request.method == 'GET':

        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(cooking_method__icontains=query) 

            results= Post.objects.filter(lookups,published_date__isnull=False).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'blog/search_post.html', context)

        else:
            post_list(request)