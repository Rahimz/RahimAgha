from django.shortcuts import render, redirect
from functools import wraps
from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access certain views.
    it does not work in generic views and we should use `IsAdminUser` instead.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
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
        template_name = "access_denied.html"
        return ai_access_required(template_name)(func)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated and getattr(user.profile, "ai_access", False)):
                # # optionally provide context data to template
                # context = {"next": request.get_full_path(), "user": user}
                return redirect('generals:no_access')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

def accounting_access_required(template_name="ai_access_denied.html", status=403):
    """
    Can be used as:
      @accounting_access_required
      @accounting_access_required()
      @accounting_access_required("custom_template.html")
    """
    # Support usage without parentheses
    if callable(template_name):
        func = template_name
        template_name = "access_denied.html"
        return accounting_access_required(template_name)(func)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated and getattr(user.profile, "accounting_access", False)):
                # # optionally provide context data to template
                # context = {"next": request.get_full_path(), "user": user}
                return redirect('generals:no_access')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


class AccountingAccessRequiredMixin:
    """
    Mixin for class-based views that requires `user.profile.accounting_access`.
    Usage:
    class MyView(LoginRequiredMixin, AccountingAccessRequiredMixin, View):
    access_denied_template = "ai/custom_access_denied.html" # optional
    access_denied_status = 403 # optional
    """

    # defaults — override on your view if needed
    access_denied_template = "access_denied.html"
    access_denied_status = 403

    def get_access_denied_template(self):
        return self.access_denied_template

    def get_access_denied_status(self):
        return self.access_denied_status

    def get_access_denied_context(self):
        # provide context for the template; override if you need custom context
        return {"next": self.request.get_full_path(), "user": getattr(self.request, "user", None)}

    def user_has_accounting_access(self):
        user = getattr(self.request, "user", None)
        if not (user and user.is_authenticated):
            return False
        profile = getattr(user, "profile", None)
        return bool(getattr(profile, "accounting_access", False))

    def dispatch(self, request, *args, **kwargs):
        # If the user doesn't have accounting access, render the template and don't proceed.
        if not self.user_has_accounting_access():
            context = self.get_access_denied_context()
            return render(
                request,
                self.get_access_denied_template(),
                context=context,
                status=self.get_access_denied_status(),
            )
        return super().dispatch(request, *args, **kwargs)

class ApiAccessRequiredMixin:
    """
    Mixin for class-based views that requires `user.profile.api_access`.
    Usage:
    class MyView(LoginRequiredMixin, ApiAccessRequiredMixin, View):
    access_denied_template = "ai/custom_access_denied.html" # optional
    access_denied_status = 403 # optional
    """

    # defaults — override on your view if needed
    access_denied_template = "access_denied.html"
    access_denied_status = 403

    def get_access_denied_template(self):
        return self.access_denied_template

    def get_access_denied_status(self):
        return self.access_denied_status

    def get_access_denied_context(self):
        # provide context for the template; override if you need custom context
        return {"next": self.request.get_full_path(), "user": getattr(self.request, "user", None)}

    def user_has_api_access(self):
        user = getattr(self.request, "user", None)
        if not (user and user.is_authenticated):
            return False
        profile = getattr(user, "profile", None)
        return bool(getattr(profile, "api_access", False))

    def dispatch(self, request, *args, **kwargs):
        # If the user doesn't have api access, render the template and don't proceed.
        if not self.user_has_api_access():
            context = self.get_access_denied_context()
            return render(
                request,
                self.get_access_denied_template(),
                context=context,
                status=self.get_access_denied_status(),
            )
        return super().dispatch(request, *args, **kwargs)