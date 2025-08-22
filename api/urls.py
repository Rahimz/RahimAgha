from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.permissions import IsSuperUser


app_name = 'api'

schema_view = get_schema_view(
   openapi.Info(
      title="RahimAgha API",
      default_version='v1',
      description="Test description",
      terms_of_service="",
      contact=openapi.Contact(email="rahim.django.projects@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=[IsSuperUser],
)


urlpatterns = [
    path('question/list/', views.QuestionListAPIView.as_view(), name='api_question_list' ),

    # drf-yasg urls
    re_path(
      r'^swagger(?P<format>\.json|\.yaml)$', 
      schema_view.without_ui(cache_timeout=0), 
      name='schema-json'
      # permission_classes=[IsSuperUser], # we could add a permission class here if needed
   ),
    re_path(
      r'^swagger/$', 
      schema_view.with_ui('swagger', cache_timeout=0), 
      name='schema-swagger-ui'
   ),
    re_path(
      r'^redoc/$', 
      schema_view.with_ui('redoc', cache_timeout=0), 
      name='schema-redoc'
   ),
]
