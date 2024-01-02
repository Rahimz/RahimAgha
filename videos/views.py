from django.shortcuts import render


def VideoListView(request):
    return render (
        request,
        'videos/videos_list.html',
    )
