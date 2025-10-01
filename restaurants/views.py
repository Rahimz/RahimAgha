from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag

from restaurants.models import Place


def ResHomeView(request):
    city = request.GET.get('city', None)
    tag = request.GET.get('tag', None)
    places = Place.actives.all()
    if city:
        places = places.filter(city=city)
        print('... gett city', city)
        
    if tag:
        print('... gett tag', tag)
        try:
            tag_obj = Tag.objects.get(slug=tag)
            print('... gett tag object', tag_obj)
        except:
            tag_obj = None
        if tag_obj:
            places= places.filter(tags__in=[tag_obj])        
    context = dict(
        page_title = _("Restaurants"),
        places=places,
        cities=Place.actives.order_by('city').distinct('city').values_list('city', flat=True),
        city=city,
        tag=tag,
    )
    return render(
        request,
        'restaurants/res_home.html',
        context
    )