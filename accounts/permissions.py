from django.shortcuts import render
from functools import wraps

# def ai_access_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         # Assuming `request.user` is the user object you have, you can check the attribute as follows:
#         if not request.user.is_authenticated or not getattr(request.user.profile, 'ai_access', False):
#             return HttpResponseForbidden("You do not have access to this resource.")
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view

def ai_access_required(template_name="ai_access_denied.html", status=403):
    """
    Can be used as:
      @ai_access_required
      @ai_access_required()
      @ai_access_required("custom_template.html")
    """
    # Support usage without parentheses
    if callable(template_name):
        func = template_name
        template_name = "ai/ai_access_denied.html"
        return ai_access_required(template_name)(func)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated and getattr(user.profile, "ai_access", False)):
                # optionally provide context data to template
                context = {"next": request.get_full_path(), "user": user}
                return render(request, template_name, context=context, status=status)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator