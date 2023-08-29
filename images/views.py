from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

# to count the images views  we use redis
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        #form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid 
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()

            # i store the user action
            create_action(request.user, 'bookmarked image', new_image)

            messages.success(request, "Image added successfully")
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request, "images/image/create.html", {
        "section" : "images",
        "form" : form
    })
    
def images_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # print(image)
    # exit("fin")

    r.zincrby('image_ranking', 1, image.id)

    # increment total image views by 1
    total_views = r.incr(f'image:{image.id}:views')

    return render(request, 'images/image/detail.html', {
        'section':'images',
        'image' : image,
        'total_views' : total_views,
    })
    
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action=='like':
                image.users_like.add(request.user)
                
                # store the user action
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # if page is not and integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # id AJAX request and page out of range 
            # return and empty page 
            return HttpResponse('')
        # if page out of range return last page of result 
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.html',{
            'section' : 'images',
            'images' : images
        })
    return render(request,'images/image/list.html',{
        'section': 'images',
        'images': images
        })
    
# Now, create a new view to display the ranking of the most viewed images.
@login_required
def image_ranking(request):
    # get the image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]

    # get the mots views image 
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(request,'images/image/ranking.html',{'section': 'images','most_viewed': most_viewed})