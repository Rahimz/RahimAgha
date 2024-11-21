from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import Http404
from django.urls import reverse

from .models import Post, Attachment
from .forms import (
    AddAttachmentCodeForm, AddAttachmentImageForm,
    AddAttachmentLinkForm, AddAttachmentScriptForm,
    AddAttachmentTextForm, AddAttachmentTitleForm
)


DICT_FORM = dict(
        code = AddAttachmentCodeForm,
        image = AddAttachmentImageForm,
        link = AddAttachmentLinkForm, 
        script = AddAttachmentScriptForm,
        title = AddAttachmentTitleForm,
        text = AddAttachmentTextForm,
    )


def BlogPostView(request, slug, attach_type=None):
    post = get_object_or_404(Post, slug=slug, published=True, active=True)
    attachments_count = post.attachments.all().count()
    dict_form = DICT_FORM
    if not post.active:
        raise Http404        
    
    if type and not request.user.is_superuser:
        messages.warning(request,_("You do not have permission"))
        return redirect('blog:blog_post', post.slug)
    
    # print('-----: ', [item for item, name in Attachment.AttachType.choices])
    if attach_type in [item for item, name in Attachment.AttachType.choices]:
                
        form_class = dict_form[attach_type]
        # print('-----: get the form class')
        
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES)
            if form.is_valid():
                new_attachment = form.save(commit=False)
                new_attachment.post = post
                new_attachment.type = attach_type
                new_attachment.save()
                messages.success(request, _("Attachment added"))
                url = f"{reverse('blog:blog_post', args=[post.slug])}#attach_id_{new_attachment.id}"
                return redirect(url)
                
            # print('-----: in method POST')
        else:
            form =form_class(initial={'rank': attachments_count + 1})
            
            # print('-----: in method GET')
    else:
        form = None
        # print('-----: form is None')
        
    
    attachments = post.attachments.filter(active=True)
    
    dict_form = DICT_FORM
    context = dict(
        page_title=post.title,
        post=post,
        attachments=attachments,
        dict_form=dict_form,
        attach_type=attach_type,
        form=form
    )
    return render(
        request,
        'blog/post_details.html',        
        context
    )



def BlogPostListView(request):
    posts = Post.actives.filter(published=True)
    context = dict(
        page_title=_("Blog"),
        posts=posts
    )
    return render(
        request,
        'blog/blog_posts.html',
        context
    )


@staff_member_required
def ChangeAttachmentRankView(request, attach_id, dir):    
    attachment = get_object_or_404(Attachment, id=attach_id)
    print('-----: ', attachment.title, attachment.rank)
    attachs = attachment.post.attachments.exclude()
    if dir == 'up':
        before_attach = attachs.filter(rank__lt=attachment.rank).last()
        if before_attach:
            before_attach.rank += 1
            before_attach.save(update_fields=["rank"])
        if attachment.rank > 1:
            attachment.rank -= 1            
            attachment.save(update_fields=["rank"])
    elif dir == 'down':
        after_attach = attachs.filter(rank__gt=attachment.rank).first()
        if after_attach and after_attach.rank > 1:
            after_attach.rank -= 1
            after_attach.save(update_fields=["rank"])
        
        attachment.rank += 1            
        attachment.save(update_fields=["rank"])
        
    url = f"{reverse('blog:blog_post', args=[attachment.post.slug])}#attach_id_{attachment.id}"
    return redirect(url)
    