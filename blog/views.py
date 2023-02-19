from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try: 
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    
    
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'tag': tag})

def post_detail(request, year, month,day,post):
    # try:
    #     post=Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # list of active comments for this post 
    comments = post.comments.filter(active=True)
    # Form for users to comment 
    form = CommentForm()
    
    # List of similar posts 
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # print(similar_posts.query)
    
    return render(request, 'blog/post/detail.html',
                  {'post':post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})

def post_share(request, post_id):
    #Retrive by post id
    sent=False
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            # form field pased the validation
            cd = form.cleaned_data
            # ... send email 
            # cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'chedjou.rocelin@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()   
    return render (request, 'blog/post/share.html', {'post':post, 'form':form, 'sent': sent})

# view for comment 
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',{'post': post,'form': form,'comment': comment})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            # stemming research 
            # results = Post.published.annotate(
            #     search=SearchVector('title', weight='A') + SearchVector('body', weight='B'), 
            #     rank=SearchRank(search_vector, search_query)
            #     ).filter(search=search_query).order_by('-rank')
            
            # trigrame search by similarity 
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results 
    })

# Create your views here.


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'
