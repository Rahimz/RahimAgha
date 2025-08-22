from django.shortcuts import render
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user}
                )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'accounts/register.html',
        {'user_form': user_form}
    )


# from django.urls import reverse_lazy
# from django.views.generic import CreateView
# from django.contrib.auth import login, logout
# from django.contrib.auth.forms import AuthenticationForm
# from django.http import JsonResponse
# from django.views.generic.edit import FormView
# from django.views import View
# import json

# from .forms import CustomUserCreationForm
# from .models import Profile




# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = "accounts/register.html"
#     success_url = reverse_lazy("home")

#     def form_valid(self, form):
#         response = super().form_valid(form) # saves User
#         # create Profile (or use signals instead)
#         Profile.objects.create(user=self.object)
#         login(self.request, self.object) # log user in after registration
#         return response
    
# class LoginView(FormView):
#     form_class = AuthenticationForm
#     http_method_names = ["post"]   # no GET template rendering

#     # If you prefer to allow GET for e.g. health-check, change http_method_names.
#     def get_form_kwargs(self):
#         """
#         Pass request into AuthenticationForm and accept either form-encoded POST
#         or a JSON body with {"username": "...", "password": "..."}.
#         """
#         kwargs = super().get_form_kwargs()
#         # parse JSON body if content-type is application/json
#         if self.request.content_type and "application/json" in self.request.content_type:
#             try:
#                 data = json.loads(self.request.body.decode() or "{}")
#             except ValueError:
#                 data = {}
#         else:
#             data = self.request.POST

#         # AuthenticationForm signature: AuthenticationForm(request, data)
#         kwargs["request"] = self.request
#         kwargs["data"] = data
#         return kwargs

#     def form_valid(self, form):
#         user = form.get_user()
#         login(self.request, user)  # create session
#         # return minimal user info (avoid exposing sensitive fields)
#         return JsonResponse({
#             "status": "ok",
#             "user": {"id": user.id, "username": user.get_username()}
#         })

#     def form_invalid(self, form):
#         # return form errors as JSON; 400 = Bad Request
#         return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# class LogoutView(View):
#     http_method_names = ["post"]  # use POST to protect against CSRF-tricks

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             logout(request)
#             return JsonResponse({"status": "ok"})
#         # If client tries to logout when not logged in, return 401 or ok depending on your policy
#         return JsonResponse({"status": "error", "message": "not authenticated"}, status=401)