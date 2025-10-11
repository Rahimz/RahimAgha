from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from restaurants.models import Place, Category, Review, Vote
from .forms import ReviewSubmissionForm

def ResHomeView(request):
    city = request.GET.get('city', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('category', None)
    places = Place.actives.select_related('category').prefetch_related('vote_summary').all()
    categories = Category.objects.values_list('slug', flat=True)
    
    
    # Check if latitude and longitude are in the request
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        lat = Decimal(lat)
        lon = Decimal(lon)
        # Here you can implement the logic to find locations around lat/lon
        places = places.filter(
            latitude__range=(lat - Decimal(0.01), lat + Decimal(0.01)), # about 2.22 kilometer
            longitude__range=(lon - Decimal(0.01), lon + Decimal(0.01)))
        # print("... nearby_places", places)
    
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
        selected_lat=lat,
        selected_lon=lon,
    )
    return render(
        request,
        'restaurants/res_home.html',
        context
    )


@login_required
def ReviewView(request, place_uuid):
    place = get_object_or_404(Place, uuid=place_uuid)
    # Get the latest active review to vote on
    review = Review.objects.filter(active=True).prefetch_related('items').last()

    # Handle case where there is no active review
    if not review:
        messages.warning(request, _("There are no active reviews at the moment."))
        return redirect('restaurants:res_home') # or some other appropriate page

    # ADD for production Check if user has already voted on this review
    if Vote.objects.filter(user=request.user, review=review, place=place).exists():
        messages.info(request, _("You have already submitted a review for this place."))
        return redirect('restaurants:res_home')
    

    if request.method == 'POST':
        form = ReviewSubmissionForm(request.POST, review=review)
        if form.is_valid():
            form.save(user=request.user, place=place)
            messages.success(request, _("Thank you! Your review has been submitted successfully."))
            return redirect('restaurants:res_home') # Redirect to a success page
    else:
        form = ReviewSubmissionForm(review=review)

    context = {
        # 'page_title': _("Review Restaurants"),
        'page_title': _("Review ") + place.name,
        'review': review,
        'form': form
    }
    return render(
        request,
        'restaurants/review.html',
        context
    )
    