from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag

from restaurants.models import Place, Category


def ResHomeView(request):
    city = request.GET.get('city', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('category', None)
    places = Place.actives.select_related('category').all()
    categories = Category.objects.values_list('slug', flat=True)
    
    if city:
        places = places.filter(city=city)
        # print('... gett city', city)
        
    if tag:
        # print('... gett tag', tag)
        try:
            tag_obj = Tag.objects.get(slug=tag)
            # print('... gett tag object', tag_obj)
        except:
            tag_obj = None
        if tag_obj:
            places= places.filter(tags__in=[tag_obj])        
    
    if category:
        try:
            category_obj = Category.objects.get(slug=category)        
            places = places.filter(category=category_obj)
        except:
            category = ''
            
    context = dict(
        page_title = _("Restaurants"),
        places=places,
        cities=Place.actives.order_by('city').distinct('city').values_list('city', flat=True),
        city=city,
        tag=tag,
        tags=Tag.objects.all(),
        category=category,
        categories=categories,
    )
    return render(
        request,
        'restaurants/res_home.html',
        context
    )