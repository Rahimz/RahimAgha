from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def AiView(request):
    context = dict(
        page_title = 'ai'
    )
    return render(
        request,
        'ai/ai_home.html',
        context
    )
